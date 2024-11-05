import unittest
from unittest.mock import Mock
from paddle.src.renderer import Renderer

class TestRenderer(unittest.TestCase):
    def setUp(self):
        pygame.display.set_mode = Mock()
        pygame.font.Font = Mock()
        self.renderer = Renderer((800, 600), Mock(), None, 20)

    def test_initialization(self):
        self.assertIsNotNone(self.renderer.screen)
        self.assertIsNotNone(self.renderer.font)
        self.assertIsNotNone(self.renderer.game_area_rect)

    def test_clear_screen(self):
        self.renderer.screen.fill = Mock()
        self.renderer.clear_screen()
        self.renderer.screen.fill.assert_called_once_with(pygame.Color('black'))

    def test_update_display(self):
        pygame.display.flip = Mock()
        self.renderer.update_display()
        pygame.display.flip.assert_called_once()

    def test_draw_paddle(self):
        paddle_mock = Mock()
        paddle_mock.get_rect.return_value = Mock()
        self.renderer.screen.fill = Mock()
        self.renderer.draw_paddle(paddle_mock)
        self.assertTrue(self.renderer.screen.fill.called)

    def test_draw_ball(self):
        ball_mock = Mock()
        ball_mock.x = 100
        ball_mock.y = 100
        ball_mock.radius = 10
        self.renderer.screen.fill = Mock()
        self.renderer.draw_ball(ball_mock)
        self.assertTrue(self.renderer.screen.fill.called)

    def test_draw_score(self):
        self.renderer.font.render = Mock()
        self.renderer.screen.blit = Mock()
        self.renderer.draw_score(3, 5)
        self.assertEqual(self.renderer.font.render.call_count, 2)
        self.assertEqual(self.renderer.screen.blit.call_count, 2)

    def test_draw_game_over_player_wins(self):
        self.renderer.font.render = Mock()
        self.renderer.screen.blit = Mock()
        self.renderer.draw_game_over("player")
        self.renderer.font.render.assert_called_once_with("You Win!", True, pygame.Color('white'))
        self.assertTrue(self.renderer.screen.blit.called)

    def test_draw_game_over_ai_wins(self):
        self.renderer.font.render = Mock()
        self.renderer.screen.blit = Mock()
        self.renderer.draw_game_over("AI")
        self.renderer.font.render.assert_called_once_with("You Lose!", True, pygame.Color('white'))
        self.assertTrue(self.renderer.screen.blit.called)

if __name__ == '__main__':
    unittest.main()
