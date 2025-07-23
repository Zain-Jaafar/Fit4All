import pygame

from utils import SCREEN, FPS, clock
from events import handle_events

class User:
    def __init__(self, age, time_availability):
        self.age = age
        self.time_availability = time_availability


def main():
    '''
    This function handles the main loop of the application, calling
    other functions and methods.
    '''
    
    while True:
        SCREEN.fill("white") # Set background to white
        
        handle_events(pygame.event.get()) # Call event loop
        
        
        pygame.display.flip()
        
        # This limits the framerate to the FPS variable, keeping the application feeling smooth
        clock.tick(FPS)

if __name__ == "__main__":
    main()
