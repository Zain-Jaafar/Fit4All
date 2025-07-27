import pygame
import pygame_gui
import sys
from ui_management import ui_manager

# Look throught the current events and do things accordingly
def handle_events(events: list[pygame.event.Event]):
    for event in events:
        ui_manager.process_events(event) # Handle pygame_gui GUI Events
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            pass

        if event.type == pygame.QUIT: # If the user pressed the close button on the window
            pygame.quit() # Uninitialise/quit pygame
            sys.exit() # Cleanly close the python program