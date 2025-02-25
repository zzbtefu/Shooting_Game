import math
import pygame

class BounceOnBoundaryStrategy:
    def __init__(self, max_bounces, bounce_count, blocks):
        self.max_bounces = max_bounces
        self.bounce_count = bounce_count
        self.blocks = blocks
        self.b_e = BGMandEffectSound()

    def __call__(self, b):
        width, height = b.world.width, b.world.height
        radius = b.radius

        if (b.pos[0] > width - radius and b.vel[0] > 0):
            b.vel[0] *= -1
            self.b_e.bounces()
            self.bounce_count += 1

        if (b.pos[1] < 0 + radius and b.vel[1] < 0) or (b.pos[1] > height - radius and b.vel[1] > 0):
            b.vel[1] *= -1
            self.b_e.bounces()
            self.bounce_count += 1
        
        if (b.pos[0] < 0 + radius and b.vel[0] < 0):
            self.bounce_count += 1
            
        for block in self.blocks:
            left_wall = block.pos[0]
            right_wall = block.pos[0] + block.width
            top_wall = block.pos[1]
            bottom_wall = block.pos[1] + block.height
            if (b.pos[0] < left_wall < b.pos[0] + radius and top_wall < b.pos[1] < bottom_wall and b.vel[0] > 0) \
                    or (b.pos[0] - radius < right_wall < b.pos[0] and top_wall < b.pos[1] < bottom_wall and b.vel[0] < 0):
                b.vel[0] *= -1
                self.b_e.bounces()
                self.bounce_count += 1

            if (b.pos[1] < top_wall < b.pos[1] + radius and left_wall < b.pos[0] < right_wall and b.vel[1] > 0) \
                    or (b.pos[1] - radius < bottom_wall < b.pos[1] and left_wall < b.pos[0] < right_wall and b.vel[1] < 0):
                b.vel[1] *= -1
                self.b_e.bounces()
                self.bounce_count += 1

        if self.bounce_count >= self.max_bounces:
            b.is_alive = False

class World:
    def __init__(self, width, height, dt):
        self.width = width
        self.height = height
        self.dt = dt

class BGMandEffectSound:
    def __init__(self):
        pygame.mixer.init(frequency = 44100)    # 初期設定
        self.explode = pygame.mixer.Sound("C:/cs1_devenv_ver20230901/cs1/assets/effect/8bit爆発3.mp3")     # 音楽ファイルの読み込み
        self.bounce = pygame.mixer.Sound("C:/cs1_devenv_ver20230901/cs1/assets/effect/短い音-プイ.mp3")
        self.shoot = pygame.mixer.Sound("C:/cs1_devenv_ver20230901/cs1/assets/effect/8bitショット1_speed_200.mp3")
        self.win = pygame.mixer.Sound("C:/cs1_devenv_ver20230901/cs1/assets/effect/ジャジャーン3.mp3")
        self.damage = pygame.mixer.Sound("C:/cs1_devenv_ver20230901/cs1/assets/effect/打撃2.mp3")
        pygame.mixer.music.set_volume(0.5)
        
    def explodes(self):
        self.explode.play()
        
    def bounces(self):
        self.bounce.play()
        
    def shoots(self):
        self.shoot.play()
        
    def wins(self):
        self.win.play()
        
    def damages(self):
        self.damage.play()
    
    def bgms(self):
        pygame.mixer.music.load("C:/cs1_devenv_ver20230901/cs1/assets/bgm/Future_1.mp3")
        pygame.mixer.music.play()

