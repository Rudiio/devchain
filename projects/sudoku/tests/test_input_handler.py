import unittest
import pygame
from unittest.mock import patch
from sudoku.src.input_handler import InputHandler

class TestInputHandler(unittest.TestCase):
    def test_get_direction_up(self):
        key_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        direction = InputHandler.get_direction(key_event)
        self.assertEqual(direction, 'up')

    def test_get_direction_down(self):
        key_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        direction = InputHandler.get_direction(key_event)
        self.assertEqual(direction, 'down')

    def test_get_direction_left(self):
        key_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
        direction = InputHandler.get_direction(key_event)
        self.assertEqual(direction, 'left')

    def test_get_direction_right(self):
        key_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        direction = InputHandler.get_direction(key_event)
        self.assertEqual(direction, 'right')

    def test_get_direction_invalid_key(self):
        key_event = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_a)
        direction = InputHandler.get_direction(key_event)
        self.assertIsNone(direction)

    def test_get_direction_not_keydown_event(self):
        key_event = pygame.event.Event(pygame.KEYUP, key=pygame.K_RIGHT)
        direction = InputHandler.get_direction(key_event)
        self.assertIsNone(direction)

if __name__ == '__main__':
    unittest.main()
