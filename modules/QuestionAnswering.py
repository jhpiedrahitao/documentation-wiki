from dotenv import load_dotenv
import langchain
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
if __name__ == "__main__":
    from DocumentEmbedder import DocumentEmbedder

load_dotenv()

class QuestionAnswering:
    """
    QuestionAnswering is a class for answering via document retrieval from a Vector Database.

    Args:
        documentEmbedder (DocumentEmbedder): The documentEmbedder object used for storing documents to retrieve within the questions.
        verbose (bool): Whether or not log all langchain steps
        behavior (str, optional): String describing an aditionl behavior for the LLM to follow. Default is None 
        template (str, optional): The template to be used among the bahavior param, as Propmt template. Default is:
            '''Use the following pieces of context to answer the question at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            {context}, 
            
            Question: {question}
            Helpful Answer:
            '''
    Methods:
        set_retrieval(self, documents_amount: int = 3):
            Set the retriever to be used for question answering.

        answer(self, text: str):
            Returns the answer for a user query.
    """
    def __init__(self, documentEmbedder, documents_amount=5, behavior="", verbose=True,template="""
            Use the following pieces of context to answer the question at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            {context}, 
            
            Question: {question}
            Helpful Answer:
            """):
        """
        Initializes a QuestionAnswering object

        Args:
        documentEmbedder (DocumentEmbedder): The documentEmbedder object used for storing documents to retrieve within the questions.
        behavior (str, optional): String describing an aditionl behavior for the LLM to follow. Default is None 
        verbose (bool): Whether or not log all langchain steps
        template (str, optional): The template to be used among the bahavior param, as Propmt template. Default is:
            '''Use the following pieces of context to answer the question at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.
            {context}, 
            
            Question: {question}
            Helpful Answer:
            '''
        """        
        self.vector_db_path = documentEmbedder.output_folder_path 
        self.embeddings=documentEmbedder.embeddings
        self.verbose = verbose
        self.template = behavior + template
        self.llm= ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0) 
        self.documents_amount = documents_amount
        self.set_retrieval()
        langchain.debug = self.verbose

    def set_retrieval(self):
        """
        set the retriever to be used for question answering.

        Returns:
            None
        """
        vectorstore = FAISS.load_local(folder_path=self.vector_db_path, embeddings=self.embeddings)
        QA_CHAIN_PROMPT = PromptTemplate.from_template(self.template)
        self.qa = RetrievalQA.from_chain_type(llm=self.llm, 
                                     chain_type="stuff", 
                                     chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}, 
                                     retriever=vectorstore.as_retriever(search_type="similarity",search_kwargs={'k': self.documents_amount, 'lambda_mult': 0.5}),
                                     return_source_documents=True, 
                                     verbose=self.verbose
                                    )

    def answer(self, text:str):
        """Returns the answer for a user query
        
        Args:
            text (str): The question made by the user

        Returns:
            result (str): a string containing the answer for the question
            sources (List): a list of documents retrieved for answering the usr question
        """     
        sources=[]
        if text != "":
            result = self.qa({"query": text})
            for doc in result['source_documents']:
                sources.append(doc.metadata["source"])
            result = result["result"]
        else:
            result = "please write a Question"
        sources=list(set(sources))
        return result, sources  


if __name__ == "__main__":
    # Making a question given a DocumentEmbedder of a specific knowledge base  
    document_embedder = DocumentEmbedder("sagemaker_documentation")
    #documentEmbedder.update_knowledge()
    qa=QuestionAnswering(document_embedder)
    print(qa.answer("what is the folder structure when a model is trained"))

