import os
from devchain.communication.document import Document
from devchain.utils.io import clean_folder

def test_clean_folder():
    """Test the ability to clean the folders"""
    
    clean_folder('tests/2048/backlog')
    clean_folder('tests/2048/requirements')
    
    assert len(os.listdir('tests/2048/backlog')) == 0
    assert len(os.listdir('tests/2048/requirements')) == 0

def test_save_backlog():
    """Tests the save_backlog function"""
    
    backlog = Document.load_file('tests/2048/backlog.md')
    
    Document.save_backlog(backlog=backlog,
                          working_dir='tests/2048/')
    
    assert len(os.listdir('tests/2048/backlog')) == 8
    assert len(os.listdir('tests/2048/requirements')) == 10
    
doc = Document.to_code(working_dir='tests/2048/')

def test_documents_load_backlog():
    """Test the ability of the system to load the backlog"""
    
    assert len(doc.title) > 0
    assert len(doc.user_request) > 0
    assert len(doc.user_stories) > 0
    assert len(doc.description) > 0
    assert len(doc.requirements) > 0

def test_documents_load_architecture():
    """Test the ability of the system to load the architecture"""
    
    assert isinstance(doc.stack,dict)
    assert 'backend' in doc.stack and 'frontend' in doc.stack
    
    assert 'erDiagram' in doc.erd
    assert len(doc.roles) > 0
    
def test_load_fixes():
    """Test the ability of the system to load fixes"""
    fixes = Document.load_fixes('tests/2048/misc/test_fixes.json')
    
    assert len(fixes) == 16