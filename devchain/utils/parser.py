import re
import yaml
import pathlib
from typing import Union

from pydantic import BaseModel, Field

class DocumentParser(BaseModel):
    """Parse a string with a Document/Markdown formatting into a document object"""
    
    path : Union[str,pathlib.Path] = Field(default='',description="Path to the file to parse")
    document : str = Field(description="Document to parse in the right format",default='')
    parsed_document : dict = Field(default={},description="Parsed document")
    
    def load_file(self,path)->None:
        """ Load the file"""
        try:
            with open(path,'r+') as file:
                self.document = file.read()
        except ValueError:
            print("The path is not correct.")
    
    def parse_headers(self,level=1,doc='',max_level:int=3)->dict:
        """Parse the file headers based on the headers and create a deterministic tree to access each section."""
        
        header_pattern = f'(^|\n+)(#{{{level}}}\s)(.*)'
        
        # Finding the headers
        matches = [(m.start(),m.end()) for m in re.finditer(header_pattern,doc)]
       
        # Stopping criterion level=6
        if level==max_level:
            return doc
        
        if len(matches)==0:
            return self.parse_headers(level=level+1,doc=doc,max_level=max_level)
        
        parsed_document = {}
        # Processing each header 
        for m in range(0,len(matches)):
            h = matches[m]
            sub_string = doc[h[0]:h[1]]
            title = (re.findall('[^#*\n](.*)',sub_string)[0]).replace(' ','_')
            if m == len(matches)-1:
                child_document = doc[h[1]+1:]
            else:
                child_document = doc[h[1]+1:matches[m+1][0]]
            parsed_document[title] = self.parse_headers(level=level+1,doc=child_document,max_level=max_level)
        
        return parsed_document
    
    def parse_ordered_list(self,string:str) -> list[str]:
        """Parse an ordered list using regex"""
        # Regex explanations
        # ^: Asserts the position at the start of a line (because of the re.MULTILINE flag).
        # (\d+)\.: Captures one or more digits followed by a literal period (the item number).
        # \s+: Matches one or more whitespace characters.
        # (.*?): Lazily captures any character (including line terminators because of the re.DOTALL flag) zero or more times (the item text).
        # (?=\n\d+\.|\Z): Positive lookahead that asserts the position is followed by a newline and a digit-period sequence for the next list item or the end of the string (\Z).
        pattern =  re.compile(r'^\d+\.\s+(.*?)(?=\n\d+\.|\Z)', re.MULTILINE | re.DOTALL)
        ol = pattern.findall(string=string)
        return ol
    
    @staticmethod
    def get_precise_class_diagram(file:str,class_diagram:str)->str:
        """Extract the precise class from a class diagram in a mermaid class diagram"""
        
        try:
            cls = (file.split('.')[0]).replace('_','')
            pattern = re.compile(f'class\s*{cls}\s*' + r'\{([^\}]*)\}',flags=re.DOTALL)
            class_context = pattern.search(class_diagram).group(0)
            return class_context
        except AttributeError:
            return file
        
    @staticmethod
    def parse_code(string:str) -> str:
        """Parse a code by using regular expressions"""
        
        # Finding the triple backticks
        matchs = [(match.start(),match.end()) for match in re.finditer('```', string)]
        
        # Finding the first backline
        back = string[matchs[0][1]:].find('\n')
        
        # Parsing
        # programming_language = string[matchs[0][1]:matchs[0][1]+back]
        code = string[matchs[0][1]+back+1:matchs[1][0]]
        
        return code
    
    @staticmethod
    def parse_python_list(python_list:str) -> list[str]:
        """Parse a python list from string format to list format"""
        
        # Converting the string to list
        python_list = python_list.replace('[','').replace(']','').replace('\n','')
        python_list = python_list.replace("'",'')
        python_list = python_list.replace('"','')
        python_list = python_list.replace(' ','')
        python_list = python_list.split(',')
        
        if python_list == ['']:
            return []
        
        return python_list
    
    @staticmethod
    def parse_backlog(backlog:str) -> dict:
        """ Parse the backlog produced by the product owner.
        
        Arguments:
            backlog(str): the backlog produced by the product owner. It contains the user stories, the requirements and the title.
                        It follows mainly the markdown syntax.
        
        Return:
            deliverable(dict): the parsed backlog
            """
        
        # Parsing the application name
        title = re.search("# ",backlog)
        _,t_start = title.span()
        
        # Parsing the second title
        back = re.search("## Product Backlog:",backlog)
        t_end,_ = back.span()
        
        # Finding the user stories span 
        user_stories = re.search("### User stories",backlog)
        _,us_end = user_stories.span()
        
        # Finding the requirements span 
        requirements = re.search("### Requirements",backlog)
        r_start,r_end = requirements.span()
        
        title = backlog[t_start:t_end-2]
        user_stories = backlog[us_end+2:r_start]
        requirements = backlog[r_end+2:]
        
        return {'title':title,'user_stories':user_stories, 'requirements':requirements}

    @staticmethod
    def parse_design(design:str) -> dict:
        """ Parse the design file produced by the agent software architect
        
        Arguments:
            design(str): the design produced by the software architect. It contains the technical stack,
                        the design and the class diagram.
        
        Return:
            deliverable(dict): the parsed design file
        """
        
        # Finding the stack
        try:
            stack = re.search('(#*) Stack selection',design)
            if stack is None:
                stack = re.search('## Stack Selection',design)
            _,s_end = stack.span()
        except ValueError:
            _,s_end = 0,0
            
        # Finding the design
        try:
            dsg = re.search('(#*) Design',design)
            d_start,d_end = dsg.span()
        except ValueError:
            d_start,d_end = 0,0
        
        # Finding the class Diagram
        try:
            clsd  = re.search('(#*) Class diagram',design)
            if clsd is None:
                clsd  = re.search('(#*) Class Diagram',design)
            c_start,_ = clsd.span()
        except ValueError:
            c_start,_ = 0,0
        
        ## Finding the list of files 
        files = re.search("(#*) Files list",design)
        f_start,_ = files.span()
        
        ## Finding the dependencies
        dep = re.search("(#*) Routes, variables, and dependencies",design)
        _,dep_end = dep.span()
        
        pattern = re.compile('\[(.*?)\]')
        files_list = pattern.findall(design[f_start:])
        files_list = files_list[0].replace(' ','').split(sep=',')
        file_assignment = design[f_start+1:]
        
        stack = design[s_end:d_start]
        dsg = design[d_end+1:c_start]
        
        cls = design[design.find('```mermaid') + len('```mermaid')+1 : design.find('``` ')]
        full_design = dsg + f"```mermaid\n{cls}\n```"
        
        dep = design[dep_end+1:]
        
        return {'stack':stack,
                'design':full_design,
                'class_diagram':cls,
                'files_list':files_list,
                'files_description':file_assignment,
                'dependencies':dep}    

    @staticmethod
    def parse_stack(stack:str) -> dict:
        """Parse the stack written by the Software architect."""
        stack = yaml.safe_load(stack)
        return stack

    @staticmethod
    def parse_code_old(doc:str) -> dict:
        """Parse the string containing the code outputed by the developper."""
        
        # Finding the triple backticks
        matchs = [(match.start(),match.end()) for match in re.finditer('```', doc)]
        
        # Finding the first backline
        back = doc[matchs[0][1]:].find('\n')
        
        # Parsing
        programming_language = doc[matchs[0][1]:matchs[0][1]+back]
        code = doc[matchs[0][1]+back+1:matchs[1][0]]
        
        return {'code':code,'programming_language':programming_language}

    @staticmethod
    def parse_dev_feedback(feedback:str) -> dict:
        """Parse the string containing the feedback given by the developper when executing its code"""
        
        def str_to_bool(string:str):
            if string=='True':
                return True
            return False
        
        # Finding status with error handling
        try:
            passing = re.search('(#*) Need to correct',feedback)
            p_start,p_end = passing.span()
            endline = feedback[p_end+1:].find("\n")
            if endline== -1:
                endline = len(feedback)-1
            status = feedback[p_end+1:p_end + endline]
        except Exception:
            status = 'False'
            p_start,p_end = None,None
            
        # Finding the actual feedback
        feed = re.search('(#*) Review',feedback)
        _,feed_end = feed.span()
        
        try:
            feedbach = feedback[feed_end+1:p_start-1]
        except ValueError:
            feedbach = feedback[feed_end+1:]
        
        return {'status':str_to_bool(status),'feedback':feedbach}

    @staticmethod
    def parse_tests(tests:str)->dict:
        """Parse the string containing the tests"""
        
        # Finding the triple backticks
        matchs = [(match.start(),match.end()) for match in re.finditer('```', tests)]
        
        # Finding the first backline
        back = tests[matchs[0][1]:].find('\n')
        tt = tests[matchs[0][1] + back+1:matchs[1][0]]
        
        return tt 
    
    @staticmethod
    def parse_tests_feedback(feedback:str) -> dict:
        """Parse the string containing the feedback given by the developper when executing its code"""
        
        # Finding the tests status
        test_status = re.search('(#*) Tests need to be corrected?',feedback)
        p_start,p_end = test_status.span()
        backline = feedback[p_start:].find("\n")
        if backline==-1:
            backline=len(feedback)-1
        test_status = feedback[p_end+1:p_start + backline]
        
        # Finding the code status
        code_status = re.search('(#*) Code need to be corrected?',feedback)
        p_start,p_end = code_status.span()
        backline = feedback[p_start:].find("\n")
        if backline==-1:
            backline=len(feedback)-1
        test_status = feedback[p_end+1:p_start + backline]
        
        # Finding the actual feedback
        feed = re.search('### Review',feedback)
        feed_start,feed_end = feed.span()
        
        feedbach = feedback[feed_end+1:p_start-1]
        
        return {'tests_status':test_status,
                'code_status':code_status,
                'feedback':feedbach}
