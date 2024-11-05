import unittest
from unittest.mock import patch
from paddle.src.main import Main

class TestMain(unittest.TestCase):
    def setUp(self):
        # Patching pygame.init and pygame.quit to avoid initializing the GUI
        self.init_patch = patch('pygame.init')
        self.quit_patch = patch('pygame.quit')
        self.init_patch.start()
        self.quit_patch.start()
        self.main = Main()

    def tearDown(self):
        self.init_patch.stop()
        self.quit_patch.stop()

    def test_initialization(self):
        self.assertTrue(self.main.running)
        self.assertIsNotNone(self.main.game)
        self.assertIsNotNone(self.main.renderer)
        self.assertIsNotNone(self.main.clock)

    @patch('pygame.key.get_pressed')
    def test_handle_events_up_key(self, mock_get_pressed):
        mock_get_pressed.return_value = {pygame.K_UP: True}
        initial_y = self.main.game.player_paddle.y
        self.main.handle_events()
        self.assertLess(self.main.game.player_paddle.y, initial_y)

    @patch('pygame.key.get_pressed')
    def test_handle_events_down_key(self, mock_get_pressed):
        mock_get_pressed.return_value = {pygame.K_DOWN: True}
        initial_y = self.main.game.player_paddle.y
        self.main.handle_events()
        self.assertGreater(self.main.game.player_paddle.y, initial_y)

    @patch('pygame.event.get')
    def test_handle_events_quit(self, mock_get_events):
        mock_get_events.return_value = [pygame.event.Event(pygame.QUIT)]
        self.main.handle_events()
        self.assertFalse(self.main.running)

    def test_update_game_over(self):
        self.main.game.player_score = 10
        self.main.update()
        self.assertFalse(self.main.running)

    @patch('generated_project.src.renderer.Renderer.draw_game_over')
    def test_render_game_over(self, mock_draw_game_over):
        self.main.game.player_score = 10
        self.main.render()
        mock_draw_game_over.assert_called_once_with("player")

    @patch('generated_project.src.renderer.Renderer.draw_score')
    def test_render_score(self, mock_draw_score):
        self.main.game.player_score = 5
        self.main.game.ai_score = 3
        self.main.render()
        mock_draw_score.assert_called_once_with(5, 3)

if __name__ == '__main__':
    unittest.main()
