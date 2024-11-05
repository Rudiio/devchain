import pygame

class Button:
    def __init__(self, position, size, text, on_click):
        self.position = position
        self.size = size
        self.text = text
        self.on_click = on_click
        self.rect = pygame.Rect(position, size)

    def draw(self, renderer):
        # Draw the button rectangle
        pygame.draw.rect(renderer.screen, (200, 200, 200), self.rect)
        
        # Draw the button text
        text_surface = renderer.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        renderer.screen.blit(text_surface, text_rect)

    def is_hovered(self, position):
        # Check if the mouse is over the button
        return self.rect.collidepoint(position)

    def click(self):
        # Call the on_click function if it exists
        if callable(self.on_click):
            self.on_click()
