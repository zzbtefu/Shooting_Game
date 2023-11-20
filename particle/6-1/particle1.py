import pygame


class BounceOnBoundaryStrategy:
    def __init__(self, max_bounces=3, restitution=0.95):
        self.restitution = restitution
        self.max_bounces = max_bounces
        self.bounce_count = 0

    def __call__(self, p):
        x, y = p.x, p.y
        vx, vy = p.vel.x, p.vel.y
        width, height = p.world.width, p.world.height
        radius = p.radius
        e = self.restitution
        if (x < 0 + radius and vx < 0) or (x > width - radius and vx > 0):
            p.vel.x *= -e

        if y > height - radius and vy > 0:
            p.vel.y *= -e
            # constrain particle on or above the floor
            p.pos.y = height - radius
            self.bounce_count += 1

        if self.bounce_count >= self.max_bounces:
            p.is_alive = False

class World:
    def __init__(self, width, height, dt, gy):
        self.width = width
        self.height = height
        self.dt = dt
        self.gravity_acc = pygame.math.Vector2(0,gy)

class Particle:
    def __init__(self, pos, vel, world, radius=10.0, color="green", postmove_strategy=None):
        self.is_alive = True
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(vel)
        self.world = world
        self.radius = radius
        self.color = pygame.Color(color)
        self.postmove_strategy = postmove_strategy

    def update(self):
        self.vel += self.world.gravity_acc * self.world.dt
        self.pos += self.vel * self.world.dt
        if self.postmove_strategy is not None:
            self.postmove_strategy(self)
        else:
            self.update_after_move()

    def update_after_move(self):
        if self.x < 0 or self.x > self.world.width or self.y > self.world.height:
            self.is_alive = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    @property
    def x(self):
        return self.pos.x

    @property
    def y(self):
        return self.pos.y