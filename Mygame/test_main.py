import math
import pygame

class BounceOnBoundaryStrategy:
    def __init__(self, max_bounces=3):
        self.max_bounces = max_bounces
        self.bounce_count = 0

    def __call__(self, b):
        pos = b.pos
        vel = b.vel
        width, height = b.world.width, b.world.height
        radius = b.radius
        
        if (pos[0] < 0 + radius and vel[0] < 0) or (pos[0] > width - radius and vel[0] > 0):
            vel[0] *= -1
            self.bounce_count += 1

        if (pos[1] < 0 + radius and vel[1] < 0) or (pos[1] > height - radius and vel[1] > 0):
            vel[1] *= -1
            self.bounce_count += 1

        if self.bounce_count >= self.max_bounces:
            b.is_alive = False

class World:
    def __init__(self, width, height, dt):
        self.width = width
        self.height = height
        self.dt = dt

class Player:
    def __init__(self, screen, pos, mouse_pos, image, image_rect, hp):
        self.screen = screen
        self.pos = pos
        self.mouse_pos = mouse_pos
        self.image = image
        self.image_rect = image_rect
        self.hp = hp
    
    def draw(self):
        dx = self.mouse_pos[0] - self.image_rect.centerx
        dy = self.mouse_pos[1] - self.image_rect.centery
        angle = math.degrees(math.atan2(dy, dx))
        rotated_image = pygame.transform.rotate(self.image, -angle)
        rotated_rect = rotated_image.get_rect(center=self.image_rect.center)
        self.screen.blit(rotated_image, rotated_rect.topleft)

class Enemy:
    def __init__(self, screen, pos, i, hp):
        self.screen = screen
        self.pos = pos
        self.enemy1_image = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/enemy/FatBat_30percent.png").convert_alpha()
        self.enemy2_image = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/enemy/slime_30percent.jpg").convert_alpha()
        self.enemy3_image = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/enemy/ghost.jpg").convert_alpha()
        self.enemy4_image = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/enemy/robot.jpg").convert_alpha()
        self.enemy5_image = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/enemy/human.jpg").convert_alpha()
        self.bullet_speed = 10
        self.i = i
        self.hp = hp
        
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
        
    def collision(self, bullets, c_flag, d_flag):
        for b in bullets:
            if self.hp <= 0:
                c_flag = False
                d_flag = True
            elif c_flag:
                self.hp -= b.power
                c_flag = False

class Bullet:
    def __init__(self, pos, vel, world, power, postmove_strategy=None):
        self.is_alive = True
        self.pos = pos
        self.vel = vel
        self.world = world
        self.radius = 5
        self.postmove_strategy = postmove_strategy
        self.power = power
        
    def update(self):
        self.pos[0] += self.vel[0] * self.world.dt
        self.pos[1] += self.vel[1] * self.world.dt
        if self.postmove_strategy is not None:
            self.postmove_strategy(self)
        else:
            self.update_after_move()
            
    def update_after_move(self):
        if self.pos[0] < 0 or self.pos[0] > self.world.width or self.pos[1] < 0 or self.pos[1] > self.world.height:
            self.is_alive = False
    
    def draw(self, screen, color):
        pygame.draw.circle(screen, color, (int(self.pos[0]), int(self.pos[1])), self.radius)

