import pygame
import random
import os

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRIS = (211, 211, 211)


# Crear la pantalla
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Juego de Esquivar con Imágenes")

# Ruta de las imágenes
img_folder = os.path.join(os.path.dirname(__file__), 'img')
player_image_path = os.path.join(img_folder, 'me.jpeg')
enemy_image_path = os.path.join(img_folder, 'enemy.jpeg')


player_image = pygame.image.load(player_image_path)
enemy_image = pygame.image.load(enemy_image_path)

# Tamaño de las imágenes
player_image = pygame.transform.scale(player_image, (80, 80))
enemy_image = pygame.transform.scale(enemy_image, (100, 100))

player_size = player_image.get_rect().size
enemy_size = enemy_image.get_rect().size


def detect_collision(player_pos, enemy_pos):
    p_x, p_y = player_pos
    e_x, e_y = enemy_pos

    if (e_x >= p_x and e_x < (p_x + player_size[0])) or (p_x >= e_x and p_x < (e_x + enemy_size[0])):
        if (e_y >= p_y and e_y < (p_y + player_size[1])) or (p_y >= e_y and p_y < (e_y + enemy_size[1])):
            return True
    return False

def update_enemy_positions(enemy_list, score, speed):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < SCREEN_HEIGHT:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        screen.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))

def collision_check(enemy_list, player_pos):
    for enemy_pos in enemy_list:
        if detect_collision(player_pos, enemy_pos):
            return True
    return False

def create_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.1:
        x_pos = random.randint(0, SCREEN_WIDTH - enemy_size[0])
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_game():
    player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 2 * player_size[1]]
    enemy_pos = [random.randint(0, SCREEN_WIDTH - enemy_size[0]), 0]
    enemy_list = [enemy_pos]

    SPEED = 40

    clock = pygame.time.Clock()

    game_over = False
    score = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= SPEED
        if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - player_size[0]:
            player_pos[0] += SPEED
        
        screen.fill(GRIS)

        create_enemies(enemy_list)
        score = update_enemy_positions(enemy_list, score, SPEED)
        
        if collision_check(enemy_list, player_pos):
            game_over = True
            break

        draw_enemies(enemy_list)

        # Dibujar al jugador
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        # Dibujar el puntaje
        font = pygame.font.SysFont(None, 55)
        draw_text(f"Puntaje: {score}", font, BLACK, screen, 10, 10)

        pygame.display.update()

        clock.tick(30)

    return score

def game_over_screen(score):
    screen.fill(WHITE)
    font = pygame.font.SysFont(None, 75)
    draw_text("Game Over Puto", font, RED, screen, SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100)
    draw_text(f"Puntaje: {score}", font, BLACK, screen, SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2)
    draw_text("Presiona R para reiniciar", font, GREEN, screen, SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 + 100)
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False

while True:
    score = main_game()
    game_over_screen(score)
