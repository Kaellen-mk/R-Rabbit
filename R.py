import pygame
import random

# Inicializa Pygame e mixer
pygame.init()
try:
    pygame.mixer.init()
    sound_enabled = True
except Exception as e:
    print("Aviso: mixer de áudio não pôde ser inicializado:", e)
    sound_enabled = False

# Tela
screen_width = 800
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("R-Rabbit")

# Cores
azul = (135, 206, 235)
verde_grama = (34, 139, 34)
verde_tufo = (0, 100, 0)
black = (0, 0, 0)
white = (255, 255, 255)

# Clock e fonte
clock = pygame.time.Clock()
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Imagens
rabbit_image = pygame.image.load(r'c:/Users/kaell/.vscode/mk/.vscode/C-Coelho/assets/rabbit.png')
rabbit_image = pygame.transform.scale(rabbit_image, (70, 70))

carrot_width = 60
carrot_height = 60
carrot_image = pygame.image.load(r'c:/Users/kaell/.vscode/mk/.vscode/C-Coelho/assets/carrot.png')
carrot_image = pygame.transform.scale(carrot_image, (carrot_width, carrot_height))

cloud_image = pygame.image.load(r'c:/Users/kaell/.vscode/mk/.vscode/C-Coelho/assets/cloud.png')
cloud_image = pygame.transform.scale(cloud_image, (100, 60))

# Sons
if sound_enabled:
    try:
        jump_sound = pygame.mixer.Sound('jump.wav')
    except:
        print("Aviso: jump.wav não encontrado.")
        jump_sound = None
    try:
        game_over_sound = pygame.mixer.Sound('game_over.wav')
    except:
        print("Aviso: game_over.wav não encontrado.")
        game_over_sound = None
else:
    jump_sound = None
    game_over_sound = None

clouds = [
    {"x": 300, "y": 50, "speed": 2},
    {"x": 600, "y": 30, "speed": 1},
    {"x": 100, "y": 70, "speed": 1.5}
]


# Funções de desenho
def draw_rabbit(x, y):
    screen.blit(rabbit_image, (x, y))


def draw_carrot(x, y):
    screen.blit(carrot_image, (x, y))


def draw_grass(offset=0):
    ground_height = 50
    y = screen_height - ground_height
    pygame.draw.rect(screen, verde_grama, (0, y, screen_width, ground_height))

    # Tufos de grama
    tile_width = 20
    for i in range(0, screen_width + tile_width, tile_width):
        x = (i - offset % tile_width)
        pygame.draw.rect(screen, verde_tufo, (x, y, 3, 10))
        pygame.draw.rect(screen, verde_tufo, (x + 5, y + 5, 2, 7))
        pygame.draw.rect(screen, verde_tufo, (x + 10, y, 3, 10))


def draw_clouds():
    for cloud in clouds:
        screen.blit(cloud_image, (cloud["x"], cloud["y"]))
        cloud["x"] -= cloud["speed"]
        if cloud["x"] < -100:
            cloud["x"] = screen_width + random.randint(0, 200)
            cloud["y"] = random.randint(20, 80)


def draw_score(score):
    score_text = small_font.render(f"Pontuação: {score}", True, white)
    screen.blit(score_text, (10, 10))


def reset_game():
    return {
        "rabbit_x": 50,
        "rabbit_y": screen_height - 70 - 40,
        "rabbit_jump": False,
        "jump_count": 10,
        "carrot_x": screen_width,
        "carrot_y": screen_height - 70 - 50,
        "score": 0,
        "game_over": False,
        "grass_scroll_offset": 0
    }


state = reset_game()
running = True
while running:
    clock.tick(25)
    screen.fill(azul)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    draw_clouds()
    draw_grass(state["grass_scroll_offset"])
    state["grass_scroll_offset"] += 4

    if not state["game_over"]:
        if state["rabbit_jump"]:
            if state["jump_count"] >= -10:
                neg = 1
                if state["jump_count"] < 0:
                    neg = -1
                state["rabbit_y"] -= (state["jump_count"] ** 2) * 0.5 * neg
                state["jump_count"] -= 1
            else:
                state["rabbit_jump"] = False
                state["jump_count"] = 10

        state["carrot_x"] -= 7
        if state["carrot_x"] < 0:
            state["carrot_x"] = screen_width
            state["score"] += 1

        if (state["carrot_x"] < state["rabbit_x"] + 50 and
                state["carrot_x"] + carrot_width > state["rabbit_x"] and
                state["carrot_y"] < state["rabbit_y"] + 50 and
                state["carrot_y"] + carrot_height > state["rabbit_y"]):
            state["game_over"] = True
            if game_over_sound:
                game_over_sound.play()

        draw_rabbit(state["rabbit_x"], state["rabbit_y"])
        draw_carrot(state["carrot_x"], state["carrot_y"])
        draw_score(state["score"])
    else:
        game_over_text = font.render("Game Over", True, black)
        screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 60))

        score_text = font.render(f"Pontuação: {state['score']}", True, black)
        screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))

        restart_text = small_font.render("Pressione ENTER para reiniciar", True, black)
        screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 60))

        if keys[pygame.K_RETURN]:
            state = reset_game()

    pygame.display.update()

    if keys[pygame.K_SPACE] and not state["rabbit_jump"] and not state["game_over"]:
        state["rabbit_jump"] = True
        if jump_sound:
            jump_sound.play()

pygame.quit()
