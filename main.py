"""
Player target shooter 
Made By: Avyukt Gupta

This game is a shooter game between 2 players where you have to try to kill the other person
by shooting them.
"""

# import libraries
import pygame

# import the player class
from player import *

# initialize pygame
pygame.init()

# print out the intructions of the game
print("You have to use the WASD and ARROW keys to move. Click S to shoot for player 1 (blue).\nClick DOWN to shoot for player 2 (red). Whoever kills the other one first wins!")
print()

# wait so the players can read the instructions
pygame.time.wait(5000) # 5 seconds

# create a window
info = pygame.display.Info() # get the size of the desktop/computer
WIDTH, HEIGHT = info.current_w - 200, info.current_h - 200
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2 Player Shooter")

# draw ground
GROUND_HEIGHT = 170
GROUND_WIDTH = WIDTH
GROUND_X = 0
GROUND_Y = HEIGHT - GROUND_HEIGHT

ground = pygame.Rect(GROUND_X, GROUND_Y, GROUND_WIDTH, GROUND_HEIGHT)

healthBar1 = 240
healthBar2 = 240

def drawGround(surface):
    pygame.draw.rect(surface, (34, 186, 54), ground)
    
# create the players
player1 = Player({'x': 100, 'y': 100}, (0, 0, 255), GROUND_Y, WIDTH)  # blue
player2 = Player({'x': WIDTH - 100, 'y': 100}, (255, 0, 0), GROUND_Y, WIDTH)  # red

# get the start time to help get how long it took
# to finish the game
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

# bullets list
bullets = []
bullet_height, bullet_width = 20, 20

# draw the health bars
health_bar_width = 250
health_bar_height = 35

# main loop
def main(healthBar1, healthBar2):
    running = True

    while running:
        global window
        
        for event in pygame.event.get(): # event loop
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    player1.stop()
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player2.stop()
                    
            # if the player shoots
            if event.type == pygame.KEYDOWN: # change the direction of the bullet based on the last key
                if event.key == pygame.K_s:
                    if player1.last_key == 'd':
                        bullets.append({'x': player1.position['x'] + player1.width + player1.gun_width, 'y': player1.position['y'] + player1.offset, 'vel': 25, 'used': False, 'player': player1})
                    else:
                        bullets.append({'x': player1.position['x'] - player1.gun_width, 'y': player1.position['y'] + player1.offset, 'vel': -25, 'used': False, 'player': player1})
                if event.key == pygame.K_DOWN:
                    if player2.last_key == 'left':
                        bullets.append({'x': player2.position['x'] - player2.gun_width, 'y': player2.position['y'] + player2.offset, 'vel': -25, 'used': False, 'player': player2})
                    else:
                        bullets.append({'x': player2.position['x'] + player2.width + player2.gun_width, 'y': player2.position['y'] + player2.offset, 'vel': 25, 'used': False, 'player': player2})
                    
        # get the keys being pressed
        keys = pygame.key.get_pressed()
        
        # fill background
        window.fill((15, 15, 40))
        
        # draw ground
        drawGround(window)
        
        # draw the health bar
        health_bar1 = pygame.Rect(50, 40, health_bar_width, health_bar_height)
        health_bar2 = pygame.Rect(WIDTH - health_bar_width - 50, 40, health_bar_width, health_bar_height)
        pygame.draw.rect(window, (220, 220, 220), health_bar1)
        pygame.draw.rect(window, (220, 220, 220), health_bar2)
        
        # draw the thing inside the health bar to indicate the health
        pygame.draw.rect(window, player1.color, pygame.Rect(55, 45, healthBar1, 25))
        pygame.draw.rect(window, player2.color, pygame.Rect(WIDTH - health_bar_width - 50 + 5, 45, healthBar2, 25))
        
        # draw the bullets
        for bullet in bullets[:]:  # iterate over a copy
            pygame.draw.rect(window, (210, 180, 90), pygame.Rect(bullet['x'], bullet['y'], bullet_width, bullet_height))
            bullet['x'] += bullet['vel']

            # remove if off screen
            if bullet['x'] < 0 or bullet['x'] + bullet_width > WIDTH:
                bullets.remove(bullet)
                continue

            # bullet rect
            bullet_rect = pygame.Rect(bullet['x'], bullet['y'], bullet_width, bullet_height)

            # check which player is the target
            if bullet['player'] == player1:
                target = player2
                bar_to_decrease = 'healthBar2'
            else:
                target = player1
                bar_to_decrease = 'healthBar1'

            # set the target to be the other player
            target_rect = pygame.Rect(target.position['x'], target.position['y'], target.width, target.height)

            # if the bullet collides with the other/opposing player
            if bullet_rect.colliderect(target_rect):
                target.health -= 10
                bullets.remove(bullet)
                if bar_to_decrease == 'healthBar1':
                    healthBar1 -= 24
                else:
                    healthBar2 -= 24
    
        # move the player up if they click
        if keys[pygame.K_UP]:
            player2.jump()
        if keys[pygame.K_w]:
            player1.jump()
        
        # move the players left and right
        if keys[pygame.K_a]:
            player1.left()
            player1.last_key = 'a'
        if keys[pygame.K_d]:
            player1.right()
            player1.last_key = 'd'
        if keys[pygame.K_LEFT]:
            player2.left()
            player2.last_key = 'left'
        if keys[pygame.K_RIGHT]:
            player2.right()
            player2.last_key = 'right'

        # draw players
        player1.draw(window)
        player2.draw(window)
        
        # update the player position
        player1.update()
        player2.update()
        
        # check if game is over
        if player1.health <= 0:
            end_time = pygame.time.get_ticks()
            elapsed_ms = end_time - start_time
            elapsed_seconds = elapsed_ms / 1000  # convert to seconds
            pygame.quit()
            print("Player 2 won! It took Player 2 about "+str(elapsed_seconds)+" second(s) to kill Player 1. Congrats!")
            break
        elif player2.health <= 0:
            end_time = pygame.time.get_ticks()
            elapsed_ms = end_time - start_time
            elapsed_seconds = elapsed_ms / 1000  # convert to seconds
            pygame.quit()
            print("Player 1 won! It took Player 1 about "+str(elapsed_seconds)+" second(s) to kill Player 2. Congrats!")
            break

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()

# only run file if it's run directly
if __name__ == "__main__":
    main(healthBar1, healthBar2)
