import pygame

class Explosion:
    def __init__(self, rect, duration=200):
        self.rect = rect
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

    def is_active(self):
        return pygame.time.get_ticks() - self.start_time < self.duration

    def draw(self, surface, image):
        if self.is_active():
            surface.blit(image, self.rect)
