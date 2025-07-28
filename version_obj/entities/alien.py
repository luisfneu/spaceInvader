import pygame
import random
from space_game.entities.bullet import Bullet

class Alien:
    def __init__(self, x, y, assets):
        self.rect = pygame.Rect(x, y, 40, 30)
        self.assets = assets

    def draw(self, surface):
        surface.blit(self.assets.alien, self.rect)

class AlienManager:
    def __init__(self, rows, cols, assets):
        self.aliens = []
        self.assets = assets
        self.direction = 1
        self.speed = 1.5
        self.enemy_bullets = []
        self.last_fire_time = pygame.time.get_ticks()
        self.fire_delay = 800

        for row in range(rows):
            for col in range(cols):
                x = 80 + col * 60
                y = 50 + row * 40
                self.aliens.append(Alien(x, y, assets))

    def update(self):
        move_down = False
        for alien in self.aliens:
            alien.rect.x += self.speed * self.direction
            if alien.rect.right >= 800 or alien.rect.left <= 0:
                move_down = True

        if move_down:
            self.direction *= -1
            for alien in self.aliens:
                alien.rect.y += 20

        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.rect.top > 600:
                self.enemy_bullets.remove(bullet)

    def draw(self, surface):
        for alien in self.aliens:
            alien.draw(surface)
        for bullet in self.enemy_bullets:
            bullet.draw(surface, self.assets.bullet_alien)

    def try_shoot(self):
        now = pygame.time.get_ticks()
        if self.aliens and now - self.last_fire_time > self.fire_delay:
            shooter = random.choice(self.aliens)
            bullet = Bullet(shooter.rect.centerx, shooter.rect.bottom, 6, is_enemy=True)
            self.enemy_bullets.append(bullet)
            self.last_fire_time = now