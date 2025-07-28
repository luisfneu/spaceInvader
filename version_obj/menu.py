import pygame
from space_game.config import WIDTH, HEIGHT

class MainMenu:
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.options = ["Iniciar Jogo", "Sair"]
        self.selected = 0
        self.running = True

    def draw(self):
        self.screen.fill((0, 0, 0))
        title = self.font.render("SPACE INVADERS", True, (0, 255, 0))
        self.screen.blit(title, title.get_rect(center=(WIDTH // 2, 100)))

        for i, option in enumerate(self.options):
            color = (255, 255, 255) if i != self.selected else (255, 0, 0)
            text = self.font.render(option, True, color)
            self.screen.blit(text, text.get_rect(center=(WIDTH // 2, 200 + i * 60)))

        pygame.display.flip()

    def run(self):
        while self.running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        return "start" if self.selected == 0 else "quit"
