## create color change clear game

import random
import math
import pygame

PgVector = pygame.math.Vector2

class World:
    def __init__(self, dt, gravity_acc, width, height, should_quit, score, end):
        self.dt = dt
        self.gravity_acc = PgVector(gravity_acc)
        self.width = width
        self.height = height
        self.should_quit = should_quit
        self.score = score
        self.end = end


class CircleDrawer:
    def __init__(self, color_num, width):
        self.width = width
        color_list = ["white", "green", "blue", "pink", "yellow", "red", (80,80,80)]
        self.color = color_list[color_num]

    def __call__(self, screen, center, radius):
        pygame.draw.circle(screen, self.color, center, radius, self.width)

def compute_gravity_force(mass, gravity_acc, slow):
    if slow:
        gravity_acc = gravity_acc / 100
    return mass * gravity_acc

def compute_viscous_damping_force(viscous_damping, vel):
    return -viscous_damping * vel


def integrate_symplectic(pos, vel, force, mass, dt):
    vel_new = vel + force / mass * dt
    pos_new = pos + vel_new * dt
    return pos_new, vel_new

class ColorBall:
    def __init__(self, pos, vel, world, radius=10.0, mass=10.0,
                 viscous_damping=0.01, restitution=0.5, drawer=None, slow=False, color_num=0):
        self.is_alive = True
        self.world = world
        self.drawer = drawer or CircleDrawer(0, 1)
        self.slow = slow #重力加速度を変化

        self.pos = PgVector(pos)
        self.vel = PgVector(vel)
        self.radius = radius
        self.mass = mass
        self.viscous_damping = viscous_damping
        self.restitution = restitution
        self.color_num = color_num

        self.total_force = PgVector((0, 0))
        self.message_list = []

    def update(self):
        self.generate_force()
        self.move()
        self.total_force = PgVector((0, 0))
        self.message_list.clear()
        
        if self.pos.y > self.world.height - self.radius and self.mass != 1e9:
            self.change_type()
            
        if self.vel.y > 0 and self.slow == False:
            self.is_alive = False

    def draw(self, screen):
        self.drawer(screen, self.pos, self.radius)

    def receive_force(self, force):
        self.total_force += PgVector(force)

    def receive_message(self, msg):
        self.message_list.append(msg)

    def generate_force(self):
        force_g = compute_gravity_force(self.mass, self.world.gravity_acc, self.slow)
        force_v = compute_viscous_damping_force(self.viscous_damping, self.vel)
        self.receive_force(force_g + force_v)

    def move(self):
        if self.mass == 1e9:
            pass
        else:
            self.pos, self.vel = \
            integrate_symplectic(self.pos, self.vel, self.total_force, self.mass, self.world.dt)
            
    def change_type(self):
        self.vel = PgVector((0,0))
        self.slow = True
        self.mass = 1e9
        self.drawer = CircleDrawer(6,0)

def is_point_mass(actor):
    return isinstance(actor, ColorBall)

def collision_change(p1, p2, world):
    if (p1.mass == 1e9 and p2.mass == 30) or (p2.mass == 1e9 and p1.mass == 30):
        p1.change_type()
        p2.change_type()
    if (p1.color_num == p2.color_num and p1.mass == 30) or (p1.color_num == p2.color_num and p2.mass == 30): ## same color vanish
        p1.is_alive = False
        p2.is_alive = False
        world.score += math.floor(1250*(p1.radius+p2.radius)/(p1.radius*p2.radius))
        print("score : ")
        print(world.score)
        
def compute_impact_force_between_points(p1, p2, world):
    if (p1.pos - p2.pos).magnitude() > p1.radius + p2.radius:
        return None
    if p1.pos == p2.pos:
        return None
    
    collision_change(p1, p2, world)
    
    normal = (p2.pos - p1.pos).normalize()
    v1 = p1.vel.dot(normal)
    v2 = p2.vel.dot(normal)
    if v1 < v2:
        return None
    e = p1.restitution * p2.restitution
    m1, m2 = p1.mass, p2.mass
    f1 = normal * (-(e + 1) * v1 + (e + 1) * v2) / (1/m1 + 1/m2) / world.dt
    
    return f1

class CollisionResolver:
    def __init__(self, world, actor_list, target_condition=None, drawer=None, slow=False):
        self.is_alive = True
        self.world = world
        self.drawer = drawer or (lambda surface: None)
        self.slow = slow
        
        self.actor_list = actor_list
        if target_condition is None:
            self.target_condition = is_point_mass
        else:
            self.target_condition = target_condition

    def update(self):
        self.generate_force()

    def draw(self, surface):
        self.drawer(surface)
    
    
    def generate_force(self):
        plist = [a for a in self.actor_list if self.target_condition(a)]
        n = len(plist)
        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = plist[i], plist[j]
                f1 = compute_impact_force_between_points(p1, p2, self.world)
                if f1 is None:
                    continue
                p1.receive_force(f1)
                p2.receive_force(-f1)    

def compute_impact_force_by_fixture(p, normal, point_included, dt):
    invasion = normal.dot(p.pos - point_included)
    if invasion + p.radius > 0 and normal.dot(p.vel) > 0:
        e = p.restitution
        v = normal.dot(p.vel)
        m = p.mass
        f = normal * (-(e + 1) * v) * m / dt
    else:
        f = None
    return f
        
