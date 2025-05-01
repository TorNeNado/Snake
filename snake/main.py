import pygame
import sys
import time
import json
from settings import *
from snake import Snake
from food import Food
from bullets import *
from particles import ParticleSystem
from sounds import SoundManager

player_name = None

def menu():
    # Menu setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Супер-пупер змейка - Меню")
    font = pygame.font.SysFont("Arial", 50)
    clock = pygame.time.Clock()
    global player_name
    


    options = ["Start","Leaderboard", "Exit"]
    selected_index = 0  # Track the currently selected option

    running = True
    while running:
        screen.fill(BLACK)

        # Draw menu options
        for i, option in enumerate(options):
            # Button setup
            button_x = WIDTH // 2 - 100
            button_y = HEIGHT // 2 - 60 + i * 65  # Adjusted spacing between buttons

            # Change background color for the selected option
            if i == selected_index:
                pygame.draw.rect(screen, GREEN, (button_x - 100, button_y + 15, 400, 50))
            else:
                pygame.draw.rect(screen, WHITE, (button_x - 100, button_y + 15, 400, 50))

            # Draw the text on top of the button
            color = RED
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, button_y + 10))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Move selection up
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:  # Move selection down
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:  # Select the current option
                    if options[selected_index] == "Start":
                        if player_name is None:
                            player_name = get_player_name()
                        running = False
                        return player_name # Exit menu and start the game
                    elif options[selected_index] == "Leaderboard":
                        leaderboard_menu() # Show leaderbord
                    elif options[selected_index] == "Exit":
                        pygame.quit()
                        exit()

        pygame.display.flip()
        clock.tick(30)
def pause_menu(screen):
    """Display the in-game pause menu."""
    font = pygame.font.SysFont("Arial", 50)
    clock = pygame.time.Clock()

    # Menu options
    options = ["Resume", "Menu"]
    selected_index = 0  # Track the currently selected option

    # Button dimensions
    button_width = 250
    button_height = 60
    button_spacing = 20

    paused = True
    while paused:
        screen.fill(BLACK)

        # Draw menu options with backgrounds
        for i, option in enumerate(options):
            # Calculate button position dynamically
            button_x = WIDTH // 2 - button_width // 2
            button_y = HEIGHT // 2 - (len(options) * (button_height + button_spacing)) // 2 + i * (button_height + button_spacing)

            # Change background color for the selected option
            if i == selected_index:
                pygame.draw.rect(screen, GREEN, (button_x, button_y, button_width, button_height))
            else:
                pygame.draw.rect(screen, WHITE, (button_x, button_y, button_width, button_height))

            # Draw the text on top of the button
            color = RED
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, button_y + 10))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Move selection up
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == pygame.K_DOWN:  # Move selection down
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == pygame.K_RETURN:  # Select the current option
                    if options[selected_index] == "Resume":
                        paused = False  # Resume the game
                    elif options[selected_index] == "Menu":
                        return "menu"  # Go back to the main menu
                elif event.key == pygame.K_ESCAPE:  # Resume the game
                    paused = False

        pygame.display.flip()
        clock.tick(30)

    return "resume"

def load_scores(file_path):
    """Load scores from a JSON file."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return an empty list if the file doesn't exist

def display_leaderboard(screen, scores):
    """Display the leaderboard on the screen."""
    font = pygame.font.SysFont("Arial", 40)
    title_font = pygame.font.SysFont("Arial", 50, bold=True)
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(BLACK)

        # Display title
        title_text = title_font.render("Leaderboard", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))

        # Display scores
        for i, entry in enumerate(scores[:10]):  # Show top 10 scores
            name = entry["name"]
            score = entry["score"]
            date = entry["date"]

            score_text = font.render(f"{i + 1}. {name} - {score} ({date})", True, WHITE)
            screen.blit(score_text, (30, 120 + i * 50))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Exit leaderboard
                    running = False

        pygame.display.flip()
        clock.tick(30)

def leaderboard_menu():
    """Load and display the leaderboard."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Leaderboard")

    # Load scores
    scores = load_scores("score.json")

    # Sort scores by highest score
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)

    # Display leaderboard
    display_leaderboard(screen, scores)

def save_score(file_path, name, score):
    """Save the player's score to the JSON file."""
    scores = load_scores(file_path)
    from datetime import datetime
    scores.append({
        "name": name,
        "score": score,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    with open(file_path, "w") as file:
        json.dump(scores, file, indent=4)

def get_player_name():
    """Prompt the player to enter their name with a maximum of 10 characters."""
    import tkinter as tk
    from tkinter import simpledialog

    root = tk.Tk()
    root.withdraw()  # Hide the root window

    while True:
        player_name = simpledialog.askstring("Player Name", "Enter your name (max 10 characters):")
        if player_name and len(player_name) <= 10:  # Check if the name is valid
            return player_name
        elif not player_name:  # If the player cancels or enters nothing
            return "Anonymous"  # Default to "Anon"
        else:
            # Show an error message if the name is too long
            tk.messagebox.showerror("Invalid Name", "Name must be 10 characters or fewer.")

def main():
    global player_name
    player_name = menu()
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
    sound_manager.load_sound("eat", f"snake/assents/sounds/eat.wav")
    sound_manager.load_sound("game_over", f"snake/assents/sounds/game_over.wav")
    sound_manager.load_sound("effect", f"snake/assents/sounds/effect.wav")
    
    # Загрузка шрифта
    try:
        font = pygame.font.Font(f"snake/assents/fonts/arial.ttf", 30)
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
                    elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:  # Open pause menu
                        action = pause_menu(screen)
                        if action == "menu":
                            return main()  # Restart the game from the main menu
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:  # Open pause menu
                        action = pause_menu(screen)
                        if action == "menu":
                            return main()  # Restart the game from the main menu
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
            if active :
                if effect == 'score_multiplier' and snake.effect_timers[effect] != 0:
                    text = f"{effect}: {snake.effect_timers[effect]}"
                    effect_text = font.render(text, True, YELLOW)
                    screen.blit(effect_text, (10, effect_y))
                    effect_y += 30
                elif effect != 'score_multiplier':
                    text = f"{effect}: {snake.effect_timers[effect]}"
                    effect_text = font.render(text, True, YELLOW)
                    screen.blit(effect_text, (10, effect_y))
                    effect_y += 30
        
        # Game Over
        if game_over:
            scores = load_scores("score.json")
            highest_score = max(scores, key=lambda x: x["score"])["score"] if scores else 0
            if snake.score > highest_score:
                save_score("score.json", player_name, snake.score)
                game_over_text = font.render("NEW HIGH SCORE!", True, GREEN)
            else:
                game_over_text = font.render("GAME OVER! Нажмите SPACE для новой игры", True, RED)

            text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(game_over_text, text_rect)

        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()