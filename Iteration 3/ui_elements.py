import pygame_gui
import pygame
import warnings
import os
import json
import random

from utils import SCREEN, SCREEN_WIDTH, SCREEN_HEIGHT, app_manager

# Filter out warnings saying that the "Label Rect is too small for text" using REGEX.
# Other warnings are still allowed.
# If I do not do this, there will be lots of warnings saying that the text for the exercises dont fit in their labels. 
# This is intended, so the warnings are useless and would just clutter the console output.
warnings.filterwarnings("ignore", message=".*Label Rect is too small for text.*")

ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'theme.json')

base_column_width = SCREEN_WIDTH/12
base_row_height = SCREEN_HEIGHT/24

# Load exercise data from json file
with open('exercise_directory.json', 'r') as f:
    EXERCISES = json.load(f)


error_notification_heading_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(base_column_width, base_row_height*18.7, base_column_width*10, 40),
    text="",
    manager=ui_manager
)

error_notification_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(base_column_width, base_row_height*19.2, base_column_width*10, 40),
    text="",
    manager=ui_manager
)

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
heading_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(base_column_width, base_row_height/2, -1, 20),
    text="Welcome To Fit4All",
    manager=ui_manager
)

age_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(base_column_width, base_row_height*2, base_column_width*5, 50),
    placeholder_text="",
    manager=ui_manager
)

age_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(0, -20, -1, 20),
    text="What is your age?",
    anchors={'bottom': 'bottom',
                'right': 'right',
                'bottom_target': age_input,
                'right_target': age_input},
    manager=ui_manager
)

injuries_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(base_column_width, base_row_height*5, base_column_width*10, 50),
    placeholder_text="",
    manager=ui_manager
)

injuries_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(0, -20, -1, 20),
    text="Got any injuries? If so, what kind?",
    anchors={'bottom': 'bottom',
                'right': 'right',
                'bottom_target': injuries_input,
                'right_target': injuries_input},
    manager=ui_manager
)

disabilities_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(base_column_width, base_row_height*8, base_column_width*10, 50),
    placeholder_text="",
    manager=ui_manager
)

disabilities_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(0, -20, -1, 20),
    text="Got any disabilities? If so, what kind?",
    anchors={'bottom': 'bottom',
                'right': 'right',
                'bottom_target': disabilities_input,
                'right_target': disabilities_input},
    manager=ui_manager
)

availability_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(base_column_width, base_row_height*11, base_column_width*10, 50),
    placeholder_text="",
    manager=ui_manager
)

availability_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(0, -20, -1, 20),
    text="How many minutes/day can you exercise?",
    anchors={'bottom': 'bottom',
                'right': 'right',
                'bottom_target': availability_input,
                'right_target': availability_input},
    manager=ui_manager
)

weight_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(base_column_width, base_row_height*14, base_column_width*10, 50),
    placeholder_text="",
    manager=ui_manager
)

weight_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(0, -20, -1, 20),
    text="What is your approximate weight?",
    anchors={'bottom': 'bottom',
                'right': 'right',
                'bottom_target': weight_input,
                'right_target': weight_input},
    manager=ui_manager
)

other_information_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect(base_column_width, base_row_height*17, base_column_width*10, 50),
    placeholder_text="",
    manager=ui_manager
)

other_information_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(0, -20, -1, 20),
    text="Any other information?",
    anchors={'bottom': 'bottom',
                'right': 'right',
                'bottom_target': other_information_input,
                'right_target': other_information_input},
    manager=ui_manager
)

onboarding_submit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(base_column_width, base_row_height*20, base_column_width*10, 50),
    text="Generate Workout Routine",
    manager=ui_manager
)

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
    weight_input,
    weight_label,
    onboarding_submit_button,
    error_notification_label,
]


exercise_scroll_container = pygame_gui.elements.UIScrollingContainer(
    relative_rect=pygame.Rect(base_column_width, base_row_height, base_column_width*10, base_row_height*20),
    should_grow_automatically=True,
    allow_scroll_x=False,
    manager=ui_manager
)

please_generate_workout_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(0, 0, -1, 20),
    text="Please generate a workout routine",
    anchors={"center": "center"},
    manager=ui_manager
)

home_elements = [
    please_generate_workout_label,
    exercise_scroll_container,
]

exercise_labels = []

def load_exercise_elements():
    # Remove the "please generate workout routine" label because we now know the user has a workout routine
    please_generate_workout_label.kill()
    
    # Remove old elements
    global exercise_labels
    for label in exercise_labels:
        label.kill()
        if label in home_elements:
            home_elements.remove(label)
    exercise_labels = []

    # Add new exercise labels
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
    

# Exercise Directory - Headings
exercise_directory_heading = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(base_column_width, base_row_height, -1, 20),
    text="Exercise Directory"
)

