# This file is used to initialise and define various constants and utility functions which will be used throughout the app

import pygame

# Initialise pygame
pygame.init()

# Sets the initial screen dimensions in pixels
# "SCREEN" refers to the window, not the computer screen, this is pygame convention
SCREEN_WIDTH = 378
SCREEN_HEIGHT = 700

SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) # Creates a window
pygame.display.set_caption("Fit4All") # Sets the title of the window


FPS = 60 # This variable defines the desired framerate/refresh rate for the rindow
clock = pygame.time.Clock() # instantiate the pygame Clock, this is used to keep track of the framerate

# Utility function to easily draw text to the screen
# def draw_text(colour, text, position, text_size=32):
#     font = pygame.font.Font('Fonts/Pixeltype.ttf', text_size)
#     text_surf = font.render(text, False, colour)
#     text_rect = pygame.Rect((0, 0), (text_surf.get_size()))
#     text_rect.topleft = position
#     SCREEN.blit(text_surf, text_rect)
