import pygame

class AssetManager:
    def __init__(self):
        self.background = pygame.transform.scale(pygame.image.load("space_game/assets/img/background.jpg"), (800, 600))
        self.player = pygame.transform.scale(pygame.image.load("space_game/assets/img/player.png"), (50, 40))
        self.bullet = pygame.image.load("space_game/assets/img/bullet.png")
        self.alien = pygame.transform.scale(pygame.image.load("space_game/assets/img/alien.png"), (40, 30))
        self.explosion = pygame.transform.scale(pygame.image.load("space_game/assets/img/explosion.png"), (70, 50))
        self.bullet_alien = pygame.image.load("space_game/assets/img/bullet_alien.png")

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.shot = pygame.mixer.Sound("space_game/assets/sound/shot.wav")
        self.shot.set_volume(0.2)
        self.explosion = pygame.mixer.Sound("space_game/assets/sound/explosion.wav")
        self.dead = pygame.mixer.Sound("space_game/assets/sound/dead.wav")
        self.win = pygame.mixer.Sound("space_game/assets/sound/win.wav")
