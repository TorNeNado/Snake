WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
FPS = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
ORANGE = (255, 160, 0)

SNAKE_START_LENGTH = 3
SNAKE_START_POS = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

FOOD_TYPES = {
    'normal' : {'color': RED, 'score': 1},
    'special': {'color': BLUE, 'score': 5, 'effect': 'speed_boost', 'duration': 100},
    'golden' : {'color': YELLOW, 'score': 10, 'effect': 'score_multiplier', 'duration': 200},
    'rainbow': {'color': PURPLE, 'score': 7, 'effect': 'rainbow', 'duration': 150}
}