from devchain.rag.code_context_retriever import CodeContextRetriever

rag = CodeContextRetriever(working_dir='tests/2048')

def test_setup_rag():
    """Test the setup_rag function"""
    rag.setup_rag()
    
    assert len(rag.store) == 6
    assert 'tests/2048/src/game_board.py' in rag.store
    assert 'tests/2048/src/game_logic.py' in rag.store
    assert 'tests/2048/src/input_handler.py' in rag.store
    assert 'tests/2048/src/main.py' in rag.store
    assert 'tests/2048/src/score_manager.py' in rag.store
    assert 'tests/2048/src/ui_manager.py' in rag.store

def test_classes():
    """Test if all the classes are found"""
    
    assert 'GameBoard' in rag.store['tests/2048/src/game_board.py']
    assert 'GameLogic' in rag.store['tests/2048/src/game_logic.py']
    assert 'InputHandler' in rag.store['tests/2048/src/input_handler.py']
    assert 'ScoreManager' in rag.store['tests/2048/src/score_manager.py']
    assert 'UIManager' in rag.store['tests/2048/src/ui_manager.py']

def test_functions():
    """Test if all the functions are found"""
    
    assert len(rag.store['tests/2048/src/game_board.py']['GameBoard']) == 12
    assert len(rag.store['tests/2048/src/game_logic.py']['GameLogic']) == 8
    assert len(rag.store['tests/2048/src/input_handler.py']['InputHandler']) == 4
    assert len(rag.store['tests/2048/src/score_manager.py']['ScoreManager']) == 4
    assert len(rag.store['tests/2048/src/ui_manager.py']['UIManager']) == 9
                                       
def test_invoke_1():
    """Test invoking CCR"""
    
    queries = ['main.py','ui_manager.py::UIManager']
    
    context = rag.invoke(queries)
    
    assert 'class UIManager' in context
    assert 'initialize_game()' in context
    
    
    