
from flask import Flask, request
import json
from flask_cors import CORS
from modules.DocumentEmbedder import DocumentEmbedder
from modules.QuestionAnswering import QuestionAnswering
from modules.utils.DocumentUpdater import documentUpdater

app = Flask(__name__)
CORS(app)

knowledge_base="sagemaker_documentation"
#documentUpdater.update_document_files_from_awsdocs(knowledge_base)
documentUpdater.update_document_files_from_awsdocs_mock(knowledge_base)
sagemaker_documentEmbedder = DocumentEmbedder(knowledge_base=knowledge_base)
#documentEmbedder.update_knowledge()
sagemaker_question_answering=QuestionAnswering(sagemaker_documentEmbedder)

@app.route("/sagemaker", methods=["POST"])
def sagemaker_question():
    question = request.form.get('question')
    answer, sources =sagemaker_question_answering.answer(question)
    return json.dumps({"answer":answer, "sources":sources})



