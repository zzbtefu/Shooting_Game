class DrawObstacle:
    def __init__(self, pos, width):

class BounceBox:
    def __init__(self, pos, width, height):
        self.pos = pos
        self.width = width
        self.height = height
        
    def __call__(self):
        
class Zone_gravity:
    def __init__(self, pos, width, height):
        self.pos = pos
        self.width = width
        self.height = height
        
    def draw(self):
        
        
    
class Zone_Slow:
    def __init__(self, pos, width, height):
        
class HealthBar():
    def __init__(self, pos, width, max):
        self.x = pos[0]
        self.y = pos[1]
        self.width = width
        self.max = max # 最大HP
        self.hp = max # HP
        self.mark = int((self.width - 4) / self.max) # HPバーの1目盛り

        self.font = pygame.font.SysFont(None, 28)
        self.label = self.font.render("HP", True, (255, 255, 255))
        self.frame = Rect(self.x + 2 + self.label.get_width(), self.y, self.width, self.label.get_height())
        self.bar = Rect(self.x + 4 + self.label.get_width(), self.y + 2, self.width - 4, self.label.get_height() - 4)
        self.value = Rect(self.x + 4 + self.label.get_width(), self.y + 2, self.width - 4, self.label.get_height() - 4)

        # effect_barを追加
        self.effect_bar = Rect(self.x + 4 + self.label.get_width(), self.y + 2, self.width - 4, self.label.get_height() - 4)
        self.effect_color = (0, 255, 255)

    def update(self):
        if self.hp >= self.max:
            self.hp = self.max
            
        if self.effect_bar.width > self.mark * self.hp:
            self.value.width = self.mark * self.hp
            if self.effect_bar.width >= self.value.width:
                self.effect_bar.inflate_ip(-1, 0)
        elif self.value.width < self.mark * self.hp:
            self.effect_bar.width = self.mark * self.hp
            self.value.inflate_ip(1, 0)

        # effect_barの色を変える
        if self.effect_bar.width <= self.bar.width / 6:
            self.effect_color = (255, 255, 0)
        elif self.effect_bar.width <= self.bar.width / 2:
            self.effect_color = (255, 255, 0)
        else:
            self.effect_color = (0, 255, 0)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.frame)
        pygame.draw.rect(screen, (0, 0, 0), self.bar)
        pygame.draw.rect(screen, self.effect_color, self.effect_bar)
        pygame.draw.rect(screen, (0, 0, 255), self.value)
        screen.blit(self.label, (self.x, self.y))
        
        for block in self.blocks:
            ldx1 = b.pos[0] - block.pos[0]
            ldy1 = b.pos[1] - block.pos[1]
            ldx2 = b.pos[0] - block.pos[0]
            ldy2 = b.pos[1] - (block.pos[1] + block.height)
            ldx3 = b.pos[0] - (block.pos[0] + block.width)
            ldy3 = b.pos[1] - (block.pos[1] + block.height)
            ldx4 = b.pos[0] - (block.pos[0] + block.width)
            ldy4 = b.pos[1] - block.pos[1]
            for s in range(4):
                dist_s = math.sqrt(ldxs**2 + ldys**2)
            if (block.height - 5 < dist1 + dist2 < block.height + 5 and) or (pos[0] > box.pos[0] + width - radius and vel[0] > 0):
                vel[0] *= -1

            if (pos[1] < box.pos[1] + radius and vel[1] < 0) or (pos[1] > box.pos[1] + height - radius and vel[1] > 0):
                vel[1] *= -1

def alarm():
    pygame.mixer.init(frequency = 44100)    # 初期設定
    pygame.mixer.music.load("sample.wav")     # 音楽ファイルの読み込み
    pygame.mixer.music.play(1)              # 音楽の再生回数(1回)
    while(1):
        a = input("Finish? --->")
        if(a is 'y'): break
    pygame.mixer.music.stop()               # 再生の終了
    return 0
    
if __name__ is "__main__":
    alarm()