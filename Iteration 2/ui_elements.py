import pygame_gui
import pygame
import warnings
import os
import random

from utils import SCREEN_WIDTH, SCREEN_HEIGHT, app_manager

# Filter out warnings saying that the "Label Rect is too small for text" using REGEX.
# Other warnings are still allowed.
# If I do not do this, there will be lots of warnings saying that the text for the exercises dont fit in their labels. 
# This is intended, so the warnings are useless and would just clutter the console output.
warnings.filterwarnings("ignore", message=".*Label Rect is too small for text.*")

ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'theme.json')

base_column_width = SCREEN_WIDTH/12
base_row_height = SCREEN_HEIGHT/24

error_notification_heading_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(base_column_width, base_row_height*18, base_column_width*10, 40),
                                                         text="",
                                                         manager=ui_manager)

error_notification_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(base_column_width, base_row_height*19, base_column_width*10, 40),
                                                         text="",
                                                         manager=ui_manager)

# Elements for Loading state
quotes = [
    "The only bad workout is the one that didn't happen",
    "The pain you feel today will be the strength you feel tomorrow",
    "Strive for progress, not perfection",
    "You don't have to be extreme, just consistent",
    "Take care of your body. It's the only place you have to live",
    "If it doesn't challenge you, it doesn't change you",
]

loading_label = pygame_gui.elements.UITextBox(
    relative_rect=pygame.Rect(0, 50, base_column_width*10, 60),
    html_text=random.choice(quotes),
    anchors={'center': 'center'},
    object_id=pygame_gui.core.ObjectID(class_id="@loading_label"),
    manager=ui_manager
)

# Load your spinner image
spinner_image = pygame.image.load(os.path.join("../Assets/loader-circle.png")).convert_alpha()

# Create a UIImage (centered in window)
loading_spinner = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect(0, 0, 40, 40),
    image_surface=spinner_image,
    anchors={'center': 'center'},
    manager=ui_manager
)


loading_elements = [
    loading_label,
    loading_spinner
]

# Onboarding Page
heading_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(base_column_width, base_row_height, -1, 20),
                                            text="Welcome To Fit4All",
                                            manager=ui_manager)

age_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(base_column_width, base_row_height*3, base_column_width*5, 50),
                                            placeholder_text="Enter Age:",
                                            manager=ui_manager)

age_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, -20, -1, 20),
                                        text="What is your age?",
                                        anchors={'bottom': 'bottom',
                                                 'right': 'right',
                                                 'bottom_target': age_input,
                                                 'right_target': age_input},
                                        manager=ui_manager)

injuries_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(base_column_width, base_row_height*6, base_column_width*10, 50),
                                            placeholder_text="Enter any injuries: ",
                                            manager=ui_manager)

injuries_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, -20, -1, 20),
                                        text="Got any injuries? If so, what kind?",
                                        anchors={'bottom': 'bottom',
                                                 'right': 'right',
                                                 'bottom_target': injuries_input,
                                                 'right_target': injuries_input},
                                        manager=ui_manager)

disabilities_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(base_column_width, base_row_height*9, base_column_width*10, 50),
                                            placeholder_text="Enter any disabilities: ",
                                            manager=ui_manager)

disabilities_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, -20, -1, 20),
                                        text="Got any disabilities? If so, what kind?",
                                        anchors={'bottom': 'bottom',
                                                 'right': 'right',
                                                 'bottom_target': disabilities_input,
                                                 'right_target': disabilities_input},
                                        manager=ui_manager)

availability_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(base_column_width, base_row_height*12, base_column_width*10, 50),
                                            placeholder_text="Enter time available: ",
                                            manager=ui_manager)

availability_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, -20, -1, 20),
                                        text="How many minutes/day can you exercise?",
                                        anchors={'bottom': 'bottom',
                                                 'right': 'right',
                                                 'bottom_target': availability_input,
                                                 'right_target': availability_input},
                                        manager=ui_manager)

other_information_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(base_column_width, base_row_height*15, base_column_width*10, 50),
                                            placeholder_text="Other information: ",
                                            manager=ui_manager)

other_information_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, -20, -1, 20),
                                        text="Any other information?",
                                        anchors={'bottom': 'bottom',
                                                 'right': 'right',
                                                 'bottom_target': other_information_input,
                                                 'right_target': other_information_input},
                                        manager=ui_manager)

onboarding_submit_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(base_column_width, base_row_height*21, base_column_width*10, 50),
                                             text="Generate Workout Routine",
                                             manager=ui_manager)

# List of elements in onboarding page
onboarding_elements = [
    heading_label, 
    age_input, 
    age_label, 
    injuries_input, 
    injuries_label, 
    disabilities_input, 
    disabilities_label, 
    availability_input, 
    availability_label, 
    other_information_input, 
    other_information_label,
    onboarding_submit_button,
    error_notification_label,
]

back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(base_column_width, base_row_height*21, base_column_width*10, 50),
                                             text="Back to Workout Generator",
                                             manager=ui_manager)

exercise_scroll_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect(base_column_width, base_row_height, base_column_width*10, base_row_height*20),
                                                                     should_grow_automatically=True,
                                                                     allow_scroll_x=False,
                                                                     manager=ui_manager)

home_elements = [
    back_button,
    exercise_scroll_container,
]

exercise_labels = []

def load_exercise_elements():
    # Remove old elements
    global exercise_labels
    for label in exercise_labels:
        label.kill()
        if label in home_elements:
            home_elements.remove(label)
    exercise_labels = []

    # Add new labels
    for index, element in enumerate(app_manager.workout):
        ui_pos_multiplier = 22*5
        
        # Format description text with newlines every 40 characters
        desc_text = element["description"]
        wrapped_desc = ""
        while len(desc_text) > 40:
            # Find the last space before 40 characters
            split_index = desc_text[:40].rfind(' ')
            if split_index == -1:  # No space found, force split at 40
                split_index = 30
            wrapped_desc += desc_text[:split_index] + '\n'
            desc_text = desc_text[split_index:].lstrip()
        wrapped_desc += desc_text  # Add remaining text
        
        # Create labels for displaying the workout exercise information
        name_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, index*ui_pos_multiplier + 4, base_column_width*10, 20),
            text=element["name"],
            container=exercise_scroll_container,
            manager=ui_manager,
        )
        description_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, index*ui_pos_multiplier + 4, base_column_width*10, base_row_height*2.2),
            text=wrapped_desc,
            container=exercise_scroll_container,
            manager=ui_manager,
        )
        sets_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(0, index*ui_pos_multiplier + base_row_height*2.2, base_column_width*5, 20),
            text=f"Sets: {element['sets']}",
            container=exercise_scroll_container,
            manager=ui_manager,
        )
        reps_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(base_column_width*5, index*ui_pos_multiplier + base_row_height*2.2, base_column_width*5, 20),
            text=f"Reps: {element['reps']}",
            container=exercise_scroll_container,
            manager=ui_manager,
        )
        
        # Add the new elements for each exercise to the home_elements and exercise_elements list to manage them in the future.
        home_elements.extend([name_label, description_label, sets_label, reps_label])
        exercise_labels.extend([name_label, description_label, sets_label, reps_label])
    
    # print(f"exercise_labels: {exercise_labels}, \n home_elements: {home_elements}")
    

# Hide all elements at first
for element in [*loading_elements, *onboarding_elements, *home_elements]:
    element.hide()
