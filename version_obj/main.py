import pygame, sys
from space_game.config import WIDTH, HEIGHT, FPS
from space_game.assets import AssetManager, SoundManager
from space_game.entities.player import Player
from space_game.entities.alien import AlienManager
from space_game.entities.explosion import Explosion
from space_game.menu import MainMenu

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Space Shooter")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 40)
        self.assets = AssetManager()
        self.sounds = SoundManager()
        self.player = Player(WIDTH // 2 - 25, HEIGHT - 60, 5, self.assets)
        self.alien_manager = AlienManager(5, 8, self.assets)
        self.explosions = []
        self.score = 0
        self.running = True
        self.game_over = False
        self.winner = False
        self.end_shown = False

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        keys = pygame.key.get_pressed()
        if not self.game_over:
            self.player.move(keys)
            if keys[pygame.K_SPACE]:
                self.player.shoot(self.sounds)
        elif keys[pygame.K_r]:
            self.__init__()

    def update(self):
        if self.game_over:
            return

        self.player.update_bullets()
        self.alien_manager.update()
        self.alien_manager.try_shoot()

        for bullet in self.player.bullets[:]:
            for alien in self.alien_manager.aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    self.player.bullets.remove(bullet)
                    self.alien_manager.aliens.remove(alien)
                    self.explosions.append(Explosion(alien.rect.copy()))
                    self.score += 10
                    # self.sounds.explosion_a.play()
                    break

        for bullet in self.alien_manager.enemy_bullets[:]:
            if bullet.rect.colliderect(self.player.rect):
                self.alien_manager.enemy_bullets.remove(bullet)
                self.player.lives -= 1
                self.explosions.append(Explosion(self.player.rect.copy()))
                self.sounds.explosion.play()
                if self.player.lives <= 0:
                    self.game_over = True
                    self.winner = False

        if not self.alien_manager.aliens:
            self.game_over = True
            self.winner = True

    def draw(self):
        self.screen.blit(self.assets.background, (0, 0))
        self.player.draw(self.screen)
        self.alien_manager.draw(self.screen)

        for explosion in self.explosions[:]:
            if explosion.is_active():
                explosion.draw(self.screen, self.assets.explosion)
            else:
                self.explosions.remove(explosion)

        self.screen.blit(self.font.render(f"Score: {self.score}", True, (255, 255, 255)), (10, 10))
        self.screen.blit(self.font.render(f"Lives: {self.player.lives}", True, (255, 255, 255)), (WIDTH - 150, 10))

        if self.game_over and not self.end_shown:
            msg = "WINNER" if self.winner else "SE FODEU"
            color = (0, 255, 0) if self.winner else (255, 0, 0)
            self.sounds.win.play() if self.winner else self.sounds.dead.play()
            text = self.font.render(msg, True, color)
            retry = self.font.render("Pressione R para reiniciar", True, (255, 255, 255))
            self.screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20)))
            self.screen.blit(retry, retry.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 30)))
            self.end_shown = True

        pygame.display.flip()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font = pygame.font.SysFont(None, 40)
    menu = MainMenu(screen, font)
    choice = menu.run()

    if choice == "start":
        Game().run()
    else:
        pygame.quit()
        sys.exit()