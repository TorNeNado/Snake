import pygame
import sys
from settings import *
from snake import Snake
from food import Food
from bullets import *
from particles import ParticleSystem
from sounds import SoundManager
def menu():
    # Menu setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Супер-пупер змейка - Меню")
    font = pygame.font.SysFont("Arial", 50)
    clock = pygame.time.Clock()

    # Button setup
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 60, 200, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)

    running = True
    while running:
        screen.fill(BLACK)

        # Draw buttons
        pygame.draw.rect(screen, GREEN, start_button)
        pygame.draw.rect(screen, RED, exit_button)

        # Draw button text
        start_text = font.render("Start", True, WHITE)
        exit_text = font.render("Exit", True, WHITE)
        screen.blit(start_text, (start_button.x + 50, start_button.y + 5))
        screen.blit(exit_text, (exit_button.x + 50, exit_button.y + 5))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    running = False  # Exit menu and start the game
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

        pygame.display.flip()
        clock.tick(30)

def main():
    # Call the menu first
    menu()

    # Инициализация
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Супер-пупер змейка - ВАУ!")
    clock = pygame.time.Clock()

    # Создание объектов
    snake = Snake()
    food = Food()
    particles = ParticleSystem()
    sound_manager = SoundManager()
    
    # Загрузка звуков
    sound_manager.load_sound("eat", "assets/sounds/eat.wav")
    sound_manager.load_sound("game_over", "assets/sounds/game_over.wav")
    sound_manager.load_sound("effect", "assets/sounds/effect.wav")
    
    # Загрузка шрифта
    try:
        font = pygame.font.Font("assets/fonts/arial.ttf", 30)
    except:
        font = pygame.font.SysFont("Arial", 30)
    
    # Игровой цикл
    running = True
    game_over = False
    
    while running:
        current_time = pygame.time.get_ticks()
        
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))
                    elif event.key == pygame.K_SPACE:  # Spacebar to shoot
                        snake.shoot()
                else:
                    if event.key == pygame.K_SPACE:
                        # Новая игра
                        snake.reset()
                        food.spawn_food()
                        game_over = False
        
        if not game_over:
            # Обновление игры
            if not snake.update(current_time):
                sound_manager.play("game_over")
                game_over = True
            
            # Проверка съедания еды
            if snake.get_head_position() == food.position:
                sound_manager.play("eat")
                
                # Добавление очков
                score_to_add = food.get_score() * snake.special_effects['score_multiplier']
                snake.score += score_to_add
                
                # Применение эффекта, если есть
                effect = food.get_effect()
                if effect:
                    sound_manager.play("effect")
                    snake.apply_effect(effect, food.get_effect_duration())
                
                # Рост змейки
                snake.grow()
                
                # Эффект частиц
                particles.add_particles(
                    food.position[0] * GRID_SIZE + GRID_SIZE // 2,
                    food.position[1] * GRID_SIZE + GRID_SIZE // 2,
                    food.color, 15
                )
                
                # Новая еда
                food.spawn_food()
            
            # Обновление частиц
            particles.update()
        
        # Отрисовка
        screen.fill(BLACK)
        
        # Сетка
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, GRID_SIZE):
            pygame.draw.line(screen, (50, 50, 50), (0, y), (WIDTH, y))
        
        # Еда
        food.draw(screen)
        
        # Змейка
        snake.draw(screen)
        
        # Частицы
        particles.draw(screen)
        
        # Очки
        score_text = font.render(f"Очки: {snake.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Эффекты
        effect_y = 50
        for effect, active in snake.special_effects.items():
            if active and effect != 'score_multiplier':
                text = f"{effect}: {snake.effect_timers[effect]}"

        
        # Game Over
        if game_over:
            # Display "Game Over" text
            game_over_text = font.render("Game Over! Press SPACE to restart", True, WHITE)
            screen.blit(game_over_text, (WIDTH // 2 - 200, HEIGHT // 2))
        
        pygame.display.flip()
        clock.tick(FPS)