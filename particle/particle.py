import random
import pygame


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
        particle_is_alive = False
        x, y = 0, 0
        vx, vy = 0, 0
        
        should_quit = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                should_quit = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    should_quit = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not particle_is_alive:
                    particle_is_alive = True
                    x, y = event.pos
                    vx = random.uniform(-10, 10)
                    vy = random.uniform(-10, 0)
        if should_quit:
            break
        
        if particle_is_alive:
            vy += gy * dt
            x += vx * dt
            y += vy * dt
            if x < 0 or x > width or y > height:
                particle_is_alive = False
            
        screen.fill(pygame.Color("black"))
        if particle_is_alive:
            radius = 10
            pygame.draw.circle(screen, pygame.Color("green"), (x, y), radius)
        pygame.display.update()
        
    pygame.quit()


if __name__ == "__main__":
    main()