arms_directory_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(base_column_width, base_row_height*2, base_column_width*10, 50),
    text="Arms Exercises",
    manager=ui_manager
)

chest_directory_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(base_column_width, base_row_height*4, base_column_width*10, 50),
    text="Chest Exercises",
    manager=ui_manager
)

shoulders_directory_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(base_column_width, base_row_height*6, base_column_width*10, 50),
    text="Shoulders Exercises",
    manager=ui_manager
)

abs_directory_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(base_column_width, base_row_height*8, base_column_width*10, 50),
    text="Abs Exercises",
    manager=ui_manager
)

back_directory_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(base_column_width, base_row_height*10, base_column_width*10, 50),
    text="Back Exercises",
    manager=ui_manager
)

legs_directory_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(base_column_width, base_row_height*12, base_column_width*10, 50),
    text="Legs Exercises",
    manager=ui_manager
)

exercise_directory_headings_elements = [
    exercise_directory_heading,
    arms_directory_button,
    chest_directory_button,
    shoulders_directory_button,
    back_directory_button,
    abs_directory_button,
    legs_directory_button,
]

def create_exercise_elements(muscle_group):
    """Generate UI elements for a specific muscle group's exercises"""
    elements = []
    
    # Create heading
    heading = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect(base_column_width, base_row_height, -1, 20),
        text=f"{muscle_group.title()} Exercises",
        manager=ui_manager
    )
    elements.append(heading)
    
    # Create elements for each exercise
    for index, exercise in enumerate(EXERCISES[muscle_group]):
        exercise_box = pygame_gui.elements.UITextBox(
            relative_rect=pygame.Rect(
                base_column_width, 
                base_row_height*(3 + index*3), 
                base_column_width*10, 
                80
            ),
            html_text=f"{exercise['name']} \n{exercise['description']}",
            manager=ui_manager
        )
        elements.append(exercise_box)
    
    # DELETE ONCE FINISHED WITH ITERATION 3
    # # Add back button
    # back_to_directory_button = pygame_gui.elements.UIButton(
    #     relative_rect=pygame.Rect(base_column_width, base_row_height*21, base_column_width*10, 50),
    #     text="Back to Exercise Directory",
    #     manager=ui_manager
    # )
    # # it will have an index of -1 as it is the last item in the list
    # elements.append(back_to_directory_button)
    
    return elements

# Then you can replace the manual element creation with:
chest_exercises_elements = create_exercise_elements("chest")
arms_exercises_elements = create_exercise_elements("arms")
shoulders_exercises_elements = create_exercise_elements("shoulders")
abs_exercises_elements = create_exercise_elements("abs")
back_exercises_elements = create_exercise_elements("back")
legs_exercises_elements = create_exercise_elements("legs")


# Navigation related things
class ClickableIcon:
    def __init__(self, image: str, position: list[int, int], size: list[int, int], onclick):
        self.image = image
        self.position = position
        self.size = size
        
        self.surface = pygame.image.load(os.path.join(image))
        self.rect = self.surface.get_rect()
        self.rect.center = self.position
        
        self.onclick = onclick
        self.enabled = False
        self.visible = True
    
    def on_click(self):
        if self.enabled:
            self.onclick()
    
    def enable(self):
        self.enabled = True
        
    def disable(self):
        self.enabled = False
    
    def show(self):
        self.visible = True
    
    def hide(self):
        self.visible = False
    
    def draw(self):
        if self.visible:
            SCREEN.blit(self.surface, self.rect)

exercise_directory_icon = ClickableIcon(
    "../Assets/notebook-text.png",
    (base_column_width*9, base_row_height*23), 
    (32, 32),
    lambda: app_manager.change_state(
        "Exercise Directory Headings", 
        exercise_directory_headings_elements, 
        app_manager.current_elements
    )
)

workout_icon = ClickableIcon(
    "../Assets/dumbbell.png",
    (base_column_width*6, base_row_height*23), 
    (32, 32),
    lambda: app_manager.change_state("Home", 
        home_elements, 
        app_manager.current_elements
    )
)

workout_generation_icon = ClickableIcon(
    "../Assets/sparkles.png",
    (base_column_width*3, base_row_height*23), 
    (32, 32),
    lambda: app_manager.change_state("Onboarding", 
        onboarding_elements, 
        app_manager.current_elements
    )
)

navigation_icons = [exercise_directory_icon, workout_icon, workout_generation_icon]

# Hide all elements at first
for element in [
    *loading_elements, 
    *onboarding_elements, 
    *home_elements, 
    *exercise_directory_headings_elements, 
    *chest_exercises_elements,
    *arms_exercises_elements,
    *shoulders_exercises_elements,
    *abs_exercises_elements,
    *back_exercises_elements,
    *legs_exercises_elements,
    ]:
    
    element.hide()

