import random
import pygame
from settings import *

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.type = 'normal'
        self.color = RED
        self.score = 1  # Добавляем атрибут score
        self.spawn_time = 0
        self.spawn_food()
    
    def spawn_food(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), 
                         random.randint(0, GRID_HEIGHT - 1))
        
        # Выбор типа еды
        rand = random.random()
        if rand < 0.65:
            self.type = 'normal'
            self.score = 1
            self.color = FOOD_TYPES['normal']['color']
        elif rand < 0.85:
            self.type = 'special'
            self.score = 5
            self.color = FOOD_TYPES['special']['color']
        elif rand < 0.98:
            self.type = 'golden'
            self.score = 10
            self.color = FOOD_TYPES['golden']['color']
        else:
            self.type = 'rainbow'
            self.score = 7
            self.color = FOOD_TYPES['rainbow']['color']
        
        self.spawn_time = pygame.time.get_ticks()
    
    def draw(self, surface):
        x, y = self.position
        center = (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2)
        
        if self.type == 'normal':
            pygame.draw.circle(surface, self.color, center, GRID_SIZE // 2 - 2)
        elif self.type == 'special':
            pygame.draw.polygon(surface, self.color, [
                (center[0], center[1] - GRID_SIZE // 3),
                (center[0] + GRID_SIZE // 3, center[1] + GRID_SIZE // 3),
                (center[0] - GRID_SIZE // 3, center[1] + GRID_SIZE // 3)
            ])
        elif self.type == 'golden':
            pygame.draw.rect(surface, self.color, 
                           (x * GRID_SIZE + 2, y * GRID_SIZE + 2,
                            GRID_SIZE - 4, GRID_SIZE - 4),
                           border_radius=GRID_SIZE // 4)
        elif self.type == 'rainbow':
            pygame.draw.circle(surface, self.color, center, GRID_SIZE // 2 - 2)
            if (pygame.time.get_ticks() - self.spawn_time) % 200 < 100:
                pygame.draw.circle(surface, WHITE, center, GRID_SIZE // 3)
    
    def get_score(self):
        return self.score
    
    def get_effect(self):
        if self.type in FOOD_TYPES:
            return FOOD_TYPES[self.type].get('effect', None)
        return None
    
    def get_effect_duration(self):
        if self.type in FOOD_TYPES:
            return FOOD_TYPES[self.type].get('duration', 0)
        return 0