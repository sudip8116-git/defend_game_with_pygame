from PygameUI import Text
from settings import *
from func import lerp




class Player:
    def __init__(self, screen, rad):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.screen = screen
        self.cir_color = 'green'
        self.rad = rad
        self.rect = None
        self.pos = self.x, self.y
        self.cannon_length = self.rad + 5
        self.cannon_color = 'black'
        self.cannon_width = 5
        self.fire_pos = self.x, self.y
        self.fire_rate = 100
        self.pre_fire_time = 0
        self.ang = 0
        self.bullets = []
        self.health = 100
 
    def draw(self):
        self.rect = pygame.draw.circle(
            self.screen, self.cir_color, self.pos, self.rad)
        pygame.draw.line(self.screen, self.cannon_color,
                         self.pos, self.fire_pos, self.cannon_width)

        pygame.draw.circle(self.screen, 'red', self.fire_pos, 5)
        pygame.draw.circle(self.screen, 'yellow', self.pos, self.rad//2)

    def update(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.ang = math.atan2(
            (self.mouse_pos[1] - self.y), (self.mouse_pos[0] - self.x))
        self.fire_pos = self.x + self.cannon_length * \
            math.cos(self.ang), self.y + \
            self.cannon_length * math.sin(self.ang)

        time = pygame.time.get_ticks()
        if(time > self.pre_fire_time + self.fire_rate):
            self.fire()
            self.pre_fire_time = time

    def fire(self):
        bull = Bullet(self.screen, self.fire_pos[0], self.fire_pos[1], 3, PLAYER_BULLET_COLOR, round(
            math.cos(self.ang), 2), round(math.sin(self.ang), 2), 4)

        self.bullets.append(bull)


class Bullet:
    def __init__(self, screen, x, y, rad, col, dx, dy, speed):
        self.screen = screen
        self.x = x
        self.y = y
        self.rad = rad
        self.col = col
        self.speed = speed
        self.dx = dx * self.speed
        self.dy = dy * self.speed
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.damage_amount = 2

    def draw(self):
        self.rect = pygame.draw.circle(
            self.screen, self.col, (self.x, self.y), self.rad)
        self.x += self.dx
        self.y += self.dy


class PlayerHealthBar:
    def __init__(self, screen, x, y, w, h):
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.curr_color = pygame.Color(0, 255, 0)
        self.health_text = Text(self.screen, "100", self.x + self.w / 2,
                                self.y + self.h / 2, bold=True, font_size=30, font_number=30)
        self.current_val = 100
        self.target_val = 100
        self.w_ratio = self.w / self.current_val
        self.pre_width = self.w
        self.color_vals = []
        r, g, b = 255, 0, 0
        for i in range(100):
            if (i <= 50):
                g += 5
            else:
                r -= 5
            self.color_vals.append((int(r), int(g), b))

    def draw(self):
        pygame.draw.rect(self.screen, self.curr_color,
                         (self.x, self.y, self.w, self.h))
        pygame.draw.rect(self.screen, 'black',
                         (self.x, self.y, self.pre_width, self.h), 2)
        self.health_text.draw()
        if (self.current_val >= 0):
            self.current_val = lerp(self.current_val, self.target_val, 0.1)

        self.health_text.changeText(f"{int(self.current_val)}%")
        self.w = self.current_val * self.w_ratio

        self.curr_color = pygame.Color.lerp(self.curr_color, self.color_vals[int(self.current_val) - 1], 0.1)

    def setVal(self, val):
        self.target_val = val

