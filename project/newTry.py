import pygame
import random
import os
from os import path
img_dir = path.join(path.dirname(__file__),"img")
width=800
height=600
FPS=30 #if I want to speed it , just put bigger fps

WHITE=(255,255,255)
BLACK =(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)

#initialize and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Projekt")
clock=pygame.time.Clock()
font_name = pygame.font.match_font('arial') #goes through font on our computer and finds something similar

#text
def draw_text(surf,text,size,x,y):
    font = pygame.font.Font(font_name,size) # font object
    text_surface = font.render(text,True,WHITE) #Truw- we want to bi anti-aliased
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surf.blit(text_surface,text_rect)
    

#sprites
class Player(pygame.sprite.Sprite):
   #sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Sprite init function
        self.image= player_img
        self.image = pygame.transform.flip(self.image,True,False)
        self.image.set_colorkey(BLACK)
        #make that color transparent,ignore it
        #every sprite has rectangle around it
        self.rect= self.image.get_rect()
        self.rect.center = (width/2,height/2) #on the center of rectangle
        self.y_speed = 0
        self.x_speed =0

    def update(self):
        self.x_speed=0
        self.y_speed = 0
        keystate = pygame.key.get_pressed() #gets back a list which key is pressed
        if keystate[pygame.K_UP]: # up arrow key
            self.y_speed = -5        
        if keystate[pygame.K_DOWN]:
            self.y_speed = 5   
        if keystate[pygame.K_RIGHT]:
            self.x_speed = 5
        if keystate[pygame.K_LEFT]:
            self.x_speed = -5
        if self.rect.bottom>height:
            self.rect.bottom = height
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right < (width - self.rect.width):
            self.rect.right = width - self.rect.width
        self.rect.y += self.y_speed
        self.rect.x += self.x_speed
        
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery)
        all_sprites.add(bullet)
        bullets.add(bullet)
        
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(mob_img,(40,30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = random.randrange(height - self.rect.height)
        self.rect.x = random.randrange(-100,-40)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)

    def update(self):
        self.rect.y += self.speedx
        self.rect.x += self.speedy
        if (self.rect.right > width +10 or self.rect.top < -20 or self.rect.bottom > height + 20 ):
            self.rect.y = random.randrange(height - self.rect.height)
            self.rect.x = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image = surf = pygame.transform.rotate(self.image,90)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.speedx = 5
        self.rect.centery = y
        self.rect.right = x
        
    def update(self):       
        self.rect.x -= self.speedx
        # kill if it moves off the top of the screen
        if self.rect.left > width or self.rect.right < 0:
            self.kill
        
        

#game-graphics
background = pygame.image.load(path.join(img_dir,"background.jpg")).convert()
background = pygame.transform.scale(background,(800,600))
background_rect = background.get_rect()
player_img= pygame.image.load(path.join(img_dir,"p1_jump.png")).convert()
mob_img = pygame.image.load(path.join(img_dir,"spaceStation.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir,"bullet.png")).convert()

all_sprites=pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player=Player()
all_sprites.add(player)

for i in range(8): #8mobs
    m=Mob()
    all_sprites.add(m)
    mobs.add(m)
score = 0

#Game loop
running = True
while running: #30 puta u sekundi se izvrti (FPS)
    #keep loop running at the right speed
    clock.tick(FPS)
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        
    #Update
    all_sprites.update()
    #check to see if bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)#check if this two groups collide and delete bullet and mob that is hitted
    for hit in hits: #how many hits,create that many new mobs and add it to their gorups
        score +=10 
        m=Mob()
        all_sprites.add(m)
        all_sprites.add(m)
        mobs.add(m)
        mobs.add(m) 
    #check if mob hit the player
    hits = pygame.sprite.spritecollide(player,mobs,False) #sprite and group
    if hits:
        running = False
    
    #Draw/render
    screen.fill(BLACK)
    screen.blit(background,background_rect)  #blit=copy the pixels fro one thing to another thing
    all_sprites.draw(screen)
    draw_text(screen,"SCORE: " + str(score),18,width/2,10)
    # after drawing flip the display
    pygame.display.flip()

pygame.quit()
