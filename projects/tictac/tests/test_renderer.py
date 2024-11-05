import unittest
from unittest.mock import Mock
from projects.tictac.src.renderer import Renderer

class TestRenderer(unittest.TestCase):
    def setUp(self):
        # Mock the pygame module to avoid launching a GUI
        self.pygame_mock = Mock()
        self.screen_size = (300, 300)
        self.font_name = 'Arial'
        self.font_size = 20
        self.renderer = Renderer(self.screen_size, self.font_name, self.font_size)

    def test_initialization(self):
        self.assertIsNotNone(self.renderer.screen)
        self.assertIsNotNone(self.renderer.font)
        self.assertIsNone(self.renderer.game_board)

    def test_draw_board_without_game_board_set(self):
        with self.assertRaises(ValueError):
            self.renderer.draw_board()

    def test_get_cell_from_position(self):
        # Test for different positions on the screen
        test_cases = [
            ((0, 0), (0, 0)),
            ((150, 150), (1, 1)),
            ((299, 299), (2, 2)),
            ((300, 300), (2, 2)),  # Should be clamped to the max value
            ((-1, -1), (0, 0)),    # Should be clamped to the min value
        ]
        for position, expected in test_cases:
            with self.subTest(position=position):
                self.assertEqual(self.renderer.get_cell_from_position(position), expected)

    def test_clear_screen(self):
        # Mock the fill method to ensure it is called with white color
        self.renderer.screen.fill = Mock()
        self.renderer.clear_screen()
        self.renderer.screen.fill.assert_called_once_with((255, 255, 255))

    def test_update_display(self):
        # Mock the flip method to ensure it is called
        self.renderer.pygame_mock.display.flip = Mock()
        self.renderer.update_display()
        self.renderer.pygame_mock.display.flip.assert_called_once()

    def test_draw_status(self):
        # Mock the font rendering and blit to ensure they are called
        self.renderer.font.render = Mock(return_value=Mock(get_rect=Mock(return_value=Mock())))
        self.renderer.screen.blit = Mock()
        message = "Test Status"
        self.renderer.draw_status(message)
        self.renderer.font.render.assert_called_once_with(message, True, (0, 0, 0))
        self.assertTrue(self.renderer.screen.blit.called)

    def test_animate_symbol(self):
        # Mock the draw methods to ensure they are called with correct parameters
        self.renderer.pygame_mock.draw.line = Mock()
        self.renderer.pygame_mock.draw.circle = Mock()
        self.renderer.animate_symbol((1, 1), 'X')
        self.assertTrue(self.renderer.pygame_mock.draw.line.called)
        self.renderer.animate_symbol((1, 1), 'O')
        self.assertTrue(self.renderer.pygame_mock.draw.circle.called)

if __name__ == '__main__':
    unittest.main()
