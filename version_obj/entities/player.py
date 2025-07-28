import pygame
from space_game.entities.bullet import Bullet

class Player:
    def __init__(self, x, y, speed, assets):
        self.rect = pygame.Rect(x, y, 50, 40)
        self.speed = speed
        self.bullets = []
        self.assets = assets
        self.last_shot = 0
        self.cooldown = 400
        self.lives = 3

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < 800:
            self.rect.x += self.speed

    def shoot(self, sound_manager):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.cooldown:
            bullet = Bullet(self.rect.centerx - 3, self.rect.y, -7)
            self.bullets.append(bullet)
            sound_manager.shot.play()
            self.last_shot = now

    def update_bullets(self):
        for b in self.bullets[:]:
            b.update()
            if b.rect.bottom < 0:
                self.bullets.remove(b)

    def draw(self, surface):
        surface.blit(self.assets.player, self.rect)
        for b in self.bullets:
            b.draw(surface, self.assets.bullet)