class Block:
    def __init__(self, screen, pos, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.width = width
        self.height = height
        self.pos = pos

    def draw(self):
        pygame.draw.rect(self.screen, 'white', (self.pos[0], self.pos[1], self.width, self.height), width=1)

class Player():
    def __init__(self, screen, pos, mouse_pos, image, image_rect):
        self.screen = screen
        self.pos = pos
        self.mouse_pos = mouse_pos
        self.image = image
        self.image_rect = image_rect
        
        dx = self.mouse_pos[0] - self.image_rect.centerx
        dy = self.mouse_pos[1] - self.image_rect.centery
        angle = math.degrees(math.atan2(dy, dx))
        self.rotated_image = pygame.transform.rotate(self.image, -angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.image_rect.center)
    
    def __call__(self):
        self.screen.blit(self.rotated_image, self.rotated_rect.topleft)

class Enemy:
    def __init__(self, screen, pos, i):
        self.screen = screen
        self.pos = pos
        self.enemy1_image = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/enemy/FatBat_30percent.png").convert_alpha()
        self.enemy2_image = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/enemy/slime_30percent.jpg").convert_alpha()
        self.enemy3_image = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/enemy/ghost_30percent.png").convert_alpha()
        self.enemy4_image = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/enemy/robot_30percent.png").convert_alpha()
        self.enemy5_image = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/enemy/human_40percent.png").convert_alpha()
        self.bullet_speed = 10
        self.i = i
        
    def draw(self):
        if self.i == 0:
            image_rect = self.enemy1_image.get_rect(center=self.pos)
            self.screen.blit(self.enemy1_image, image_rect.topleft)
        elif self.i == 1:
            image_rect = self.enemy2_image.get_rect(center=self.pos)
            self.screen.blit(self.enemy2_image, image_rect.topleft)
        elif self.i == 2:
            image_rect = self.enemy3_image.get_rect(center=self.pos)
            self.screen.blit(self.enemy3_image, image_rect.topleft)
        elif self.i == 3:
            image_rect = self.enemy4_image.get_rect(center=self.pos)
            self.screen.blit(self.enemy4_image, image_rect.topleft)
        elif self.i == 4:
            image_rect = self.enemy5_image.get_rect(center=self.pos)
            self.screen.blit(self.enemy5_image, image_rect.topleft)

class Bullet:
    def __init__(self, pos, vel, world, power, blocks, postmove_strategy=None, reflect_box=None):
        self.is_alive = True
        self.pos = pos
        self.vel = vel
        self.world = world
        self.radius = 5
        self.postmove_strategy = postmove_strategy
        self.reflect_box = reflect_box
        self.power = power
        self.blocks = blocks
        
    def update(self):
        self.pos[0] += self.vel[0] * self.world.dt
        self.pos[1] += self.vel[1] * self.world.dt
        if self.postmove_strategy is not None:
            self.postmove_strategy(self)
        elif self.reflect_box is not None:
            self.reflect_box(self)
    
    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (int(self.pos[0]), int(self.pos[1])), self.radius)
        
class StartWindow:
    def __init__(self, world, screen, start=False):
        self.world = world
        self.screen = screen
        self.start = start
    
    def __call__(self):
        while self.start is not True:
            font1 = pygame.font.Font(None, 100)
            font2 = pygame.font.Font(None, 50)
            start1_text = font1.render("SHOOT IT", True, 'White')
            start2_text = font2.render("Press SPACE to start game", True, 'white')
            start1_rect = start1_text.get_rect(center=(self.world.width//2, self.world.height//3))
            start2_rect = start2_text.get_rect(center=(self.world.width//2, self.world.height*2.2//3))
            self.screen.fill(pygame.Color("black"))
            self.screen.blit(start1_text, start1_rect)
            self.screen.blit(start2_text, start2_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    print("--------GAME START--------")
                    self.start = True
                    break

class ResultWindow:
    def __init__(self, world, screen, i, result=False):
        pygame.init()
        self.world = world
        self.screen = screen
        self.result = result
        self.i = i
        
    def __call__(self):
        while self.result is not True:
            font1 = pygame.font.Font(None, 100)
            font2 = pygame.font.Font(None, 50)
            result_text = font1.render("Well Done!", True, 'white')
            result_rect = result_text.get_rect(center=(self.world.width//2, self.world.height//3))
            result2_text = font2.render("Press SPACE to go next stage", True, 'white')
            result2_rect = result2_text.get_rect(center=(self.world.width//2, self.world.height*2//3))
            self.screen.fill(pygame.Color("black"))
            self.screen.blit(result_text, result_rect)
            self.screen.blit(result2_text, result2_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    print(f"level {self.i + 2}")
                    self.result = True
                    break
                
class EndWindow:
    def __init__(self, world, screen):
        self.world = world
        self.screen = screen
        self.font = pygame.font.Font(None, 60)
        
    def __call__(self):
        self.screen.fill(pygame.Color("black"))
        end_text = self.font.render("Nice Work!", True, 'white')
        end2_text = self.font.render("See you next time!", True, 'white')
        end_rect = end_text.get_rect(center=(self.world.width//2, self.world.height//3))
        end2_rect = end2_text.get_rect(center=(self.world.width//2, self.world.height*2//3))
        self.screen.blit(end_text, end_rect)
        self.screen.blit(end2_text, end2_rect)
        pygame.display.update()
        pygame.time.delay(2500)
        pygame.quit()
