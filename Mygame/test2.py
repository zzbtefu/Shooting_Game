import math
import pygame

class BounceOnBoundaryStrategy:
    def __init__(self, max_bounces=2):
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

class BounceOnBoxBoundaryStrategy:
    def __call__(self, b, box):
        pos = b.pos
        vel = b.vel
        width, height = box.width, box.height
        radius = b.radius

        if (pos[0] < box.pos[0] + radius and vel[0] < 0) or (pos[0] > box.pos[0] + width - radius and vel[0] > 0):
            vel[0] *= -1

        if (pos[1] < box.pos[1] + radius and vel[1] < 0) or (pos[1] > box.pos[1] + height - radius and vel[1] > 0):
            vel[1] *= -1

class BounceBox:
    def __init__(self, pos, width, height, app):
        self.pos = pos
        self.width = width
        self.height = height
        self.start_pos = None
        self.willdraw_rect = None
        self.draw_rect = None
        self.app = app
        self.bounce_strategy = BounceOnBoxBoundaryStrategy()

    def check_collision(self, bullet):
        if self.draw_rect is not None:
            rect_left = min(self.draw_rect[0][0], self.draw_rect[1][0])
            rect_right = max(self.draw_rect[0][0], self.draw_rect[1][0])
            rect_top = min(self.draw_rect[0][1], self.draw_rect[1][1])
            rect_bottom = max(self.draw_rect[0][1], self.draw_rect[1][1])

            return rect_left < bullet.pos[0] < rect_right and rect_top < bullet.pos[1] < rect_bottom

        return False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.start_pos = event.pos
        elif event.type == pygame.MOUSEMOTION and self.start_pos is not None:
            current_pos = event.pos
            self.willdraw_rect = [list(self.start_pos), list(current_pos)]
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            current_pos = event.pos
            self.willdraw_rect = None
            self.draw_rect = [list(self.start_pos), list(current_pos)]
            self.start_pos = None

    def draw(self, screen):
        if self.willdraw_rect is not None:
            pygame.draw.line(screen, (255, 255, 255), self.willdraw_rect[0], (self.willdraw_rect[1][0], self.willdraw_rect[0][1]), 1)
            pygame.draw.line(screen, (255, 255, 255), (self.willdraw_rect[1][0], self.willdraw_rect[0][1]), self.willdraw_rect[1], 1)
            pygame.draw.line(screen, (255, 255, 255), self.willdraw_rect[1], (self.willdraw_rect[0][0], self.willdraw_rect[1][1]), 1)
            pygame.draw.line(screen, (255, 255, 255), (self.willdraw_rect[0][0], self.willdraw_rect[1][1]), self.willdraw_rect[0], 1)
        elif self.draw_rect is not None:
            dx = self.draw_rect[1][0] - self.draw_rect[0][0]
            dy = self.draw_rect[1][1] - self.draw_rect[0][1]
            ldx = abs(dx)
            ldy = abs(dy)
            if dx >= 0 and dy >= 0:
                pygame.draw.rect(screen, (255, 255, 255), (self.draw_rect[0][0], self.draw_rect[0][1], ldx, ldy))
            elif dx >= 0 and dy < 0:
                pygame.draw.rect(screen, (255, 255, 255), (self.draw_rect[0][0], self.draw_rect[1][1], ldx, ldy))
            elif dx < 0 and dy < 0:
                pygame.draw.rect(screen, (255, 255, 255), (self.draw_rect[1][0], self.draw_rect[1][1], ldx, ldy))
            elif dx < 0 and dy >= 0:
                pygame.draw.rect(screen, (255, 255, 255), (self.draw_rect[1][0], self.draw_rect[0][1], ldx, ldy))

    def apply_bounce_strategy(self, bullet):
        self.bounce_strategy(bullet, self)


class World:
    def __init__(self, width, height, dt):
        self.width = width
        self.height = height
        self.dt = dt

class Player:
    def __init__(self, screen, pos, mouse_pos, image, image_rect, image1, image1_rect):
        self.screen = screen
        self.pos = pos
        self.mouse_pos = mouse_pos
        self.image = image
        self.image_rect = image_rect
        self.image1 = image1
        self.image1_rect = image1_rect
        
        dx = self.mouse_pos[0] - self.image_rect.centerx
        dy = self.mouse_pos[1] - self.image_rect.centery
        angle = math.degrees(math.atan2(dy, dx))
        self.rotated_image = pygame.transform.rotate(self.image1, -angle)
        self.rotated_rect = self.rotated_image.get_rect(center=self.image_rect.center)
    
    def __call__(self):
        self.screen.blit(self.rotated_image, self.rotated_rect.topleft)

