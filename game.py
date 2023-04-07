
from PygameBasic import *
from enemy import EnemyManger
from func import crossHair
from settings import *
from player import *
from particleSystem import ParticleSystem, StaticParticle
from PygameUI import *



pygame.init()


class Game(Window):
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, TITLE)
        pygame.mouse.set_visible(False)

    def run(self):
        self.setup()
        while self.running:
            self.eventManger()
            
            if self.player.health <= 0:
                self.onPlayerDie()
                self.update()
                super().update()
                continue
            
            if self.game_pause:
                self.pauseScreen()
            else:
                self.setBackColor(BACKGROUND_COLOR)
                self.draw()



            self.update()
            super().update()

        self.running = True
        pygame.mouse.set_visible(True)

    def onPlayerDie(self):
        pygame.mouse.set_visible(True)
        self.setBackColor('white')
        self.show_score_text.changeText(f"Your Score : {self.score}")
        self.player_die_text.draw()
        self.show_score_text.draw()
        self.quit_button.draw()

    def pauseScreen(self):
        self.setBackColor('white')
        self.game_pause_text.draw()
        self.continue_button.draw()
        self.quit_button.draw()

    def setup(self):
        self.player = Player(self.screen, 30)
        self.enemyManager = EnemyManger(self.screen)
        self.fps_text = Text(self.screen, "Fps : 0", 50,
                             HEIGHT - 20, bold=True, color='green', font_size=25, font_number=20)
        self.player_health_bar = PlayerHealthBar(
            self.screen, WIDTH * 0.4, HEIGHT - 40, WIDTH * 0.2, 30)
        self.particle_systems = []
        self.static_particle_systems = []
        self.score = 0
        self.score_text = Text(self.screen, "Score : 0", WIDTH *
                               0.8, HEIGHT - 30, font_size=30, bold=True, font_number=32)
        self.curent_score = 0

        self.pause_btn = Button(self.screen, WIDTH - 60, 25, 100, 40, "Pause",
                                base_color=(200, 100, 200), border=True, bold=True, hover_color='green')

        self.game_pause = False

        self.game_pause_text = Text(self.screen, "Game Paused", WIDTH //
                                    2, HEIGHT * 0.3, font_size=70, bold=True, font_number=25)

        self.continue_button = Button(self.screen, WIDTH // 2, HEIGHT * 0.5, 200, 50, "Continue", border=True,
                                      bold=True, font_size=30, base_color=(40, 50, 120), color="white", hover_color=(120, 120, 120))

        self.quit_button = Button(self.screen, WIDTH // 2, HEIGHT * 0.8, 200, 50, "Main Menu", border=True,
                                  bold=True, font_size=30, base_color=(40, 50, 120), color="white", hover_color=(120, 120, 120))
        
        
        self.player_die_text = Text(self.screen, "You Failed", WIDTH // 2, HEIGHT * 0.3, font_size=70, bold=True)
        
        self.show_score_text = Text(self.screen, "Your Score : ", WIDTH//2, HEIGHT * 0.5, font_size = 50, bold=True)
        
        
     

        
        

    def eventManger(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

    def draw(self):
        self.player.draw()
        self.player.update()

        for bull in self.player.bullets:
            bull.draw()
            if(bull.x < - 10 or bull.x > WIDTH + 10 or bull.y < - 10 or bull.y > HEIGHT + 10):
                self.player.bullets.remove(bull)
            # enemy collide with enemy
            enemy_coll_list = bull.rect.collidelistall(
                self.enemyManager.enemies)

            if(enemy_coll_list):
                self.enemyManager.enemies[enemy_coll_list[0]].takeDamage(
                    bull.damage_amount)
                static_particle = StaticParticle(
                    self.screen, bull.x, bull.y, random.randint(4, 10), 'yellow', 0.5)
                self.static_particle_systems.append(static_particle)
                self.player.bullets.remove(bull)

        for ene in self.enemyManager.enemies:
            ene.draw()
            if(ene.health <= 0):
                self.enemyManager.enemies.remove(ene)
                self.score += ene.damage_when_die
                self.particle_systems.append(ParticleSystem(
                    self.screen, ene.x, ene.y, ene.rad, 20, 15, 0.1))

        self.enemyManager.update()

        self.fps_text.draw()
        self.fps_text.changeText("FPS : " + str(int(self.clock.get_fps())))

        # collision detection
        # player with enemy

        ene_coll_list = self.player.rect.collidelistall(
            self.enemyManager.enemies)
        for _ene_num in ene_coll_list:
            damage_val = self.enemyManager.enemies[_ene_num].damage_when_die

            self.player.health -= damage_val
            self.player_health_bar.setVal(self.player.health)
            ene = self.enemyManager.enemies[_ene_num]
            self.particle_systems.append(ParticleSystem(
                self.screen, ene.x, ene.y, ene.rad, 20, 15, 0.1))

            self.enemyManager.enemies.pop(_ene_num)  # destroy enemy

        # player bullet with enemy
        self.player_health_bar.draw()

        # particle system
        for particle_system in self.particle_systems:
            particle_system.draw()
            if(len(particle_system.particles) == 0):
                self.particle_systems.remove(particle_system)

        for static_particle in self.static_particle_systems:
            static_particle.draw()
            if static_particle.rad <= 0:
                self.static_particle_systems.remove(static_particle)

        self.score_text.draw()

        self.curent_score = lerp(self.curent_score, self.score, 0.1)
        self.score_text.changeText(f"Score : {int(self.curent_score)}")

        self.pause_btn.draw()

        crossHair(self.screen)

    
    
    def update(self):
        m_pos = pygame.mouse.get_pos()
        if isMousePressed():
            if self.pause_btn.rect.collidepoint(m_pos):
                self.game_pause = True
                pygame.mouse.set_visible(True)
            if self.continue_button.rect.collidepoint(m_pos):
                self.game_pause = False
                pygame.mouse.set_visible(False)
                
            if self.quit_button.rect.collidepoint(m_pos):
                self.running = False

    def startGame(self):
        pygame.mouse.set_visible(True)
        self.main_menu_text = Text(
            self.screen, "Tower Defence 2D", WIDTH//2, HEIGHT * 0.3, font_size=70, bold=True)
        self.blank_surface = pygame.Surface(self.res)
        self.start_game_button = Button(
            self.screen, WIDTH//2, HEIGHT * 0.5, 200, 50, "Start Game", bold=True, font_size=30, border=True, hover_color='green')
        
        self.exit_game_button = Button(
            self.screen, WIDTH//2, HEIGHT * 0.6, 200, 50, "Exit Game", bold=True, font_size=30, border=True, hover_color='red')

        blank_alpha = 255
        self.blank_surface.set_alpha(blank_alpha)
        self.start_game = False
        while self.running:
            self.eventManger()
            self.setBackColor('white')

            self.main_menu_text.draw()

            self.start_game_button.draw()
            self.exit_game_button.draw()

            m_pos = pygame.mouse.get_pos()
            if isMousePressed():
                if self.start_game_button.rect.collidepoint(m_pos):
                    self.run()

                if self.exit_game_button.rect.collidepoint(m_pos):
                    self.running = False

            if blank_alpha >= 0:
                blank_alpha -= 1
                self.blank_surface.set_alpha(blank_alpha)
            self.blank_surface.fill('black')
            self.screen.blit(self.blank_surface, (0, 0))

            super().update()



