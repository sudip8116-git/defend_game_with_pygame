from settings import *



class Window:
    def __init__(self, width, height, title, fps=60):
        self.res = self.width, self.height = width, height
        self.title = title
        self.fps = fps
        self.screen = pygame.display.set_mode(self.res, pygame.HWSURFACE)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(title)
        self.running = True

    def update(self):
        pygame.display.update()
        self.clock.tick(self.fps)

    def setBackColor(self, color):
        
        self.screen.fill(color)
       