class Bullet:
    def __init__(self, pos, vel, world, postmove_strategy=None):
        self.is_alive = True
        self.pos = pos
        self.vel = vel
        self.world = world
        self.radius = 5
        self.postmove_strategy = postmove_strategy
        
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
            start_text = font.render("Press SPACE to start game", True, 'maroon')
            self.screen.fill(pygame.Color("gray"))
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
                    self.start=True
                    break

class AppMain:
    def __init__(self):
        pygame.init()
        width, height = 1000, 600
        dt = 1.0
        self.screen = pygame.display.set_mode((width, height))
        self.image1_pos = (200, 300)
        self.image2_pos = (800, 300)
        self.image1 = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/Cannon/illust_white.jpg").convert_alpha()
        self.image2 = pygame.image.load("C:/cs1_devenv_ver20230901/cs1/assets/Cannon/illust_white_reversed.jpg").convert_alpha()
        self.image1_rect = self.image1.get_rect(center=self.image1_pos)
        self.image2_rect = self.image2.get_rect(center=self.image2_pos)
        self.bullet_speed = 5
        self.world = World(width, height, dt)
        self.white = (255, 255, 255)
        self.black = (0, 0, 0)
        self.bullets = []
        self.bounce_box = BounceBox((0, 0), 0, 0, self)

        self.start_win = StartWindow(self.world, self.screen, start=False)

    def update(self):
        for b in self.bullets:
            b.update()
            self.bounce_box.check_collision(b)
        self.bullets[:] = [b for b in self.bullets if b.is_alive]
        
    def draw_bullet(self):
        for b in self.bullets:
            b.draw(self.screen, self.white)
        pygame.display.update()
        
    def add_bullet(self, image_pos, image_rect, bullet):
        dx = pygame.mouse.get_pos()[0] - image_pos[0]
        dy = pygame.mouse.get_pos()[1] - image_pos[1]
        angle = math.atan2(dy, dx)
        bullet_velocity = (self.bullet_speed * math.cos(angle), self.bullet_speed * math.sin(angle))
        bullet.pos = list(image_rect.center)
        bullet.vel = list(bullet_velocity)
        self.bullets.append(bullet)


    def run_shooting(self):
        pygame.display.set_caption("Pygame Shooting Example")
        i = 0
        while True:
            self.screen.fill("black")
            should_quit = False
            if i % 2 == 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        should_quit = True
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        should_quit = True
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # 弾を追加する前に新しい弾を生成
                        b = Bullet([], [], self.world, postmove_strategy=BounceOnBoundaryStrategy())
                        self.add_bullet(self.image1_pos, self.image1_rect, b)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        i += 1
                    elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
                        self.bounce_box.handle_event(event)
                
                # ループ内で弾を適用
                for b in self.bullets:
                    self.bounce_box.apply_bounce_strategy(b)
                
                self.bounce_box.draw(self.screen)
                
                mouse_pos = pygame.mouse.get_pos()
                
                player1 = Player(self.screen, self.image1_pos, mouse_pos, self.image1, self.image1_rect, self.image1, self.image1_rect)
                player1()
                self.screen.blit(self.image2, self.image2_rect.topleft)

                self.update()
                self.draw_bullet()
                
                pygame.time.Clock().tick(60)

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        should_quit = True
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        should_quit = True
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        # 弾を追加する前に新しい弾を生成
                        b = Bullet([], [], self.world, postmove_strategy=BounceOnBoundaryStrategy())
                        self.add_bullet(self.image2_pos, self.image2_rect, b)
                    elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        i += 1
                    elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONUP:
                        self.bounce_box.handle_event(event)
                
                # ループ内で弾を適用
                for b in self.bullets:
                    self.bounce_box.apply_bounce_strategy(b)
                
                self.bounce_box.draw(self.screen)
                
                mouse_pos = pygame.mouse.get_pos()
                
                player2 = Player(self.screen, self.image2_pos, mouse_pos, self.image2, self.image2_rect, self.image1, self.image1_rect)
                player2()
                self.screen.blit(self.image1, self.image1_rect.topleft)

                self.update()
                self.draw_bullet()
                
                pygame.time.Clock().tick(60)
                
            if should_quit:
                break

        pygame.quit()

        
    def run(self):
        self.start_win()
        self.run_shooting()
        
if __name__ == "__main__":
    ap = AppMain()
    ap.run()
