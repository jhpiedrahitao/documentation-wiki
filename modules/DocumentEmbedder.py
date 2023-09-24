import os
from dotenv import load_dotenv
import langchain
from langchain.document_loaders import UnstructuredMarkdownLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

langchain.debug = True
load_dotenv()


class DocumentEmbedder:
    """
    DocumentEmbedder is a class for loading, splitting, embedding, and storing documents in a Vector Database.

    Args:
        knowledge_base (str): The name path of the knowledge base.
        documents_path (str, optional): The path to the directory containing RAW knowledge base. Default is "Documents".
        output_path (str, optional): The path to the directory where the vectorized documents will be stored. Default is "Storage".
        embeddings (langchain embedding, optional): The embedding to use to vectorize documents.

    Methods:
        load_txt(self, path: str):
            Load a text document from a file.

        load_md(self, path: str):
            Load a markdown document from a file.

        split_documents(self, documents, chunk_size: int = 1000, chunk_overlap: int = 200):
            Split long documents into smaller chunks.

        vectorize_and_store(self):
            Vectorize the documents and store them using FAISS vector store.

        update_knowledge(self):
            Update the knowledge base by loading, splitting, vectorizing, and storing documents.

    """
    def __init__(self, knowledge_base: str, documents_path: str = "Documents", output_path: str = "Storage", embeddings = OpenAIEmbeddings()):
        """
        Initializes a DocummentEmbedder object
        
        Args:
            knowledge_base (str): The name path of the knowledge base.
            documents_path (str, optional): The path to the directory containing RAW knowledge base. Default is "Documents".
            output_path (str, optional): The path to the directory where the vectorized documents will be stored. Default is "Storage".
            embeddings (langchain embedding, optional), embedding to use to vectorize documents 
        """           
        self.knowledge_base = knowledge_base
        self.documents_path = documents_path
        self.output_folder_path = os.path.join(output_path, self.knowledge_base)
        self.documents = []
        self.embeddings = embeddings


    def load_txt(self, path: str):
        """
        Load a text document from a file.

        Args:
            path (str): The path to the text document file.

        Returns:
            list: a Langchain Document object containing the loaded document.
        """
        loader = TextLoader(file_path=path)
        document = loader.load()
        return document

    def load_md(self, path: str):
        """
        Load a markdown document from a file.

        Args:
            path (str): The path to the text document file.

        Returns:
            list: a Langchain Document object containing the loaded document.
        """
        loader = UnstructuredMarkdownLoader(file_path=path)
        document = loader.load()
        return document

    def split_documents(self, documents, chunk_size: int = 1000, chunk_overlap: int =200):
        """
        Split long documents into smaller chunks.

        Args:
            documents (list): A list of langchain documents.
            chunk_size (int, optional): desired size of splitted documents . Default is 1000
            chunk_overlap (int, optional): desired size of overlap betwen splitted documents . Default is 200

        Returns:
            list: A list of smaller document chunks.
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size, 
            chunk_overlap=chunk_overlap, 
            separators=["\n\n", "\n"]
        )
        print(type(documents[0]))
        documents = text_splitter.split_documents(documents=documents)
        return documents

    def vectorize_and_store(self):
        """
        Vectorize the documents and store them using FAISS vector store.

        Returns:
            None
        """
        embeddings = self.embeddings
        print(f"{len(self.documents)} documents will be stored")
        vectorstore = FAISS.from_documents(
            documents=self.documents, embedding=embeddings
        )
        vectorstore.save_local(os.path.join(self.output_folder_path))

    def update_knowledge(self, store=True):
        """
        Update the knowledge base by loading, splitting, vectorizing, and storing documents.

        Args:
            store (Bool, optional): Whether to vectorize and store or not 

        Returns:
            Boolean: True after successful update
        """
        files = os.listdir(os.path.join(self.documents_path, self.knowledge_base))
        for file in files:
            document = None
            if ".md" == file[-3:]:
                document = self.load_md(
                    os.path.join(self.documents_path, self.knowledge_base, file)
                )
            elif ".txt" == file[-4:]:
                document = self.load_txt(
                    os.path.join(self.documents_path, self.knowledge_base, file)
                )
            else:
                print(
                    f"File {file} can't be loaded, loader for {file[-3:]} extension not implemented"
                )
            if document:
                self.documents += document
        self.documents = self.split_documents(self.documents)
        if store:
            self.vectorize_and_store()
        return(True)


if __name__ == "__main__":
    # Create an instance of DocumentEmbedder for a specific knowledge base and update the knowledge base
    document_embedder = DocumentEmbedder("sagemaker_documentation")
    document_embedder.update_knowledge()