import random
import pygame


class Particle:
    pass


def main():
    pygame.init()
    width, height = 600, 400
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    
    while True:
        frames_per_second = 60
        clock.tick(frames_per_second)
        
        dt = 1.0
        gy = 0.5
        p = Particle()
        p.is_alive = False
        p.x, p.y = 0, 0
        p.vx, p.vy = 0, 0
        
        should_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    should_quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not p.is_alive:
                    p.is_alive = True
                    p.x, p.y = event.pos
                    p.vx = random.uniform(-10, 10)
                    p.vy = random.uniform(-10, 0)
        if should_quit:
            break
        
        if p.is_alive:
            p.vy += gy * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
            if p.x < 0 or p.x > width or p.y > height:
                p.is_alive = False
            
        screen.fill(pygame.Color("black"))
        if p.is_alive:
            radius = 10
            pygame.draw.circle(screen, pygame.Color("green"), (p.x, p.y), radius)
        pygame.display.update()
        
    pygame.quit()


if __name__ == "__main__":
    main()