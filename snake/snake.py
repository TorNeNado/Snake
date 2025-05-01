import pygame
import time
import math
from settings import *
from bullets import *
# Define COLORS if not already defined in settings
COLORS = [GREEN, RED, BLUE, YELLOW, PURPLE]  # Example color list
from particles import Particle

class Snake:
    def __init__(self):
        self.reset()
        self.particles = []
        self.bullets = []  # List to store bullets
        self.last_shot_time = -1000  # Track the time of the last shot
        self.shoot_cooldown = 1000  # Cooldown in milliseconds (2 seconds)

    def shoot(self):
        # Create a new bullet at the snake's head
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            head_x, head_y = self.get_head_position()
            bullet_x = head_x * GRID_SIZE + GRID_SIZE // 2
            bullet_y = head_y * GRID_SIZE + GRID_SIZE // 2
            bullet = Bullet(bullet_x, bullet_y, self.direction, self.color)
            self.bullets.append(bullet)
            self.last_shot_time = current_time
        
        
    def reset(self):
        self.positions = [SNAKE_START_POS]
        for i in range(1, SNAKE_START_LENGTH):
            self.positions.append((SNAKE_START_POS[0] - i, SNAKE_START_POS[1]))
            
        self.length = SNAKE_START_LENGTH
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.score = 0
        self.color = GREEN
        self.speed = FPS
        self.grow_to = self.length
        self.last_move_time = 0
        self.special_effects = {
            'rainbow': False,
            'speed_boost': False,
            'invincible': False,
            'score_multiplier': 1
        }
        self.effect_timers = {
            'rainbow': 0,
            'speed_boost': 0,
            'invincible': 0,
            'score_multiplier': 0
        }
    
    def get_head_position(self):
        return self.positions[0]
    
    def update(self, current_time):
        # Обновление эффектов
        self.bullets = [b for b in self.bullets if b.update()]
        for effect in list(self.effect_timers.keys()):
            if self.effect_timers[effect] > 0:
                self.effect_timers[effect] -= 1
                if self.effect_timers[effect] <= 0:
                    self.special_effects[effect] = False
                    if effect == 'speed_boost':
                        self.speed = FPS
                    elif effect == 'score_multiplier':
                        self.special_effects['score_multiplier'] = 1
        
        # Обновление частиц
        self.particles = [p for p in self.particles if p.update()]
        
        # Движение змейки
        if current_time - self.last_move_time > 1000 / self.speed:
            self.last_move_time = current_time
            self.direction = self.next_direction
        
            head_x, head_y = self.get_head_position()
            dir_x, dir_y = self.direction
            new_x = head_x + dir_x
            new_y = head_y + dir_y
        
            # Проверка на столкновение со стенами (границами)
            if new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT:
                return False  # Смерть при столкновении со стеной
            
            # Проверка на столкновение с собой
            if (new_x, new_y) in self.positions[1:]:
                return False
            
            self.positions.insert(0, (new_x, new_y))
            if len(self.positions) > self.grow_to:
                self.positions.pop()
    
        return True
    
    def draw(self, surface):
        # Отрисовка частиц
        for p in self.particles:
            p.draw(surface)

        for bullet in self.bullets:
            bullet.draw(surface)
            
        # Отрисовка змейки
        for i, (x, y) in enumerate(self.positions):
            color = self.color
            
            if self.special_effects['rainbow']:
                color_idx = (i + pygame.time.get_ticks() // 100) % len(COLORS)
                color = COLORS[color_idx]
            
            rect = pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            if i == 0:  # Голова
                pygame.draw.rect(surface, color, rect)
                eye_size = GRID_SIZE // 5
                # Глаза
                pygame.draw.circle(surface, WHITE, 
                                   (x * GRID_SIZE + GRID_SIZE // 3, y * GRID_SIZE + GRID_SIZE // 3), 
                                   eye_size)
                pygame.draw.circle(surface, WHITE, 
                                   (x * GRID_SIZE + 2 * GRID_SIZE // 3, y * GRID_SIZE + GRID_SIZE // 3), 
                                   eye_size)
                # Зрачки
                pygame.draw.circle(surface, BLACK, 
                                   (x * GRID_SIZE + GRID_SIZE // 3 + self.direction[0] * 2, 
                                    y * GRID_SIZE + GRID_SIZE // 3 + self.direction[1] * 2), 
                                   eye_size // 2)
                pygame.draw.circle(surface, BLACK, 
                                   (x * GRID_SIZE + 2 * GRID_SIZE // 3 + self.direction[0] * 2, 
                                    y * GRID_SIZE + GRID_SIZE // 3 + self.direction[1] * 2), 
                                   eye_size // 2)
            else:  # Тело
                pygame.draw.rect(surface, color, rect, border_radius=GRID_SIZE // 4)
    
    def grow(self):
        self.grow_to += 1
    
    def apply_effect(self, effect, duration):
        self.special_effects[effect] = True
        self.effect_timers[effect] = duration
        
        if effect == 'speed_boost':
            self.speed = FPS * 1.5
        elif effect == 'score_multiplier':
            self.special_effects['score_multiplier'] = 2
    
    def change_direction(self, direction):
        # Запрещаем разворот на 180 градусов
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.next_direction = direction