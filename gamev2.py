import pygame, sys, time, random

def init_game():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("Space Invaders")
    icon = pygame.transform.scale(pygame.image.load("img/logo.png"), (128, 128))
    pygame.display.set_icon(icon)

def load_assets():
    return {
        "background": pygame.transform.scale(pygame.image.load("img/background.jpg"), (800, 600)),
        "player": pygame.transform.scale(pygame.image.load("img/player.png"), (50, 40)),
        "alien": pygame.transform.scale(pygame.image.load("img/alien.png"), (40, 30)),
        "explosion": pygame.transform.scale(pygame.image.load("img/explosion.png"), (70, 50)),
        "bullet": pygame.image.load("img/bullet.png"),
        "alien_bullet": pygame.image.load("img/bullet_alien.png"),
        "heart": pygame.transform.scale(pygame.image.load("img/heart.png"), (30, 30)),
        "bg_music": "som/background.wav",
        "shot_sound": pygame.mixer.Sound("som/shot.wav"),
        "explosion_sound": pygame.mixer.Sound("som/explosion.wav"),
        "win_sound": pygame.mixer.Sound("som/win.wav"),
        "dead_sound": pygame.mixer.Sound("som/dead.wav")
    }

def init_state(difficulty):
    return {
        "score": 0,
        "lives": 3,
        "player": pygame.Rect(800 // 2 - 25, 600 - 50, 50, 40),
        "bullets": [],
        "aliens": [pygame.Rect(80 + c * 60, 50 + r * 40, 40, 30) for r in range(5) for c in range(8)],
        "alien_bullets": [],
        "alien_direction": 1,
        "last_enemy_fire": pygame.time.get_ticks(),
        "explosions": [],
        "invulnerable": False,
        "invulnerable_start": 0,
        "game_over": False,
        "winner": False,
        "difficulty": difficulty,
        "score_multiplier": 10 * difficulty
    }

def game_loop():
    WIDTH, HEIGHT = 800, 600
    difficulty = 1
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 40)
    assets = load_assets()
    state = init_state(difficulty)
    pygame.mixer.music.load(assets["bg_music"])
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.1)
    assets["shot_sound"].set_volume(0.2)

    while True:
        events()
        update_game(state, assets, WIDTH, HEIGHT)
        render_game(screen, state, assets, font, WIDTH, HEIGHT)
        if state["game_over"]:
            end_game(screen, state, assets, WIDTH, HEIGHT)
        pygame.display.flip()
        clock.tick(60)

def events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

def update_game(state, assets, WIDTH, HEIGHT):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and state["player"].left > 0:
        state["player"].x -= 5
    if keys[pygame.K_RIGHT] and state["player"].right < WIDTH:
        state["player"].x += 5
    if keys[pygame.K_SPACE]:
        if not state["bullets"] or state["bullets"][-1].y < HEIGHT - 150:
            state["bullets"].append(pygame.Rect(state["player"].centerx - 3, state["player"].y, 6, 12))
            assets["shot_sound"].play()

    current_time = pygame.time.get_ticks()
    if current_time - state["last_enemy_fire"] > 300 / state["difficulty"] and state["aliens"]:
        shooter = random.choice(state["aliens"])
        state["alien_bullets"].append(pygame.Rect(shooter.centerx, shooter.bottom, 6, 12))
        state["last_enemy_fire"] = current_time

    for b in state["bullets"][:]:
        b.y -= 6 + state["difficulty"]
        if b.bottom < 0:
            state["bullets"].remove(b)

    for b in state["bullets"][:]:
        for a in state["aliens"][:]:
            if b.colliderect(a):
                state["bullets"].remove(b)
                state["aliens"].remove(a)
                state["explosions"].append({"rect": a.copy(), "start_time": current_time})
                state["score"] += state["score_multiplier"]
                if not state["aliens"]:
                    state["winner"] = True
                    state["game_over"] = True
                break

    for b in state["alien_bullets"][:]:
        b.y += 5
        if b.top > HEIGHT:
            state["alien_bullets"].remove(b)
        elif b.colliderect(state["player"]) and not state["invulnerable"]:
            state["explosions"].append({"rect": state["player"].copy(), "start_time": current_time})
            assets["explosion_sound"].play()
            state["lives"] -= 1
            state["alien_bullets"].remove(b)
            if state["lives"] <= 0:
                state["game_over"] = True
            else:
                state["invulnerable"] = True
                state["invulnerable_start"] = current_time

    edge_hit = False
    for a in state["aliens"]:
        a.x += (2 + state["difficulty"]) * state["alien_direction"]
        if a.right >= WIDTH or a.left <= 0:
            edge_hit = True
    if edge_hit:
        state["alien_direction"] *= -1
        for a in state["aliens"]:
            a.y += 20

    if state["invulnerable"] and current_time - state["invulnerable_start"] > 3000:
        state["invulnerable"] = False

def render_game(screen, state, assets, font, WIDTH, HEIGHT):
    screen.blit(assets["background"], (0, 0))
    if not state["invulnerable"] or (pygame.time.get_ticks() // 100) % 2 == 0:
        screen.blit(assets["player"], state["player"])
    for b in state["bullets"]:
        screen.blit(assets["bullet"], b)
    for b in state["alien_bullets"]:
        screen.blit(assets["alien_bullet"], b)
    for a in state["aliens"]:
        screen.blit(assets["alien"], a)
    for e in state["explosions"][:]:
        if pygame.time.get_ticks() - e["start_time"] > 200:
            state["explosions"].remove(e)
        else:
            screen.blit(assets["explosion"], e["rect"])
    screen.blit(font.render(f"Score: {state['score']}", True, (255, 255, 255)), (10, 10))
    for i in range(state["lives"]):
        screen.blit(assets["heart"], (WIDTH - (i + 1) * 35 - 10, 10))

def end_game(screen, state, assets, WIDTH, HEIGHT):
    msg = "WINNER" if state["winner"] else "GAME OVER"
    color = (0, 255, 0) if state["winner"] else (255, 0, 0)
    sound = assets["win_sound"] if state["winner"] else assets["dead_sound"]
    sound.play()
    font = pygame.font.SysFont(None, 120)
    shadow = font.render(msg, True, (0, 0, 0))
    shadow_rect = shadow.get_rect(center=(WIDTH // 2 + 2, HEIGHT // 2 + 2))
    text = font.render(msg, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(shadow, shadow_rect)
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    init_game()
    game_loop()
