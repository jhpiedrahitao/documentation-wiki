# Documentation-wiki

Documentation wiki, using LLMs and document retrieval methods for Question Answering
This project aims to develop a Documentation Assistance Tool to help Company X's developers find relevant information quickly within their documentation resources. The tool will utilize combining a large language model (LLM) with a document retrieval system (RAG), via langchain libary. The system will initially focus on a Proof of Concept (POC) to demonstrate its effectiveness in reducing the time developers spend searching through documentation. This tool aims to address these issues by providing developers with quick access to relevant information, reducing interruptions to experienced team members, and ensuring up-to-date documentation is always accessible.

## Components
1. **Document Embedder**: Split documents in chunks, vectorize them, and store them in a vector DB.
2. **Question Answering Document Retrieval**: Retrieve relevant documents using the vectorized user query and pass them trought the llm, giving an answer based on the retrieved documents.
3. **Document Updater**: Periodically search for update in source documents.
4. **API Service**: Deploys an API service for user interaction and integration into the development environment.
5. **User Interface**: Web based user interface for developers to interact with the tool.
6. **Evaluation Module**: Metrics and evaluation methods to measure the tool's effectiveness.

## Deployment
put your openai access token in the ```.env``` file (example in ```.env example``` file)  
For simple deployment of the docker containerized application execute the following commands  
```sh
./build.sh
./start.sh
```

## Usage
### User Interface
you can try the aplication via simple user interface after deploying  
[0.0.0.0:8888](http://0.0.0.0:8888)
### REST API
Uri: [0.0.0.0:5589/sagemaker](http://0.0.0.0:5589/sagemaker)  
Method: POST  
Data: "question":"your question here" (formdata)
### CURL
```sh
curl --location '0.0.0.0:5589/sagemaker' \
--form 'question="your question here"'
```

## Future Enhancements
