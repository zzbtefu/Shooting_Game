import math
import sys
import pygame

class AppMain:
    def __init__(self):
        pygame.init()
        self.width, self.height = 800, 600
        self.white = (255, 255, 255)
        self.blue = (0, 0, 255)
        self.bullets = []
        
    def run(self):
        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pygame Shooting Example")
        
        ship_image = pygame.Surface((50, 50), pygame.SRCALPHA)  # 透明なSurfaceを作成
        pygame.draw.rect(ship_image, self.blue, (0, 0, 50, 50))  # 四角形を描画
        ship_rect = ship_image.get_rect(center=(400, 300))
        bullet_speed = 5
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # 左クリックで弾を発射
                    dx = pygame.mouse.get_pos()[0] - ship_rect.centerx
                    dy = pygame.mouse.get_pos()[1] - ship_rect.centery
                    angle = math.atan2(dy, dx)
                    bullet_velocity = (bullet_speed * math.cos(angle), bullet_speed * math.sin(angle))
                    self.bullets.append([list(ship_rect.center), bullet_velocity])
            
            screen.fill("white")
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            dx = mouse_x - ship_rect.centerx
            dy = mouse_y - ship_rect.centery

            angle = math.degrees(math.atan2(dy, dx))
            rotated_image = pygame.transform.rotate(ship_image, -angle)
            rotated_rect = rotated_image.get_rect(center=ship_rect.center)

            screen.blit(rotated_image, rotated_rect.topleft)

            for bullet in self.bullets:
                bullet[0][0] += bullet[1][0]
                bullet[0][1] += bullet[1][1]
                pygame.draw.circle(screen, self.blue, (int(bullet[0][0]), int(bullet[0][1])), 5)

            pygame.display.flip()

            pygame.time.Clock().tick(60)
        
        pygame.quit()
        
if __name__ == "__main__":
    app = AppMain()
    app.run()
