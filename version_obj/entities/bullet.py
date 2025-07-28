import pygame

class Bullet:
    def __init__(self, x, y, speed, is_enemy=False):
        self.rect = pygame.Rect(x, y, 6, 12)
        self.speed = speed
        self.is_enemy = is_enemy

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface, image):
        surface.blit(image, self.rect)
