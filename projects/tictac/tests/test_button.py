import unittest
from unittest.mock import Mock
from projects.tictac.src.button import Button

class TestButton(unittest.TestCase):
    def setUp(self):
        self.mock_renderer = Mock()
        self.mock_renderer.screen = Mock()
        self.mock_renderer.font = Mock()
        self.mock_renderer.font.render.return_value.get_rect.return_value = Mock(center=(50, 50))
        self.on_click_called = False
        def on_click():
            self.on_click_called = True
        self.button = Button((0, 0), (100, 100), "Test", on_click)

    def test_initialization(self):
        self.assertEqual(self.button.position, (0, 0))
        self.assertEqual(self.button.size, (100, 100))
        self.assertEqual(self.button.text, "Test")
        self.assertTrue(callable(self.button.on_click))

    def test_draw(self):
        self.button.draw(self.mock_renderer)
        self.mock_renderer.screen.blit.assert_called_once()
        self.mock_renderer.font.render.assert_called_with("Test", True, (0, 0, 0))

    def test_is_hovered_true(self):
        self.assertTrue(self.button.is_hovered((50, 50)))

    def test_is_hovered_false(self):
        self.assertFalse(self.button.is_hovered((150, 150)))

    def test_click(self):
        self.button.click()
        self.assertTrue(self.on_click_called)

if __name__ == '__main__':
    unittest.main()
