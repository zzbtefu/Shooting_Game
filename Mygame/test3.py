import math
import pygame

class BounceOnBoundaryStrategy:
    def __init__(self, max_bounces, bounce_count):
        self.max_bounces = max_bounces
        self.bounce_count = bounce_count

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


class BounceOnBoxStrategy:
    def __init__(self, max_bounces, bounce_count):
        self.max_bounces = max_bounces
        self.bounce_count = bounce_count

    def __call__(self, b):
        radius = b.radius
        pos = b.pos
        vel = b.vel
        left_wall = b.block.pos[0]
        right_wall = b.block.pos[0] + b.block.width
        top_wall = b.block.pos[1]
        bottom_wall = b.block.pos[1] + b.block.height

        if (pos[0] < left_wall < pos[0] + radius and top_wall < pos[1] < bottom_wall and vel[0] > 0) \
                or (pos[0] - radius < right_wall < pos[0] and top_wall < pos[1] < bottom_wall and vel[0] < 0):
            vel[0] *= -1
            print("hi")
            self.bounce_count += 1

        if (pos[1] < top_wall < pos[1] + radius and left_wall < pos[0] < right_wall and vel[1] > 0) \
                or (pos[1] - radius < bottom_wall < pos[1] and left_wall < pos[0] < right_wall and vel[1] < 0):
            vel[1] *= -1
            print("hi")
            self.bounce_count += 1

        if self.bounce_count >= self.max_bounces:
            b.is_alive = False

class World:
    def __init__(self, width, height, dt):
        self.width = width
        self.height = height
        self.dt = dt

class Block:
    def __init__(self, screen, pos, i):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.width = 100
        self.height = 500
        self.pos = pos
        self.i = i

    def draw(self):
        if self.i == 0:
            pygame.draw.rect(self.screen, 'white', (self.pos[0], self.pos[1], self.width, self.height), width=1)
        else:
            pass

class Player():
    def __init__(self, screen, pos, mouse_pos, image, image_rect, hp):
        self.screen = screen
        self.pos = pos
        self.mouse_pos = mouse_pos
        self.image = image
        self.image_rect = image_rect
        self.hp = hp
        
        dx = self.mouse_pos[0] - self.image_rect.centerx
        dy = self.mouse_pos[1] - self.image_rect.centery
        angle = math.degrees(math.atan2(dy, dx))
        self.rotated_image = pygame.transform.rotate(self.image, -angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.image_rect.center)
    
    def __call__(self):
        self.screen.blit(self.rotated_image, self.rotated_rect.topleft)

class Enemy:
    def __init__(self, screen, pos, i, hp):
        self.screen = screen
        self.pos = pos
        self.hp = hp
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
    def __init__(self, pos, vel, world, power, block, postmove_strategy=None, reflect_box=None):
        pygame.sprite.Sprite.__init__(self)
        self.is_alive = True
        self.pos = pos
        self.vel = vel
        self.world = world
        self.radius = 5
        self.postmove_strategy = postmove_strategy
        self.reflect_box = reflect_box
        self.power = power
        self.block = block
        
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
        self.block = Block(self.screen, pos=(0, 0), i=0)
        self.hp_player = 100
        self.hp_enemy = 50
        self.max_bounce = 4
        self.bounce_count = 0
        
        self.collision_flag = False
        self.font = pygame.font.Font(None, 60)
        self.start_win = StartWindow(self.world, self.screen, start=False)

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
        b = Bullet(list(image_rect.center), list(bullet_velocity), self.world, self.bullet_power, block, \
           reflect_box=BounceOnBoxStrategy(self.max_bounce, self.bounce_count), \
           postmove_strategy=BounceOnBoundaryStrategy(self.max_bounce, self.bounce_count))

        self.bullets.append(b)
    
    def check_collision(self):
        for b in self.bullets:
            ldx = b.pos[0] - self.enemy_pos[0]
            ldy = b.pos[1] - self.enemy_pos[1]
            l_xy = math.sqrt(ldx**2 + ldy**2)
            if l_xy < 45:
                b.is_alive = False
                self.hp_enemy += -b.power

    def run_shooting(self, i):
        pygame.display.set_caption("SHOOT IT")
        should_quit = False
        next_stage = False

        while True:
            self.screen.fill("black")
            level_text = self.font.render(f"level{i+1}", True, 'white')
            self.screen.blit(level_text, (10, 10))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    should_quit = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    should_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.add_bullet(self.image1_pos, self.image1_rect)

            mouse_pos = pygame.mouse.get_pos()
            
            self.check_collision()
            
            if self.hp_enemy <= 0:
                next_stage = True

            block = Block(self.screen, (600, 0), i)
            block.draw()

            player1 = Player(self.screen, self.image1_pos, mouse_pos, self.image1, self.image1_rect, self.hp_player)
            player1()
            enemy = Enemy(self.screen, self.enemy_pos, i, self.hp_enemy)
            enemy.draw()

            self.update()
            self.draw()

            pygame.time.Clock().tick(60)

            if should_quit:
                pygame.quit()
                break
            
            if next_stage:
                if i == 4:
                    end_win = EndWindow(self.world, self.screen)
                    end_win()
                    break
                else:
                    result_win = ResultWindow(self.world, self.screen, i, result=False)
                    result_win()
                    self.hp_enemy = 200
                    break
                
    def run(self):
        self.start_win()
        for i in range(5):
            self.run_shooting(i)
            if i == 4:
                break

if __name__ == "__main__":
    app = AppMain()
    app.run()
