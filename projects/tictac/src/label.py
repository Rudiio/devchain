import pygame

class Label:
    def __init__(self, position, text):
        self.position = position
        self.text = text

    def draw(self, renderer):
        # Render the label text and blit it onto the screen at the specified position
        text_surface = renderer.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(topleft=self.position)
        renderer.screen.blit(text_surface, text_rect)
        # Removed the renderer.update_display() call

    def set_text(self, text):
        # Update the label text
        self.text = text
