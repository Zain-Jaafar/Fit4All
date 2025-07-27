import pygame

from utils import SCREEN, FPS, clock
from events import handle_events
from ui_management import ui_manager


def main():
    '''
    This function handles the main loop of the application, calling
    other functions and methods.
    '''
    
    while True:
        # This limits the framerate to the value of the FPS constant, keeping the application feeling smooth
        # delta_time is a variable which holds the time since the last frame, which is useful for managing UI
        delta_time = clock.tick(FPS)/1000.0
        
        handle_events(pygame.event.get()) # Call event loop
        
        ui_manager.update(delta_time)
        
        
        SCREEN.fill("white") # Set background to white
        ui_manager.draw_ui(SCREEN) # Display GUI elements on the screen
        
        # Update the screen
        pygame.display.flip()
        

if __name__ == "__main__":
    main()