class Limit:
    def __init__(self, world, actor_list, target_condition=None):
        self.world = world
        self.actor_list = actor_list
        if target_condition is None:
            self.target_condition = is_point_mass
        else:
            self.target_condition = target_condition
    def check(self, limit_pos):
        plist = [a for a in self.actor_list if self.target_condition(a)]
        n = len(plist)
        for i in range(n):
            p = plist[i]
            if p.mass == 1e9 and p.pos.y - p.radius <= limit_pos:
                pygame.time.delay(500)
                print("--------GAME OVER--------")
                self.world.end = True

class Boundary:
    def __init__(self, normal, point_included, world, actor_list,
                 target_condition=None, drawer=None):
        self.is_alive = True
        self.world = world
        self.drawer = drawer or (lambda surface: None)

        self.normal = PgVector(normal).normalize()
        self.point_included = PgVector(point_included)
        self.actor_list = actor_list
        if target_condition is None:
            self.target_condition = is_point_mass
        else:
            self.target_condition = target_condition

    def update(self):
        self.generate_force()

    def draw(self, surface):
        self.drawer(surface)

    def is_floor(self):
        return self.normal == PgVector((0, 1))

    def generate_force(self):
        plist = [a for a in self.actor_list if self.target_condition(a)]
        for p in plist:
            f = compute_impact_force_by_fixture(p, self.normal, self.point_included, self.world.dt)
            if f is None:
                continue
            p.receive_force(f)

class ActorFactory:
    def __init__(self, world, actor_list):
        self.world = world
        self.actor_list = actor_list

    def create_point_mass(self, pos, slow=False):
        if slow: ##set dropping ball
            vel = (0, random.uniform(0.1,3.0))
            color_num = random.randint(1,5)
            radius = random.randint(25, 50)
            mass = 30
            width = 0
        else: ##set shooting ball
            vel = (0, -10)
            color_num = 0
            radius = 10
            mass = 10
            width = 3

        viscous = 0.01
        restitution = 0.95
        
        PointMassClass = ColorBall
        return PointMassClass(pos, vel, self.world, radius, mass, viscous,
                              restitution, CircleDrawer(color_num, width), slow, color_num)
    
    def create_collision_resolver(self):
        return CollisionResolver(self.world, self.actor_list)

    def create_boundary(self, name):
        width = self.world.width
        height = self.world.height
        geometry = {"top": ((0, -1), (0, 0)),
                    "bottom": ((0, 1), (0, height)),
                    "left": ((-1, 0), (0, 0)),
                    "right": ((1, 0), (width, 0))}
        normal, point_included = geometry[name]
        return Boundary(normal, point_included, self.world, self.actor_list)
    
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

class EndWindow:
    def __init__(self):
        self.font = pygame.font.Font(None, 60)
        
    def __call__(self, world, screen):
        screen.fill(pygame.Color("gray"))
        score_text = self.font.render(f"Score: {world.score}", True, 'black')
        screen.blit(score_text, (world.width // 2 - 120, world.height // 2))
        pygame.display.update()
        pygame.time.delay(2500)
        pygame.quit()
        
class AppMain:
    def __init__(self):
        pygame.init()
        self.world = World(dt=1.0, gravity_acc=(0, 0.4), width=600, height=700, should_quit=False, score=0, end=False)
        self.screen = pygame.display.set_mode((self.world.width, self.world.height))
        self.actor_list = []
        self.factory = ActorFactory(self.world, self.actor_list)
        self.limit = Limit(self.world, self.actor_list, target_condition=None)
        self.limit_pos = 30
        self.start_win = StartWindow(self.world, self.screen, start=False)
        self.end_win = EndWindow()

        self.actor_list.append(self.factory.create_collision_resolver())
        self.actor_list.append(self.factory.create_boundary("top"))
        self.actor_list.append(self.factory.create_boundary("bottom"))
        self.actor_list.append(self.factory.create_boundary("left"))
        self.actor_list.append(self.factory.create_boundary("right"))
        
        self.point_mass_prev = None

    def add_point_mass(self, pos, button):
        if button == 1:
            slow = False
        elif button == 3:
            slow = True
        else:
            return
        
        p = self.factory.create_point_mass(pos, slow)
        self.actor_list.append(p)
        self.point_mass_prev = p

    def update(self):
        for a in self.actor_list:
            a.update()
        self.actor_list[:] = [a for a in self.actor_list if a.is_alive]
        self.limit.check(self.limit_pos)

    def draw(self):
        self.screen.fill(pygame.Color("black"))
        pygame.draw.line(self.screen, 'red', (0,self.limit_pos), (self.world.width, self.limit_pos), 2)
        for a in self.actor_list:
            a.draw(self.screen)
        pygame.display.update()
    
    def run_colorgame(self):
        clock = pygame.time.Clock()
        while True:
            
            frames_per_second = 60
            clock.tick(frames_per_second)
            
            time_now = pygame.time.get_ticks()
            if time_now <= 2e4:
                time_interval =  1000
            elif time_now <= 6e4:
                time_interval = 700
            else:
                time_interval = 500
            if time_now % time_interval < 10:
                create_pos = (random.uniform(0,self.world.width), 0)
                self.add_point_mass(create_pos, 3)
                
            should_quit = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    quit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_c:
                    self.world.score += 10000
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                    self.world.end = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.add_point_mass(event.pos, event.button)
            if  should_quit:
                break
            if self.world.end:
                break

            self.update()
            self.draw()
        
    def run(self):
        self.start_win()
        self.run_colorgame()
        self.end_win(self.world, self.screen)
        
if __name__ == "__main__":
    AppMain().run()
    