from pydantic import BaseModel, Field, InstanceOf

from langchain_core.vectorstores import VectorStore,VectorStoreRetriever
from langchain.text_splitter import TextSplitter
from langchain_core.embeddings import Embeddings
from langchain.document_loaders.base import BaseLoader
from langchain_core.runnables import RunnablePassthrough
from langfuse.callback import CallbackHandler

from devchain.utils.tracer import load_callback
class Rag(BaseModel):
    """Interface for Retrieval Augmented Generation (RAG) operations.
    It should be used to allow agents to index documents into the database and to retrieve context directly"""
    
    loader : InstanceOf[BaseLoader] = Field(default=None,description="Document loader")
    vector_db : InstanceOf[VectorStore] = Field(default=None,description="Vector database that stores the documents")
    retriever : InstanceOf[VectorStoreRetriever] = Field(default=None,description="Database retriever")
    splitter : InstanceOf[TextSplitter] = Field(default=None,description="Textsplitter")
    embeddings : InstanceOf[Embeddings] = Field(default=None,description="Text embeddings model")
    callback : InstanceOf[CallbackHandler] = Field(default_factory=load_callback,description="Langfuse callback for open source tracing")
    persist_directory : str = Field(default='',description="Directory in which save the vector db")
    index : dict[str,list] = Field(default={},description="Index of documents, associate a file to the corresponding ids")
    
    def setup_rag(self):
        """Sets up the rag components for the RAG system"""
        return NotImplementedError()
    
    def load_documents(self,document_path:str,index:str):
        """Load the document directly from a path"""
        return NotImplementedError()

    def invoke(self,query:str,search_type='similarity',k=5):
        """Retrieval part of the RAG."""
        self.retriever = self.vector_db.as_retriever(search_type=search_type,
                                                    search_kwargs={"k": k})
        
        chain = (self.retriever | RunnablePassthrough()).with_config({"run_name": "CodeRetriever"})
        
        return chain.invoke(query, config={"callbacks": [self.callback]})
    
    @property
    def retriever(self):
        """Sets property for the retriever"""
        return self.retriever
