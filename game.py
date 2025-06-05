import pygame, sys, time, random

pygame.init()
pygame.display.set_caption("Space Invaders")
pygame.display.set_icon(pygame.transform.scale(pygame.image.load("img/logo.png"), (128, 128)))
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

# Constantes
difficulty = 1 # 1: normal, 2: hard, 3: souls like
score = 0
score_multiplier = 10 * difficulty
player_lives = 3
player_speed = 5
bullet_speed = 6 + difficulty
alien_speed = 2 + difficulty
enemy_bullet_speed = 5
enemy_fire_delay = 300 / difficulty
invulnerable_start = 0
invulnerable = False
game_over = False
winner = False

# images
background_img = pygame.transform.scale(pygame.image.load("img/background.jpg"), (800, 600))
player_img = pygame.transform.scale(pygame.image.load("img/player.png"), (50, 40))
alien_img = pygame.transform.scale(pygame.image.load("img/alien.png"), (40, 30))
explosion_img = pygame.transform.scale(pygame.image.load("img/explosion.png"), (70, 50))
bullet_img = pygame.image.load("img/bullet.png") 
alien_bullet_img = pygame.image.load("img/bullet_alien.png")
heart_img = pygame.transform.scale(pygame.image.load("img/heart.png"), (30, 30))

# m usic
pygame.mixer.init()
pygame.mixer.music.load("som/background.wav") 
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# sfx
shot_sound = pygame.mixer.Sound("som/shot.wav")
shot_sound.set_volume(0.2)
explosion_sound = pygame.mixer.Sound("som/explosion.wav")
win_sound = pygame.mixer.Sound("som/win.wav")
dead_sound = pygame.mixer.Sound("som/dead.wav")

# player
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 50, 50, 40)
bullets = []

# Aliens
alien_rows, alien_cols = 5 , 8
alien_w, alien_h = 40, 30
aliens = []
alien_bullets = []
for row in range(alien_rows):
    for col in range(alien_cols):
        aliens.append(pygame.Rect(80 + col * 60, 50 + row * 40, alien_w, alien_h))
alien_direction = 1
last_enemy_fire = pygame.time.get_ticks()

# boom 
explosions = []

# Main Loop
while True:
    # background
    win.blit(background_img, (0, 0))
    for quit in pygame.event.get():
        if quit.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    # keys and player move       
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0: player.x -= player_speed
    if keys[pygame.K_RIGHT] and player.right < WIDTH: player.x += player_speed
    if keys[pygame.K_SPACE]:
        if not bullets or bullets[-1].y < HEIGHT - 150:
            bullets.append(pygame.Rect(player.centerx - 3, player.y, 6, 12))
            shot_sound.play()
    
    # alien bullets     
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_fire > enemy_fire_delay and aliens:
        shooting_alien = aliens[random.randint(0, len(aliens) - 1)]
        alien_bullets.append(pygame.Rect(shooting_alien.centerx, shooting_alien.bottom, 6, 12))
        last_enemy_fire = current_time

    # check alien hit
    for ali in aliens:
        if ali.colliderect(player):
            game_over = True
            break

    # update bullets
    for bul in bullets[:]:
        bul.y -= bullet_speed
        if bul.bottom < 0:
            bullets.remove(bul)
          
    # check player hit
    for bul in bullets[:]:
        for ali in aliens[:]:
            if bul.colliderect(ali):
                bullets.remove(bul)
                aliens.remove(ali)
                explosions.append({
                    'rect': ali.copy(),
                    'start_time': pygame.time.get_ticks()
                })
                score += score_multiplier
                if not aliens:
                    winner = True
                    game_over = True
                break

    # bullets
    for b in bullets:
        win.blit(bullet_img, b)

    # alien bullet
    for bul in alien_bullets[:]:
        bul.y += enemy_bullet_speed
        if bul.top > HEIGHT:
            alien_bullets.remove(bul)
        elif bul.colliderect(player) and not invulnerable:
            explosions.append({
                'rect': player.copy(),
                'start_time': pygame.time.get_ticks()
            })
            explosion_sound.play()
            player_lives -= 1
            alien_bullets.remove(bul)
            if player_lives <= 0:
                game_over = True
            else:
                invulnerable = True
                invulnerable_start = pygame.time.get_ticks()
        else:
            win.blit(alien_bullet_img, bul)
    
    # aliens edge limitation
    edge_hit = False
    for ali in aliens:
        ali.x += alien_speed * alien_direction
        if ali.right >= WIDTH or ali.left <= 0:
            edge_hit = True
    if edge_hit:
        alien_direction *= -1
        for ali in aliens:
            ali.y += 20

    # Desenha jogador - Piscar nos primeiros 3 segundos da invulnerabilidade
    if not invulnerable or (current_time - invulnerable_start) > 3000 or (current_time // 100) % 2 == 0:
        win.blit(player_img, player)

    # Desenha aliens
    for ali in aliens:
        win.blit(alien_img, ali)
    
    # Controle de imunidade de dano
    if invulnerable:
        elapsed = current_time - invulnerable_start
        if elapsed > 3000:  # 3 segundos de invulnerabilidade (ms)
            invulnerable = False    
  
    for ex in explosions[:]:
        if current_time - ex['start_time'] > 200:
            explosions.remove(ex)
        else:
            win.blit(explosion_img, ex['rect'])

    # hud
    win.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10)) # score
    for heart in range(player_lives): # lives with hearts
        win.blit(heart_img, (WIDTH - (heart + 1) * 35 - 10, 10))
    
    # check status
    if game_over:
        if not hasattr(pygame, "end_sound_played"):
            pygame.end_sound_played = True
            if winner:
                msg = "WINNER"
                color = (0, 255, 0)
                win_sound.play()
            else:
                msg = "SE FODEU"
                color = (255, 0, 0)
                dead_sound.play()                
            end_font = pygame.font.SysFont(None, 120)
            shadow = end_font.render(msg, True, (0, 0, 0))
            shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 2, HEIGHT // 2 + 2))
            text = end_font.render(msg, True, color)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            win.blit(shadow, shadow_rect)
            win.blit(text, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)