import pygame
import random
import os

width=800
height=600
FPS=30 #if I want to speed it , just put bigger fps

WHITE=(255,255,255)
BLACK =(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)

#set up assets folders
game_folder= os.path.dirname(__file__) 
img_folder = os.path.join(game_folder,"img")

#sprites
class Player(pygame.sprite.Sprite):
   #sprite for the player
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) # Sprite init function
        self.image= pygame.image.load(os.path.join(img_folder,"p1_jump.png")).convert()
        self.left = pygame.transform.flip(self.image,True,False)
        self.right = pygame.image.load(os.path.join(img_folder,"p1_jump.png")).convert()
        self.image.set_colorkey(BLACK) #make that color transparent,ignore it
        #every sprite has rectangle has around it
        self.rect= self.image.get_rect()
        self.rect.center = (width/2,height/2) #on the center of rectangle
        self.y_speed = 0

    def update(self):
        self.y_speed = 0 #dont move
        keystate = pygame.key.get_pressed() #gets back a list which key is pressed
        if keystate[pygame.K_UP]: # left arrow key
            self.y_speed = -5         
        if keystate[pygame.K_DOWN]:
            self.y_speed = 5
        if keystate[pygame.K_LEFT]:
            self.image= self.left
        if keystate[pygame.K_RIGHT]:
            self.image= self.right
        self.rect.y += self.y_speed

#initialize and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Projekt")
clock=pygame.time.Clock()

all_sprites=pygame.sprite.Group()
player=Player()
all_sprites.add(player)
#Game loop
running = True


while running: #30 puta u sekundi se izvrti (FPS)
    #keep loop running at the right speed
    clock.tick(FPS)
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    #Update
    all_sprites.update()
    #Draw/render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # after drawing flip the display
    pygame.display.flip()




pygame.quit()
