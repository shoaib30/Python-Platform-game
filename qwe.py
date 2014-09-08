import pygame
import sys
import random
from pygame.image import load
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 500
GROUND_LEVEL = 370
b1=load('background3.jpg')
b2=load('background3.jpg')
flag=0
chx=0
chx1=0
chx2=3000
a=0
b=3000
class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image=load('sprite1.png')
        self.rect = self.image.get_rect()
    def update(self):
        if flag==1:
            change_x=0
        self.calc_grav()
        
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, passive_sprite_list, False) #
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                self.rect.left = block.rect.right


        self.rect.y += self.change_y
        #self.change_y=0
        block_hit_list = pygame.sprite.spritecollide(self, passive_sprite_list, False)
        for block in block_hit_list:
            
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            self.change_y=0
        


    def calc_grav(self):
        if self.change_y == 0:
            self.change_y = 1
        else:
           self.change_y += .35
        if self.rect.y >= GROUND_LEVEL - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = GROUND_LEVEL - self.rect.height
    def jump(self):
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self,passive_sprite_list, False)
        self.rect.y -= 2
        if len(platform_hit_list) > 0 or self.rect.bottom >= GROUND_LEVEL:
            self.change_y = -10

    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self,x,y, width, height):
        pygame.sprite.Sprite.__init__(self)
 
        self.image = pygame.Surface([width, height])
        self.image.fill(green)
 
        self.rect = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def update(self,chx):
        self.rect.x-=chx


active_sprite_list = pygame.sprite.Group()
p=Platform(300,240,50,50)
active_sprite_list.add(p)
passive_sprite_list = pygame.sprite.Group()
passive_sprite_list.add(p)
    
def main():
    global chx1,chx2,chx
    pygame.init()
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    s = pygame.display.set_mode(size)
    s.fill(black)
    player = Player()
    player.rect.x = 0
    player.rect.y = GROUND_LEVEL - player.rect.height
    active_sprite_list.add(player)
    
    

    done= False
    while not done:
        #pygame.time.delay(5)
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
        
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
        player.update()
        p.update(chx)
        chx=0

        if player.rect.right > SCREEN_WIDTH/2:
            player.rect.right = SCREEN_WIDTH/2-1
            flag=1
        else:
            flag=0
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0
        if flag==1:
            chx1-=6
            chx2-=6
            chx+=6
            
        if chx1<-3000:
            chx1=3000
        if chx2<-3000:
            chx2=3000
        s.blit(b1,(chx1,-1000))
        s.blit(b2,(chx2,-1000))
        active_sprite_list.draw(s)
        
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    pygame.quit()


main()
    
