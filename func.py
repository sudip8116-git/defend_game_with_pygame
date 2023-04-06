
from settings import *


def crossHair(screen):
    pygame.draw.circle(screen, 'red', pygame.mouse.get_pos(), 10, 2)
    
def getRandomColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    return (r, g, b)

def lerp(_from, _to , time):
    return _from + (_to - _from) * time 