class StartWindow:
    def __init__(self, world, screen, start=False):
        self.world = world
        self.screen = screen
        self.start = start
    
    def __call__(self):
        while self.start is not True:
            font = pygame.font.Font(None, 60)
            start_text = font.render("Press SPACE to start game", True, 'white')
            self.screen.fill(pygame.Color("black"))
            self.screen.blit(start_text, (self.world.width // 2 - 260, self.world.height // 2))
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
    def __init__(self, world, screen, result=False):
        self.world = world
        self.screen = screen
        self.result = result
        
    def __call__(self):
        while self.result is not True:
            font = pygame.font.Font(None, 60)
            result_text = font.render("Well Done!\n\nPress SPACE to go next stage", True, 'comicsansms')
            result_rect = result_text.get_rect(center=(self.world.width//2, self.world.height//4))
            self.screen.fill(pygame.Color("black"))
            self.screen.blit(result_text, result_rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    print("level 2")
                    self.result = True
                    break
                
class EndWindow:
    def __init__(self, world, screen):
        self.world = world
        self.screen = screen
        self.font = pygame.font.Font(None, 60)
        
    def __call__(self):
        self.screen.fill(pygame.Color("gray"))
        score_text = self.font.render(f"Score: {self.world.score}", True, 'black')
        self.screen.blit(score_text, (self.world.width // 2 - 120, self.world.height // 2))
        pygame.display.update()
        pygame.time.delay(2500)
        pygame.quit()

class AppMain:
    def __init__(self):
        pygame.init()
        width, height = 1000, 600
        dt = 1.0
        self.world = World(width, height, dt)
        self.screen = pygame.display.set_mode((width, height))
        
        self.image1_pos = (100, 300)
        self.enemy_pos = (900, 300)
        self.image1 = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/Cannon/illust_white.jpg").convert_alpha()
        self.image1_rect = self.image1.get_rect(center=self.image1_pos)
        
        self.bullet_speed = 5
        self.bullet_power = 25
        self.bullets = []
        self.hp_player = 100
        self.hp_enemy = 100
        self.collision_flag = False
        self.triumph_flag = False

        self.start_win = StartWindow(self.world, self.screen, start=False)
        self.result_win = ResultWindow(self.world, self.screen, result=False)
        self.end_win = EndWindow(self.world, self.screen)

    def update(self):
        for b in self.bullets:
            b.update()
        self.bullets[:] = [b for b in self.bullets if b.is_alive]
        
    def draw(self):
        for b in self.bullets:
            b.draw(self.screen, (255,255,255))
        pygame.display.update()
        
    def add_bullet(self, image_pos, image_rect):
        dx = pygame.mouse.get_pos()[0] - image_pos[0]
        dy = pygame.mouse.get_pos()[1] - image_pos[1]
        angle = math.atan2(dy, dx)
        bullet_velocity = (self.bullet_speed * math.cos(angle), self.bullet_speed * math.sin(angle))
        b = Bullet(list(image_rect.center), list(bullet_velocity), self.world, self.bullet_power,\
                                                    postmove_strategy=BounceOnBoundaryStrategy())
        self.bullets.append(b)
        
    def check_collision(self, enemy_pos):
        for b in self.bullets:
            ldx = b.pos[0] - enemy_pos[0] 
            ldy = b.pos[1] - enemy_pos[1]
            distance = math.sqrt(ldx**2 + ldy**2)
            if distance < 50:
                self.collision_flag = True

    def triumph(self):
        image = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/effect/explode.png")
        image_rect = image.get_rect(center=self.enemy_pos)
        self.screen.blit(image, image_rect.topleft)
        defeat_sound = pygame.mixer.Sound("8bit爆発3.mp3")  # サウンドをロード
        defeat_sound.play()  # サウンドを再生
        
    def run_shooting(self, i):
        pygame.display.set_caption("Pygame Shooting Example")
        while True:
            self.screen.fill("black")
            should_quit = False
            next_stage = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    should_quit = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    should_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 左クリックで弾発射
                    self.add_bullet(self.image1_pos, self.image1_rect)
                
            mouse_pos = pygame.mouse.get_pos()
            
            player1 = Player(self.screen, self.image1_pos, mouse_pos, self.image1, self.image1_rect, self.hp_player)
            player1.draw()
            enemy = Enemy(self.screen, self.enemy_pos, i, self.hp_enemy)
            enemy.draw()
            
            for b in self.bullets:
                b.update()
                self.check_collision(self.enemy_pos)
                
            if self.collision_flag:
                enemy.collision(self.bullets, self.collision_flag, self.triumph_flag)
                if self.triumph_flag:
                    self.triumph()
                    self.triumph_flag = False
                    next_stage = True
            
            self.update()
            self.draw()
            
            pygame.time.Clock().tick(60)
            
            if should_quit:
                pygame.quit()
                
            if next_stage:
                break
        
    def run(self):
        self.start_win()
        i = 0
        while i < 6:
            self.run_shooting(i)
            self.result_win()
            
            if i == 6:
                self.end_win()
            i += 1
        
if __name__ == "__main__":
    app = AppMain()
    app.run()
