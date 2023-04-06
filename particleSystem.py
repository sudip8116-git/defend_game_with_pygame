from random import randint
from settings import *
from func import getRandomColor, lerp

class ParticleSystem:
    def __init__(self,screen, x, y, rad, max_count, min_count, life_time):
        self.x = x
        self.y = y
        self.rad = rad
        self.screen = screen
        self.particle_count = random.randint(min_count, max_count)
        
        
        
        self.particles = [Particle(self.x, self.y, random.randint(50, 100) / 10, random.randint(10, 30) / 10, getRandomColor(), life_time) for i in range(self.particle_count)]
    
    
        
    def draw(self):
        for particle in self.particles:
            particle.draw(self.screen)
            particle.update()
            if particle.rad <= 0:
                self.particles.remove(particle)
        
class Particle:
    def __init__(self, x, y, rad, speed, color, dt):
        self.color = color
        self.dt = dt
        self.x = x
        self.y = y
        self.rad = rad
        ang = math.radians(random.randint(0, 360))
        self.dx = math.cos(ang) * speed
        self.dy = math.sin(ang) * speed
        self.rect = pygame.Rect(self.x, self.y, self.rad, self.rad)
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        
        
    def update(self):
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        self.rad -= self.dt
        self.rect.size = self.rad, self.rad
        
class StaticParticle:
    def __init__(self,screen, x, y, rad,color, life_time):
        self.x = x
        self.screen = screen
        self.y = y
        self.rad = rad
        self.life_time = life_time
        self.color = color
        
    def draw(self):
        pygame.draw.circle(self.screen, self.color, (self.x, self.y),self.rad)
        self.rad -= self.life_time
        