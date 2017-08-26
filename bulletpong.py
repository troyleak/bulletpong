#!/usr/bin/env python3

"""
Hacked together using Sample Python/Pygame Programs
from Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

Programmer: Troy Leak
"""

import pygame
import math
import random

# Set some variables

screen_width = 800
screen_height = 600
screen_size = [screen_width, screen_height]

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

MAX_BOUNCES = 20

# For Debugging. Multiple arguments will be printed on separate lines
DEBUG = True
def logger(*argv):
    if DEBUG == True:
        for arg in argv:
            print(arg)

class Ball(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self, x, y):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create the image of the ball
        self.image = pygame.Surface([10, 10])

        # Color the ball
        self.image.fill(GREEN)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Speed in pixels per cycle
        self.speed = 0

        # Floating point representation of where the ball is
        self.x = 1
        self.y = 1

        # Direction of ball in degrees
        self.direction = 0

        # Height and width of the ball
        self.width = 10
        self.height = 10

        self.bounces = 0

        logger("Ball Starting at: {0}, {1} ".format(self.x, self.y), "Direction: {0}".format(self.direction))

        # Set the initial ball speed and position
        self.reset()

    def reset(self):
        logger("--- Resetting Ball ---", "X and Y positions: ({0},{1})".format(self.x, self.y),
                "Speed: {0}".format(self.speed),
                "Direction: {0}".format(self.direction),
                "Bounces: {0}".format(self.bounces))
        self.x = screen_width/2
        self.y = screen_height/2
        self.speed=0.0
        self.bounces = 0

        # Direction of ball (in degrees)
        self.direction = 0

    # This function will bounce the ball off a horizontal surface (not a vertical one)
    def bounce(self, diff): # Diff is always degrees
        # logger("Ball bouncing", "Direction: {0}".format(self.direction))
        # if vertical == True:
        #     self.direction = self.direction+180
        # else:
        #     self.direction = (180-self.direction)%360

        self.direction = diff
        self.bounces += 1

        # Speed the ball up
        if self.speed == 0:
            logger("Ball was stopped, moving again")
            self.speed = 4
        elif self.speed >= 1:
            logger("Speeding up ball to {0}".format(round(self.speed, 2)))
            self.speed *= 1.1

    # Update the position of the ball
    def update(self):
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.cos(direction_radians)
        self.y += self.speed * math.sin(direction_radians)

        if self.y <= 0 or self.y >= screen_height - 25 or self.x >= screen_width-self.width:
            self.bounce(((2*self.direction)-90)%360)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce of the right side of the screen?
        if self.x <= 0:
            self.reset()

        if self.bounces >= MAX_BOUNCES:
            self.reset()


class Player(pygame.sprite.Sprite):
    """ The class is the player-controlled sprite. """
    # -- Methods
    def __init__(self, x, y):
        """Constructor function"""
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.width, self.height = 15, 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(BLACK)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # -- Attributes
        # Set speed vector
        self.change_x = 0
        self.change_y = 0

    def changespeed(self, x, y):
        """ Change the speed of the player"""
        self.change_x += x
        self.change_y += y

    def update(self):
        """ Find a new position for the player"""

        if self.rect.y <= 0:
            logger("resetting to bottom edge")
            self.rect.y = 0

        if self.rect.y > screen_height-self.height:
            logger("resetting to top edge")
            self.rect.y = screen_height-self.height

        self.rect.x += self.change_x
        self.rect.y += self.change_y
        # logger("Player X Position: {0}".format(self.rect.x), "Player Y Position: {0}".format(self.rect.y))

