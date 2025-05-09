import pygame
from settings import *
class Bullet:
    def __init__(self, x, y, direction, color):
        self.x = x
        self.y = y
        self.direction = direction
        self.color = color
        self.speed = 30  # Adjust bullet speed as needed
        self.size = 5  # Bullet size

    def update(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        # Return False if the bullet goes off-screen
        return 0 <= self.x < WIDTH and 0 <= self.y < HEIGHT

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.size)