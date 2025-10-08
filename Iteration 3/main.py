import pygame

from utils import SCREEN, FPS, clock, app_manager
from events import handle_events
from ui_elements import (
    ui_manager, 
    onboarding_elements, 
    home_elements, 
    load_exercise_elements, 
    spinner_image, 
    loading_spinner,
    exercise_directory_icon,
    workout_generation_icon,
    workout_icon,
    user_manual_icon,
    please_generate_workout_label,
    navigation_icons,
)


def main():
    '''
    This function handles the main loop of the application, calling
    other functions and methods.
    '''
    
    # Set the callback function which runs whenever app_manager.workout is changed
    app_manager.workout_changed_callback = load_exercise_elements
    
    # Change to onboarding page
    app_manager.change_state("Onboarding", onboarding_elements, [])
    
    # Enable all icons except the workout generation form icon
    workout_icon.enable()
    workout_generation_icon.disable()
    exercise_directory_icon.enable()
    user_manual_icon.enable()
    
    # Set the starting angle of the loading spinner
    loading_spinner_angle = 0
    
    # Attempt to load the user and workout routine
    app_manager.load_user()
    app_manager.load_workout()
    
    if app_manager.user and app_manager.workout:
        app_manager.change_state("Home", home_elements, onboarding_elements)
        
        # Enable all icons except the workout icon
        workout_icon.disable()
        workout_generation_icon.enable()
        exercise_directory_icon.enable()
        user_manual_icon.enable()
        
        please_generate_workout_label.hide()
    
    while True:
        # This limits the framerate to the value of the FPS constant, keeping the application feeling smooth
        # delta_time is a variable which holds the time since the last frame, which is useful for managing UI
        delta_time = clock.tick(FPS)/1000.0
        
        handle_events(pygame.event.get()) # Call event loop
        
        # Update UI elements
        ui_manager.update(delta_time)
        
        if app_manager.states["Loading"]:
            # Rotate spinner
            loading_spinner_angle = (loading_spinner_angle + 180 * delta_time) % 360  # degrees per second
            rotated_image = pygame.transform.rotate(spinner_image, loading_spinner_angle)

            # Update UIImage with rotated surface
            loading_spinner.set_image(rotated_image)
        
        
        # Set background to white
        SCREEN.fill("white") 
        
        # Display GUI elements on the screen
        ui_manager.draw_ui(SCREEN)
        
        # Only draw icons for navigation when not in the loading state.
        for navigation_icon in navigation_icons:
            navigation_icon.draw()
        
        pygame.display.flip()
        

if __name__ == "__main__":
    main()
