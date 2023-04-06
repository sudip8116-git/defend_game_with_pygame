
from PygameUI import Text
from func import getRandomColor
from settings import *

class Enemy:
    def __init__(self,screen, x, y):
        self.screen = screen
        self.x = x
        self.y = y
        self.rad = random.randint(10, 50)
        self.color = getRandomColor()
        self.speed = random.randint(10, 20) / 10
        ang = math.atan2((HEIGHT // 2) - self.y, (WIDTH//2) - self.x)
        self.dx = round(math.cos(ang), 2) * self.speed
        self.dy = round(math.sin(ang), 2) * self.speed
        self.rect = pygame.Rect(self.x, self.y, 0, 0)
        self.health = self.rad
        self.damage_when_die = self.health // 2
        self.health_text = Text(self.screen, str(self.health), self.x, self.y, font_number = 25, bold=True,font_size = self.health, color='white')
        
    def draw(self):
        self.rect = pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.rad)
        self.rect = pygame.draw.circle(self.screen, 'black', (self.x, self.y), self.rad, 1)
        
        self.x += self.dx
        self.y += self.dy
        
        self.health_text.draw()
        self.health_text.changePos(self.x, self.y)
        self.health_text.changeText(str(self.health))
    
    def takeDamage(self, val):
        self.health -= val
        
            
    
        
class EnemyManger:
    def __init__(self, screen):
        self.enemies = []
        self.pre_spawn_time = 0
        self.screen = screen
        self.next_spawn_time = random.randint(10, 50) / 10
        
        
    def update(self):
        time = pygame.time.get_ticks() / 1000
        if(time > self.pre_spawn_time + self.next_spawn_time):
            x, y = getRandomPos()
            en = Enemy(self.screen, x, y)
            self.enemies.append(en)
            self.next_spawn_time = random.randint(10, 50) / 10
            self.pre_spawn_time = time
    
    
        


def getRandomPos():

    rad = random.randint(int(HEIGHT * 0.75), int(WIDTH * 0.75))
    ang = math.radians(random.randint(0, 360))
    x = WIDTH // 2 + math.cos(ang) * rad
    y = HEIGHT // 2 + math.sin(ang) * rad
    return x, y