import math
import pygame
import modules

class AppMain:
    def __init__(self):
        pygame.init()
        width, height = 1000, 600
        dt = 1.0
        self.world = modules.World(width, height, dt)
        self.screen = pygame.display.set_mode((width, height))

        self.image1_pos = (100, 300)
        self.enemy_pos = (900, 300)
        self.image1 = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/Cannon/illust_white.jpg").convert_alpha()
        self.image1_rect = self.image1.get_rect(center=self.image1_pos)

        self.bullet_speed = 5
        self.bullet_power = 25
        self.bullets = []
        self.blocks = []
        self.hp_enemy = 50
        self.max_bounce = 8
        self.bounce_count = 0

        self.b_e = modules.BGMandEffectSound()
        self.collision_flag = False
        self.font = pygame.font.Font(None, 60)
        self.start_win = modules.StartWindow(self.world, self.screen, start=False)

    def add_block(self, screen, pos, width, height):
        block = modules.Block(screen, pos, width, height)
        self.blocks.append(block)

    def update(self):
        for b in self.bullets:
            b.update()
        self.bullets[:] = [b for b in self.bullets if b.is_alive]

    def draw_bullet(self):
        for b in self.bullets:
            b.draw(self.screen, (255, 255, 255))
        pygame.display.update()

    def add_bullet(self, image_pos, image_rect):
        dx = pygame.mouse.get_pos()[0] - image_pos[0]
        dy = pygame.mouse.get_pos()[1] - image_pos[1]
        angle = math.atan2(dy, dx)
        bullet_velocity = (self.bullet_speed * math.cos(angle), self.bullet_speed * math.sin(angle))
        b = modules.Bullet(list(image_rect.center), list(bullet_velocity), self.world, self.bullet_power, self.blocks,\
                                            postmove_strategy=modules.BounceOnBoundaryStrategy(self.max_bounce, self.bounce_count, self.blocks))
        self.bullets.append(b)

    def check_collision(self):
        for b in self.bullets:
            ldx = b.pos[0] - self.enemy_pos[0]
            ldy = b.pos[1] - self.enemy_pos[1]
            l_xy = math.sqrt(ldx ** 2 + ldy ** 2)
            if l_xy < 45:
                self.b_e.damages()
                b.is_alive = False
                self.hp_enemy += -b.power

    def run_shooting(self, i):
        pygame.display.set_caption("SHOOT IT")
        should_quit = False
        next_stage = False
        retry = False
        
        if i == 4:
            self.max_bounce = 18

        while True:
            self.screen.fill("black")
            level_text = self.font.render(f"level{i + 1}", True, 'white')
            self.screen.blit(level_text, (10, 10))
            max_bounce_text = self.font.render(f"Max Bounces:{self.max_bounce}", True, 'white')
            self.screen.blit(max_bounce_text, (180, 10))
            pygame.draw.rect(self.screen, 'white', (0, 0, self.world.width, self.world.height), width=1)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    should_quit = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    should_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if len(self.bullets) > 8:
                        break
                    else:
                        self.b_e.shoots()
                        self.add_bullet(self.image1_pos, self.image1_rect)
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                    retry = True
                    self.bullets.clear()
                    
            mouse_pos = pygame.mouse.get_pos()

            self.check_collision()

            if self.hp_enemy <= 0:
                
                next_stage = True
                
            if i == 0:
                self.add_block(self.screen, (600, 0), 100, 500)
                for block in self.blocks:
                    block.draw()
            elif i == 1:
                self.add_block(self.screen, (500, 0), 50, 500)
                self.add_block(self.screen, (700, 100), 50, 500)
                for block in self.blocks:
                    block.draw()
            elif i == 2:
                self.add_block(self.screen, (600, 50), 100, 500)
                self.add_block(self.screen, (750, 0), 100, 100)
                self.add_block(self.screen, (750, 500), 100, 100)
                for block in self.blocks:
                    block.draw()
            elif i == 3:
                for t in range(5):
                    self.add_block(self.screen, (600, 70 + 100 * t), 50, 70)
                self.add_block(self.screen, (700, 50), 50, 500)
                for block in self.blocks:
                    block.draw()
            elif i == 4:
                for t in range(5):
                    self.add_block(self.screen, (600,70 + 100 * t), 50, 70)
                self.add_block(self.screen, (800, 0), 30, 500)
                self.add_block(self.screen, (700, 100), 30, 500)
                for block in self.blocks:
                    block.draw()

            player1 = modules.Player(self.screen, self.image1_pos, mouse_pos, self.image1, self.image1_rect)
            player1()
            enemy = modules.Enemy(self.screen, self.enemy_pos, i)
            enemy.draw()

            self.update()
            self.draw_bullet()

            pygame.time.Clock().tick(60)

            if should_quit:
                pygame.quit()
                break

            if retry:
                retry = False
                continue

            if next_stage:
                if i == 4:
                    self.b_e.wins()
                    self.blocks.clear()
                    self.bullets.clear()
                    end_win = modules.EndWindow(self.world, self.screen)
                    end_win()
                    break
                else:
                    self.b_e.wins()
                    self.blocks.clear()
                    self.bullets.clear()
                    result_win = modules.ResultWindow(self.world, self.screen, i, result=False)
                    result_win()
                    self.hp_enemy = 200
                    break

    def run(self):
        self.b_e.bgms()
        self.start_win()
        for i in range(5):
            self.run_shooting(i)
            if i == 4:
                break

if __name__ == "__main__":
    app = AppMain()
    app.run()