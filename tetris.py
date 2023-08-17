import pygame
import random
import sys

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Spielfeldgröße
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 45
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Tetris-Figuren
SHAPES = [
    [[1, 1, 1, 1]],              # Cyan
    [[1, 1], [1, 1]],            # Gelb
    [[1, 1, 0], [0, 1, 1]],      # Orange
    [[0, 1, 1], [1, 1, 0]],      # Blau
    [[1, 1, 1], [0, 1, 0]],      # Grün
    [[1, 1, 1], [1, 0, 0]],      # Lila
    [[1, 1, 1], [0, 0, 1]]       # Rot
]

# Farben für die Formen
SHAPE_COLORS = [
    CYAN,
    YELLOW,
    ORANGE,
    BLUE,
    GREEN,
    PURPLE,
    RED
]

# Initialisierung des Spielfelds
grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]

# Punktestand
score = 0

# Initialisierung von Pygame
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tetris")

# Funktion zum Zeichnen des Spielfelds
def draw_grid():
    window.fill(BLACK)
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            color = get_color(grid[row][col])
            pygame.draw.rect(window, color, (col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Funktion zum Zeichnen der aktuellen Figur
def draw_shape(shape, row, col, color):
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j]:
                pygame.draw.rect(window, color, ((col + j) * GRID_SIZE, (row + i) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Funktion zum Zeichnen des Vorschau-Steins
def draw_preview_shape(shape):
    preview_row = 1
    preview_col = 1
    color = WHITE
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j]:
                pygame.draw.rect(window, color, ((preview_col + j) * GRID_SIZE, (preview_row + i) * GRID_SIZE, GRID_SIZE, GRID_SIZE))

# Funktion zum Überprüfen, ob eine Bewegung gültig ist
def is_valid_move(shape, row, col):
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j]:
                if row + i >= GRID_HEIGHT or col + j < 0 or col + j >= GRID_WIDTH or grid[row + i][col + j]:
                    return False
    return True

# Funktion zum Rotieren der Figur
def rotate_shape(shape):
    return list(zip(*reversed(shape)))

# Funktion zum Einfügen der aktuellen Figur ins Spielfeld
def place_shape(shape, row, col, color):
    for i in range(len(shape)):
        for j in range(len(shape[0])):
            if shape[i][j]:
                grid[row + i][col + j] = color

# Funktion zum Überprüfen, ob eine Zeile voll ist
def is_full_row(row):
    for cell in grid[row]:
        if cell == 0:
            return False
    return True

# Funktion zum Löschen einer vollen Zeile
def clear_row(row):
    del grid[row]
    grid.insert(0, [0] * GRID_WIDTH)

# Funktion zum Überprüfen, ob das Spiel vorbei ist
def is_game_over():
    return any(grid[0])

# Funktion zur Umwandlung des Zahlenwerts in eine Farbe
def get_color(value):
    if value > 0:
        return SHAPE_COLORS[value-1]
    else:
        return BLACK

# Funktion zum Zeichnen des Punktestands
def draw_score():
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    score_rect = score_text.get_rect()
    score_rect.topright = (WINDOW_WIDTH - 20, 20)
    window.blit(score_text, score_rect)

# Hauptschleife des Spiels
clock = pygame.time.Clock()
current_shape = random.choice(SHAPES)
current_color = random.randint(1, len(SHAPE_COLORS))
next_shape = random.choice(SHAPES)
shape_row, shape_col = 0, GRID_WIDTH // 2 - len(current_shape[0]) // 2
game_over = False
move_down_timer = pygame.time.get_ticks()
show_preview = False  # Setze das Vorschaubild auf False
fall_speed = 500  # Anfangsgeschwindigkeit

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_v:
                show_preview = not show_preview

    # Steuerung der Figur
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and is_valid_move(current_shape, shape_row, shape_col - 1):
        shape_col -= 1
    elif keys[pygame.K_RIGHT] and is_valid_move(current_shape, shape_row, shape_col + 1):
        shape_col += 1
    elif keys[pygame.K_DOWN] and is_valid_move(current_shape, shape_row + 1, shape_col):
        shape_row += 1
    elif keys[pygame.K_SPACE]:
        rotated_shape = rotate_shape(current_shape)
        if is_valid_move(rotated_shape, shape_row, shape_col):
            current_shape = rotated_shape

    # Automatisches Fallenlassen des Steins
    current_time = pygame.time.get_ticks()
    if current_time - move_down_timer > fall_speed:
        if is_valid_move(current_shape, shape_row + 1, shape_col):
            shape_row += 1
        else:
            place_shape(current_shape, shape_row, shape_col, current_color)
            for i in range(GRID_HEIGHT):
                if is_full_row(i):
                    clear_row(i)
                    score += 10  # Erhöhe den Punktestand um 10
                    fall_speed -= 50  # Verringere die Fallgeschwindigkeit um 50 ms
            if is_game_over():
                game_over = True
                break
            else:
                current_shape = next_shape
                current_color = random.randint(1, len(SHAPE_COLORS))
                next_shape = random.choice(SHAPES)
                shape_row, shape_col = 0, GRID_WIDTH // 2 - len(current_shape[0]) // 2
                if not is_valid_move(current_shape, shape_row, shape_col):
                    game_over = True
        move_down_timer = current_time

    # Zeichnen des Spielfelds und der aktuellen Figuren
    draw_grid()
    draw_shape(current_shape, shape_row, shape_col, SHAPE_COLORS[current_color-1])
    if show_preview:
        draw_preview_shape(next_shape)
    draw_score()
    pygame.display.flip()

    # Begrenzung der Aktualisierungsrate auf 10 Frames pro Sekunde
    clock.tick(10)

# Spiel vorbei
font = pygame.font.Font(None, 72)
game_over_text = font.render("Du hast verloren!", True, WHITE)
game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
window.blit(game_over_text, game_over_rect)
pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
