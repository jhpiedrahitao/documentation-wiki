import os
import random
import pandas as pd
from tqdm import tqdm
import langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import QAGenerationChain
from langchain.evaluation.qa import QAEvalChain
from dotenv import load_dotenv
if __name__ == "__main__":
    from DocumentEmbedder import DocumentEmbedder
    from QuestionAnswering import QuestionAnswering

load_dotenv()
langchain.debug = False

class ModelEvaluation:
    """
    A class for evaluating a document embedder and a question answering system.

    Args:
        document_embedder: An instance of DocumentEmbedder.
        question_answering: An instance of QuestionAnswering.

    Methods:
        generate_question_answer_pairs(self, out_path:str, question_number:int = 5, llm = ChatOpenAI(temperature=0.5,model_name="gpt-3.5-turbo")):
            Generates n question-answer pairs based on random subset of the given documents.

        evaluate_questions(self, qa_path:str ,out_path:str):
            pass the generated questions troug the question_answering object and saves the results.

        evaluate_responses(self, qar_path:str ,out_path:str, llm= ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo")):
            Evaluates the responses against the answers and calculates LLM Based Evaluation Accuracy.
    """

    def __init__(self, document_embedder, question_answering):
        self.document_embedder = document_embedder
        self.question_answering = question_answering
        tqdm.pandas()

    def generate_question_answer_pairs(self, out_path:str, question_number:int = 5, llm = ChatOpenAI(temperature=0.5,model_name="gpt-3.5-turbo")):
        """
        Generates question-answer pairs based on a the set of documents in the document_embedder.

        Args:
            out_path (str): The path to save the generated question-answer pairs csv file.
            question_number (int): The number of question-answer pairs to generate, Default is 5.
            llm: The language model to use for generating questions and answers.

        Returns:
            None
        """
        # set chain
        template = """You are a smart assistant designed to come up with meaninful question and answer pair. The question should be to the point and the answer should be as detailed as possible.
        Given a piece of text, you must come up with a question and answer pair that can be used to evaluate a QA bot. Do not make up stuff. Stick to the text to come up with the question and answer pair.
        When coming up with this question/answer pair, you must respond in the following format:
        ```
        {{
            "question": "$YOUR_QUESTION_HERE",
            "answer": "$THE_ANSWER_HERE"
        }}
        ```

        Everything between the ``` must be valid json.
        Please come up with a question/answer pair, in the specified JSON format, for the following text:
        ----------------
        {text}"""
        promt_Template = PromptTemplate.from_template(template)
        generation_chain = QAGenerationChain.from_llm(llm=llm, prompt=promt_Template)
        #et a sample of thedocuments in the knowledge base 
        documents=[doc.page_content for doc in self.document_embedder.documents]      
        documents=random.sample(documents, question_number)
        #generate question answers pairs
        qa_pairs = []
        for document in tqdm(documents, desc="Generating Question Answer pairs"):
            try:
                qa=generation_chain.run(text=document)
                if isinstance(qa[0], dict):
                    qa[0]["model"] = llm.model_name
                    qa_pairs.extend(qa)
            except Exception as e:
                print(e)
        qa_df = pd.DataFrame(qa_pairs)
        qa_df.to_csv(out_path,sep='|')
        print(f"{len(qa_pairs)} qa pairs generated")

    def evaluate_questions(self, qa_path:str ,out_path:str):
        """
        pass the generated questions trought the question answering object.

        Args:
            qa_path (str): The path to the generated question-answer pairs csv file.
            out_path (str): The path to save the question-answer + responses csv file.

        Returns:
            None
        """
        df_qa=pd.read_csv(qa_path, sep='|', index_col=0)
        df_qa["response"]=df_qa.progress_apply(lambda x: self.question_answering.answer(x.question)[0],axis=1)
        df_qa.to_csv(out_path,sep='|')
        

    def evaluate_responses(self, qar_path:str ,out_path:str, llm= ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo")):
        """
        Evaluates the responses against the answers and calculates LLM Based Evaluation Accuracy.
        Args:
            qar_path (str): The path to the question-answer pairs with responses csv file.
            out_path (str): The path to save the evaluation results csv file.
            llm: The language model to use for evaluation.

        Returns:
            None
        """
        eval_chain = QAEvalChain.from_llm(llm = llm, verbose=False)
        df_qar=pd.read_csv(qar_path, sep='|', index_col=0)
        qa_pairs=df_qar[["question","answer"]].to_dict("records")
        responses=df_qar["response"].reset_index().to_dict("records")
        graded_outputs=eval_chain.evaluate(examples = qa_pairs, 
                                           predictions = responses, 
                                           question_key= "question", 
                                           answer_key= "answer", 
                                           prediction_key= "response"
                                           )
        out_df=pd.concat([df_qar, pd.DataFrame(graded_outputs)], axis=1)
        out_df.to_csv(out_path,sep='|')
        total_corrects=out_df['results'].value_counts().get('CORRECT', 0)
        accuracy=total_corrects/len(out_df)
        print(f"LLM Based Evaluation Accuracy: {accuracy}")


if __name__ == '__main__':
    #set the docummet embedder object witout updating the vector db for making splitted in chunks documents
    sagemaker_document_embedder = DocumentEmbedder(knowledge_base="sagemaker_documentation")
    sagemaker_document_embedder.update_knowledge(store=False)
    #set the  question answer object for runing the question for evalation
    behavior = "You are the knowlegebase with the updated documentation of sagemaker tool \nQuestions are made by developers"
    sagemaker_question_answering = QuestionAnswering(sagemaker_document_embedder, behavior = behavior, verbose=False)
    #init evalation object
    sagemaker_model_evalaution=ModelEvaluation(sagemaker_document_embedder,sagemaker_question_answering)
    sagemaker_model_evalaution.generate_question_answer_pairs(
                                out_path=os.path.join("eval","sagemaker_qa_pairs.csv"), 
                                question_number=30
                                )
    sagemaker_model_evalaution.evaluate_questions(
                                 qa_path=os.path.join("eval","sagemaker_qa_pairs.csv"),
                                 out_path=os.path.join("eval","sagemaker_qa_responses.csv")
                                 )
    sagemaker_model_evalaution.evaluate_responses(
                                qar_path=os.path.join("eval","sagemaker_qa_responses.csv"),
                                out_path=os.path.join("eval","sagemaker_qa_responses_eval.csv")
                                )