import random
import math
import pygame

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.life = random.randint(20, 40)
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(0.5, 2)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        self.size = max(0, self.size - 0.1)
        return self.life > 0
        
    def draw(self, surface):
        alpha = min(255, self.life * 6)
        # Создаем поверхность с альфа-каналом
        s = pygame.Surface((self.size*2, self.size*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color[:3], alpha), (self.size, self.size), self.size)
        surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))

class ParticleSystem:
    def __init__(self):
        self.particles = []
    
    def add_particles(self, x, y, color, count=5):
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def update(self):
        self.particles = [p for p in self.particles if p.update()]
    
    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)