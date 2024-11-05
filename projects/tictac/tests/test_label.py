import unittest
from unittest.mock import Mock
from projects.tictac.src.label import Label

class TestLabel(unittest.TestCase):
    def setUp(self):
        self.position = (100, 200)
        self.text = "Player X's turn"
        self.label = Label(self.position, self.text)

    def test_initialization(self):
        self.assertEqual(self.label.position, self.position)
        self.assertEqual(self.label.text, self.text)

    def test_set_text(self):
        new_text = "Player O's turn"
        self.label.set_text(new_text)
        self.assertEqual(self.label.text, new_text)

    def test_draw(self):
        # Create a mock renderer object
        mock_renderer = Mock()
        mock_renderer.font.render.return_value.get_rect.return_value = Mock(topleft=self.position)

        # Call the draw method with the mock renderer
        self.label.draw(mock_renderer)

        # Assert that the renderer's methods were called with the correct arguments
        mock_renderer.font.render.assert_called_once_with(self.text, True, (0, 0, 0))
        mock_renderer.screen.blit.assert_called()

if __name__ == '__main__':
    unittest.main()
