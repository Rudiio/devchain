import esprima.error_handler
from pydantic import Field, InstanceOf
from typing import Union
import esprima
import glob
import ast
import escodegen

from langfuse.callback import CallbackHandler

from devchain.rag.rag import Rag
from devchain.communication.document import Document


class CodeContextRetriever(Rag):
    """Code context retriever for Code generation. It load the documents, parses them and retrieve the right ones."""
    callback : InstanceOf[CallbackHandler] = Field(default=None,description="Langfuse callback for open source tracing")
    store : dict = Field(default={},description="Map the functions to their actual code")
    file_store : dict = Field(default={},description="Map the files to their direct code")
    classes_stores : dict = Field(default={},description="Map the classes to their direct code")
    working_dir : str = Field(default='',description="Path the working directory of the project")
    
    def setup_rag(self):
        
        # Load the files from the src folder
        files = glob.glob(f'{self.working_dir}/src/**/*.*',recursive=True)
        
        # filtering the list
        files = [file.replace('//','/') for file in files if ('__pycache__' not in file and '__init__' not in file)]
        
        # Load each file in the index
        for file in files:
            self.file_store[file] = Document.load_file(file)
            self.store[file] = {}
            
        # Parse each file
        for file in self.file_store:
            self.parse_file(file)
        
    def parse_file(self,file):
        """Parse the code according to the programmin language"""
        
        ext = file.split('.')[-1]
        
        if ext == 'py':
            self.extract_python(file)
        elif ext =='js' or ext=='jsx':
            self.extract_js(file)
        else:
            self.store[file] = {}
        
    def extract_python(self,file:str):
        """Extract the functions and classes from the python code and populate the store"""
        code = self.file_store[file]
        parsed = ast.parse(code)
        
        # Finding the classes
        classes = [node for node in ast.walk(parsed) if isinstance(node,(ast.ClassDef))]
        
        # Finding the methods
        for cls in classes:
            # Initializating the class in the store
            if cls.name not in self.store[file]:
                self.store[file][cls.name] = {}
            # Adding the class code in the store
            self.classes_stores[cls.name] = ast.unparse(cls)

            # Iterating over the other nodes to find the functions
            for node in ast.walk(cls):
                if isinstance(node, (ast.FunctionDef,ast.AsyncFunctionDef)):
                    function_name = node.name
                    function_code = ast.unparse(node)
                    
                    # Adding the code into the store
                    if function_name not in self.store[file][cls.name]:
                        self.store[file][cls.name][function_name] = function_code

    def extract_js(self,file:str):
        """Extract the functions from the javascript code and populate the store"""
        
        code = self.file_store[file]
        # Esprima to parse javascript code + escodegen to get the code back at a certain node
        try:
            parsed_code = esprima.parseModule(code,{'jsx':True})
        except esprima.error_handler.Error: # Parsing error
            try:
                parsed_code = esprima.parseScript(code,{'jsx':True})
            except esprima.error_handler.Error:
                print("Not able to parse, only the entire code will be indexed")
                return            
        
        # Exploring the ast to find the classes
        classes = [node for node in parsed_code.body if node.type == 'ClassDeclaration']
        for cls in classes:
            # Initializating the class in the store
            if cls.id.name not in self.store[file]:
                self.store[file][cls.id.name] = {}
            # Adding the class code in the store
            self.classes_stores[cls.id.name] = escodegen.generate(cls)
            
            # Iterating over the other nodes to find the functions
            for node in cls.body.body:
                if node.type == 'MethodDefinition':
                    function_name = node.key.name
                    function_code = escodegen.generate(node)
                    
                    # Adding the code into the store
                    if function_name not in self.store[file][cls.id.name]:
                        self.store[file][cls.id.name][function_name] = function_code
                
    def load_documents(self, document_path: str):
        """Load the documents"""
        document_path = document_path.replace('//','/')
        self.store[document_path] = {}
        self.file_store[document_path] = Document.load_file(document_path)
        self.parse_file(document_path)
    
    def dump(self,)->str:
        """Dump the code definitions into a string"""
        dump = ''
        # Formatting the dump
        for file in self.store:
            dump += f"`{file}`:\n"
            for cls in self.store[file]:
                dump += f"\tclass {cls}\n"
                # for func in self.store[file][cls]:
                #     dump += f"\t\t- function {func}\n"
            # dump += '\n'
        return dump
    
    def invoke(self,queries:Union[str,list],k:int=5,file_path:str='') -> str:
        """Extract the needed code context from the other files"""
        
        context = ""
        pre_path = f'{self.working_dir}/src/'.replace('//','/')
        
        for query in queries:
            parsed = query.split('::')
            
            # Converting to a list
            if not isinstance(parsed,list):
                parsed = [parsed]
            
            # Normalizing the file_path
            if pre_path not in file_path:
                file_path = (pre_path + file_path).replace('//','/')
            
            # Checking if the query already contain the pre-path + normalization if not
            if pre_path not in parsed[0]:
                file = (pre_path + parsed[0]).replace('//','/')
            else:
                file = parsed[0]
        
            if not file==file_path:
                # Format was : file::class::function
                if len(parsed)==3:
                    cls = parsed[1] 
                    func = parsed[2]
                    
                    # Getting the code
                    if file in self.store:
                        if cls in self.store[file]:
                            # Getting directly the correct functions
                            if func in self.store[file][cls]:
                                context += f"```{file}\n{self.store[file][cls][func]}```\n\n"
                            # Fallback : getting the class instead
                            else:
                                context += f"```{file}\n{self.classes_stores[cls]}```\n\n"
                        # Fallback : Verifying if the class exists even if it is in another file
                        elif cls in self.classes_stores:
                            context += f"```{file}\n{self.classes_stores[cls]}```\n\n"
                        # Fallback : getting the file content instead
                        else:
                            context += f"```{file}\n{self.file_store[file]}```\n\n"
                    else:
                        print("error when trying to retrieve code context : len=3")
                
                # Format was : file::function or file::class
                elif len(parsed)==2:
                    second = parsed[1]
                  
                    # Getting the code
                    if file in self.store:
                        # checking if the class/function is in the file (second = class)
                        if second in self.store[file]:    
                            # Checking if it is a class
                            if second in self.classes_stores:
                                context += f"```{file}\n{self.classes_stores[second]}```\n\n"
                            # It is supposed to be a file
                            else:
                                context += f"```{file}\n{self.store[file][second]}```\n\n"
                        # Fallback : second is not in file, checking if it is an existing class
                        elif second in self.classes_stores:
                            context += f"```{file}\n{self.classes_stores[second]}```\n\n"
                        # Fallback : second is not an existing class, copying the code file.
                        else:
                            context += f"```{file}\n{self.file_store[file]}```\n\n"
                    else:
                        print("error when trying to retrieve code context : len=2")
         
                # Format was : file
                # TODO : implement a code merger
                elif len(parsed)==1:
                    if file in self.store:
                        context += f"```{file}\n{self.file_store[file]}```\n\n"
                    else:
                        print("error when trying to retrieve code context : len=1")

        if context !="":    
            return "# Code Context\nUse these codes to understand how to solve your task.\n" + context
        return ''
        
        
        
        
        