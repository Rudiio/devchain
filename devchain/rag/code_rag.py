import os
import json

from pydantic import InstanceOf, Field

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import Language
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders import TextLoader

from devchain.rag.rag import Rag
from devchain.llm import load_Hugging_face_embeddings


class CodeRag(Rag):
    """Class that applies Retrival augmented generation especially for Code."""
    
    parser : InstanceOf[LanguageParser] = Field(default=None,description="Coding language parser")
    
    def setup_rag(self):
        """Sets up the rag components for the RAG system"""
        
        # Setup Embeddings model
        self.embeddings = load_Hugging_face_embeddings()
        
        # Setup vector database
        self.vector_db = Chroma(persist_directory=self.persist_directory,embedding_function=self.embeddings)
        
        # Setup retriever to avoir error
        self.retriever = self.vector_db.as_retriever(search_type='similarity',
                                                     search_kwargs={"k": 5})
        
        # Loading the index
        if os.path.exists(f'{self.persist_directory}/index.json'):
            with open(f'{self.persist_directory}/index.json','r+') as file:
                self.index = json.load(file)
        
    def load_documents(self, document_path: str):
        """Load the documents"""
        
        file = document_path.split('/')[-1]
        ext = document_path.split('.')[-1]
        chunk_size = 1000
        chunk_overlap = 200
        
        # Creating the document loader
        if ext=='py':
            self.loader = GenericLoader.from_filesystem(
                path=document_path,
                suffixes=[".py"],
                exclude=["**/non-utf8-encoding.py"],
                parser=LanguageParser(language=Language.PYTHON)
            )
            
            self.splitter = RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON,
                                                                         chunk_size=chunk_size,
                                                                         chunk_overlap=chunk_overlap)
            
        elif ext in ['html','css']:
            self.loader = TextLoader(file_path=document_path)
            self.splitter = RecursiveCharacterTextSplitter.from_language(language=Language.HTML,
                                                                         chunk_size=chunk_size,
                                                                         chunk_overlap=chunk_overlap,
                                                                         )
        elif ext == 'js':
            self.loader = TextLoader(file_path=document_path)
            self.splitter = RecursiveCharacterTextSplitter.from_language(language=Language.JS,
                                                                         chunk_size=chunk_size,
                                                                         chunk_overlap=chunk_overlap)
                                
            
        # Load the documents
        documents = self.loader.load()
        
        # Split documents
        documents = self.splitter.split_documents(documents=documents)
        texts = [doc.page_content for doc in documents]
        metadatas = [doc.metadata for doc in documents]
        
        # Checking is the file is already in the database
        if file in self.index:
            self.vector_db.delete(ids=self.index[file])
            self.index[file] = None
        
        # Add the text
        self.index[file] = self.vector_db.add_texts(texts=texts,metadatas=metadatas)
        
        # Turn db into retriever
        self.retriever = self.vector_db.as_retriever(search_type='similarity',
                                                     search_kwargs={"k": 5})
            
        # Saving the index
        with open(f'{self.persist_directory}/index.json','w+') as file:
            json.dump(self.index,file)
        
        
        
        
        
            
        
        
       
        
        