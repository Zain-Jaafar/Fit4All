import pygame
import sys

# Look throught the current events and do things accordingly
def handle_events(events: list[pygame.event.Event]):
    for event in events:
        
        if event.type == pygame.QUIT: # If the user pressed the close button on the window
            pygame.quit() # Uninitialise/quit pygame
            sys.exit() # Cleanly close the python program
    
    