class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet. """

    def __init__(self, start_x, start_y, dest_x, dest_y):
        """ Constructor.
        It takes in the starting x and y location.
        It also takes in the destination x and y position.
        """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Set up the image for the bullet
        self.image = pygame.Surface([4, 10])
        self.image.fill(BLACK)

        self.rect = self.image.get_rect()

        # Move the bullet to our starting location
        self.rect.x = start_x
        self.rect.y = start_y

        # Because rect.x and rect.y are automatically converted
        # to integers, we need to create different variables that
        # store the location as floating point numbers. Integers
        # are not accurate enough for aiming.
        self.floating_point_x = start_x
        self.floating_point_y = start_y

        # Calculation the angle in radians between the start points
        # and end points. This is the angle the bullet will travel.
        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        self.angle = math.atan2(y_diff, x_diff);

        # Taking into account the angle, calculate our change_x
        # and change_y. Velocity is how fast the bullet travels.
        self.velocity = 5
        self.change_x = math.cos(self.angle) * self.velocity
        self.change_y = math.sin(self.angle) * self.velocity

    def update(self):
        """ Move the bullet. """

        # The floating point x and y hold our more accurate location.
        self.floating_point_y += self.change_y
        self.floating_point_x += self.change_x


        # The rect.x and rect.y are converted to integers.
        self.rect.y = int(self.floating_point_y)
        self.rect.x = int(self.floating_point_x)

        # If the bullet flies of the screen, get rid of it.
        if self.rect.x < 0 or self.rect.x > screen_width or self.rect.y < 0 or self.rect.y > screen_height:
            logger("--- Bullet Exited Screen ---", "X and Y positions: ({0},{1})".format(self.rect.x, self.rect.y),
                    "Speed: {0}".format(self.velocity),
                    "Direction: {0} degrees".format(round(math.degrees(self.angle), 2)))
            self.kill()

    def get_direction(self):
        # Need to convert radians to degrees
        logger("Bullet Direction - Radians: {0}".format(self.angle))
        angle_degrees = math.degrees(self.angle)
        logger("Bullet Direction - Degrees: {0}".format(angle_degrees))
        return angle_degrees

# Call this function so the Pygame library can initialize itself
pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode(screen_size)

# Set the title of the window
pygame.display.set_caption('Bullet Pong')

# Disable this to make the mouse disappear when over our window
pygame.mouse.set_visible(1)

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)

# Create a surface we can draw on
background = pygame.Surface(screen.get_size())

# Create the player object
player = Player(50, screen_height/2)
ball = Ball(25, 25)

all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player)

balls = pygame.sprite.Group()
balls.add(ball)

all_sprites_list.add(ball)

bullet_list = pygame.sprite.Group()
ball_hit_list = pygame.sprite.Group()

clock = pygame.time.Clock()
done = False

score = 0

while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        # Set the speed based on the key pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.changespeed(0, -3)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.changespeed(0, 3)

        # Reset speed when key goes up
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.changespeed(0, 3)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.changespeed(0, -3)

        # Fire a bullet if the user clicks the mouse button
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            pos = pygame.mouse.get_pos()

            mouse_x = pos[0]
            mouse_y = pos[1]

            # Create the bullet based on where we are, and where we want to go.
            bullet = Bullet(player.rect.x, player.rect.y, mouse_x, mouse_y)

            # Add the bullet to the lists
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)


    # --- Win conditions
    if score >= 1:
        text = font.render("Game Over", 1, (200, 200, 200))
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 50
        screen.blit(text, textpos)
        logger("Game Over")
        done = True

    # Calculate mechanics for each bullet
    for bullet in bullet_list:

        # See if it hit a ball
        ball_hit_list = pygame.sprite.spritecollide(bullet, balls, False)

        # For each ball hit, remove the bullet and bounce away
        for ball in ball_hit_list:
            direction = bullet.get_direction()
            logger("Bouncing ball at {0} degrees".format(direction))
            ball.bounce(direction)
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
            logger("Score: {0}".format(score))

    # This calls update on all the sprites
    all_sprites_list.update()

    # -- Draw everything
    # Clear screen
    screen.fill(WHITE)

    # Draw sprites
    all_sprites_list.draw(screen)

    # Flip screen
    pygame.display.flip()

    # Pause
    clock.tick(60)

pygame.quit()
