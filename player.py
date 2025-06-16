# import library
import pygame

class Player:
    def __init__(self, pos: dict, color: tuple, ground: int, width: int): # make sure it is the correct data type
         # define all the variables
        self.position = pos
        self.velocityX = 0
        self.velocityY = 0
        self.color = color
        self.width = 50
        self.height = 200
        # create gravity to move players to ground
        self.gravity = 1
        # get variables from main to check boundaries
        self.ground = ground
        self.screenWidth = width
        # health
        self.health = 100
        # set these as global to modify inside the draw function
        # these are to draw the gun
        self.gun_rect = pygame.Rect(0, 0, 0, 0)
        self.gun_rect2 = pygame.Rect(0, 0, 0, 0)
        # dimesions of gun
        self.offset = 55
        self.gun_width = 80
        self.gun_height = 20
        self.gun_height2 = 35

        # use the last key variable to check which way the gun should
        # be pointing and which way the bullets should be shooting
        self.last_key = 'd' if self.color == (0, 0, 255) else 'left'

    def draw(self, surface):
        # draw player rectangle
        player_rect = pygame.Rect(self.position['x'], self.position['y'], self.width, self.height)
        pygame.draw.rect(surface, self.color, player_rect)

        # determine direction
        facing_right = self.last_key in ['d', 'right']

        # gun color based on player
        gun_color = (192, 192, 192) if self.color == (0, 0, 255) else (60, 80, 110)

        # draw gun based on direction
        if facing_right:
            # gun to the right
            self.gun_rect = pygame.Rect(
                self.position['x'] + self.width,
                self.position['y'] + self.offset,
                self.gun_width,
                self.gun_height
            )
            self.gun_rect2 = pygame.Rect(
                self.position['x'] + self.width,
                self.position['y'] + self.offset + self.gun_height,
                self.gun_height,
                self.gun_height2
            )
        else:
            # gun to the left
            self.gun_rect = pygame.Rect(
                self.position['x'] - self.gun_width,
                self.position['y'] + self.offset,
                self.gun_width,
                self.gun_height
            )
            self.gun_rect2 = pygame.Rect(
                self.position['x'] - self.gun_height,
                self.position['y'] + self.offset + self.gun_height,
                self.gun_height,
                self.gun_height2
            )

        # draw both gun parts
        pygame.draw.rect(surface, gun_color, self.gun_rect)
        pygame.draw.rect(surface, gun_color, self.gun_rect2)

        
        # draw gun
        if self.color == (0, 0, 255):
            pygame.draw.rect(surface, (192, 192, 192), self.gun_rect)
            pygame.draw.rect(surface, (192, 192, 192), self.gun_rect2)
        else:
            pygame.draw.rect(surface, (60, 80, 110), self.gun_rect)
            pygame.draw.rect(surface, (60, 80, 110), self.gun_rect2)

    def jump(self):
        self.velocityY = -15
        
    def left(self):
        self.velocityX = -11
    
    def right(self):
        self.velocityX = 11
    
    def isOnGround(self) -> bool: # checks if you should still apply gravity
        if (self.position['y'] + self.height) > self.ground:
            return True
        else:
            return False
        
    def stop(self):
        self.velocityX = 0

    def update(self): # update the position of the player
        # add values to position to move
        self.velocityY += self.gravity
        self.position['y'] += self.velocityY
        
        self.position['x'] += self.velocityX 

        # on ground
        if self.position['y'] + self.height >= self.ground:
            self.position['y'] = self.ground - self.height  # Set on top of ground
            self.velocityY = 0 # reset the velocity
            
        # stop the player if its on the boundaries
        if self.position['x'] + self.width >= self.screenWidth:
            self.position['x'] = self.screenWidth - self.width
            self.velocityX = 0
            
        if self.position['x'] < 0: # check if they are too far to the left
            self.position['x'] = 0
            self.velocityX = 0
        
        # make sure that the player doesn't go too high
        if self.position['y'] < 0:
            self.position['y'] = 0
            self.velocityY = 0