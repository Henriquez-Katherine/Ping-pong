import pygame
import random 
import time


pygame.init()


win = pygame.display.set_mode((720, 600))
# 'Window'

data = [] 
# List with all objects in game

clock = pygame.time.Clock()
fps = 60 # Fps (120, 60, 30)
Run = True
joym = False # Joystick connect
score1 = 0 # Player score
score2 = 0 # Bot score

# Some vars

f = pygame.font.SysFont('kokila', 50)
f1 = pygame.font.SysFont('kokila', 20)
# Fonts


bup = pygame.mixer.Sound("Bup.wav")
# This is game sound


class Player():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 40
        self.h = 200
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.speed = 12
        
    def draw(self):
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.w, self.h))
        
    def move(self):
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.y > 0 and joym == False:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < 400 and joym == False:
            self.y += self.speed
        if joym == True:
            if joysticks[0].get_hat(0) == (0, -1) and self.y < 400:
                self.y += self.speed
            if joysticks[0].get_hat(0) == (0, 1) and self.y > 0:
                self.y -= self.speed

                
class Bot():
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 40
        self.h = 200
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.speed = 4
        
    def draw(self):
        pygame.draw.rect(win, (255, 255, 255), (self.x, self.y, self.w, self.h))
        
    def move(self):
        if bl.y > self.y + self.h // 2 and self.y < 400:
            self.y += self.speed
        if bl.y < self.y + self.h // 2 and self.y > 0:
            self.y -= self.speed
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)


class Ball():
    
    def __init__(self, x, y):
        self.x = x 
        self.y = y
        self.w = 30
        self.h = 30
        self.rect = pygame.Rect(self.x - 15, self.y - 15, self.w, self.h)
        self.speed = 16
        # Main vars
        
        self.dest_x = 0
        self.dest_y = 0
        self.d = 0 # distance
        self.speed_x = 0
        self.speed_y = 0
        # Vars for find_path() and move_to()
        
    def draw(self):
        pygame.draw.circle(win, (255, 255, 255), (self.x, self.y), 15)
        
    def find_path(self, dest_x, dest_y):
        self.dest_x = dest_x - self.x
        self.dest_y = dest_y - self.y
        self.d = (self.dest_x ** 2 + self.dest_y ** 2) ** 0.5
        self.speed_x = (self.dest_x / self.d) * self.speed
        self.speed_y = (self.dest_y / self.d) * self.speed
        
    def move_to(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect = pygame.Rect(self.x - 15, self.y - 15, self.w, self.h)
        # Move Ball and Ball's rect
        
        for i in data:
            if self.rect.colliderect(pygame.Rect(i.x, i.y + i.h, i.w, 5)):
                self.speed_y *= -1
                bup.play()
            if self.rect.colliderect(pygame.Rect(i.x, i.y - 2, i.w, 3)):
                self.speed_y *= -1
                bup.play()
            if self.rect.colliderect(pygame.Rect(i.x + i.w, i.y, 5, i.h)):
                self.speed_x *= -1
                bup.play()
            if self.rect.colliderect(pygame.Rect(i.x - 2, i.y, 3, i.h)):
                self.speed_x *= -1
                bup.play()
        # Here we check collisions (with Player or Bot)
        # and play sound 'Buups'.
        
        if self.y <= 10:
            self.speed_y *= -1
            self.y = 10
        if self.y >= 590:
            self.speed_y *= -1
            self.y = 590
        if self.x <= 10:
            self.speed_x *= -1
            self.x = 10
        if self.x >= 710:
            self.speed_x *= -1
            self.x = 710
        # Ball rebound

            


while Run:
        keys = pygame.key.get_pressed()
        clock.tick(fps)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Run = False
        pygame.draw.rect(win, (0, 0, 0), (0, 0, 720, 600))
        text = f"{score1}     |     {score2}"
        win_text = f.render(str(text), 1, (255, 255, 255))
        win.blit(win_text, (300, 100))
        # Here We just drawing background
        
        if joym == False:
            text = f"Press SPACE to start"
            win_text = f.render(str(text), 1, (255, 255, 255))
            win.blit(win_text, (200, 150))
            text = f"Press k to connect joystick"
            win_text = f1.render(str(text), 1, (255, 255, 255))
            win.blit(win_text, (100, 100))
        if joym == True:
            text = f"Press Right Trigger to start(5)"
            win_text = f.render(str(text), 1, (255, 255, 255))
            win.blit(win_text, (200, 150))
            if joysticks[0].get_button(5):
                Run = False
        
        if keys[pygame.K_SPACE] and joym == False:
            Run = False
        if keys[pygame.K_k] and joym == False:
            joym = True
            try:
                joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
                print ("Joysticks count: ", len(joysticks))
                print ("Name: ", joysticks[0].get_name())
                print ("GUID: ", joysticks[0].get_guid())
                print ("Power level: ", joysticks[0].get_power_level())
                joym = True
            except:
                print ("Error, Cant find joystick")
                joym = False
        
        # Here We connect joystick
        pygame.display.update()

# This is loop for joysticks
#        
        
 

data.append(Player(0, 300))
data.append(Bot(680, 300))
bl = Ball(360, 300)
b = random.randint(0, 600)
go = [(0, b), (720, b)]
a = random.choice(go)
bl.find_path(a[0], a[1])

# Random for ball move

Run = True
while Run:
        clock.tick(fps)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Run = False
        pygame.draw.rect(win, (0, 0, 0), (0, 0, 720, 600))
        text = f"{score1}     |     {score2}"
        win_text = f.render(str(text), 1, (255, 255, 255))
        win.blit(win_text, (300, 100))
        for i in data:
            i.draw()
            i.move()
        bl.draw()
        bl.move_to()
        if bl.x < 20:
            bl.x = 300
            bl.y = 300
            score2 += 1
            b = random.randint(0, 600)
            a = random.choice(go)
            bl.find_path(a[0], a[1])
        if bl.x > 700:
            bl.x = 300
            bl.y = 300
            score1 += 1
            b = random.randint(0, 600)
            a = random.choice(go)
            bl.find_path(a[0], a[1])
        pygame.display.update()
