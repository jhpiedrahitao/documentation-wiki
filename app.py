import os
import json
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from modules.DocumentEmbedder import DocumentEmbedder
from modules.QuestionAnswering import QuestionAnswering
from modules.utils.DocumentUpdater import documentUpdater


app = Flask(__name__)
CORS(app)

STREAMLIT_APP_URL = "/streamlit_app"

knowledge_base="sagemaker_documentation"
#documentUpdater.update_document_files_from_awsdocs(knowledge_base)
documentUpdater.update_document_files_from_awsdocs_mock(knowledge_base)
sagemaker_documentEmbedder = DocumentEmbedder(knowledge_base=knowledge_base)
#sagemaker_documentEmbedder.update_knowledge()
behavior = "You are the knowlegebase with the updated documentation of sagemaker tool \nQuestions are made by developers"
sagemaker_question_answering = QuestionAnswering(sagemaker_documentEmbedder, behavior=behavior)

@app.route("/update_knowledge", methods=["POST"])
def updateknowledge():
    #Updating endpoit, calls method for fetching changes in documents and update vector database
    #documentUpdater.update_document_files_from_awsdocs(knowledge_base)
    documentUpdater.update_document_files_from_awsdocs_mock(knowledge_base)
    sagemaker_documentEmbedder.update_knowledge()
    global sagemaker_question_answering
    sagemaker_question_answering = QuestionAnswering(sagemaker_documentEmbedder, behavior=behavior)
    return True

@app.route("/sagemaker", methods=["POST"])
def sagemaker_question():
    #simple enpoint for question answering with question in formdata
    question = request.form.get('question')
    answer, sources =sagemaker_question_answering.answer(question)
    return json.dumps({"answer":answer, "sources":sources})

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    #simple endpoint for retrieving documents
    directory = os.path.join('Documents',knowledge_base)
    return send_from_directory(directory, filename)




