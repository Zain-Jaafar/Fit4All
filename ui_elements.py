import pygame_gui
import pygame

from utils import SCREEN_WIDTH, SCREEN_HEIGHT

ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), 'theme.json')

base_column_width = SCREEN_WIDTH/12
base_row_height = SCREEN_HEIGHT/24

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
                                        text="Do you have any injuries?",
                                        anchors={'bottom': 'bottom',
                                                 'right': 'right',
                                                 'bottom_target': injuries_input,
                                                 'right_target': injuries_input},
                                        manager=ui_manager)

disabilities_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(base_column_width, base_row_height*9, base_column_width*10, 50),
                                            placeholder_text="Enter any disabilities: ",
                                            manager=ui_manager)

disabilities_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, -20, -1, 20),
                                        text="Do you have any disabilities?",
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
]

back_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(base_column_width, base_row_height*21, base_column_width*10, 50),
                                             text="Back to Workout Generator",
                                             manager=ui_manager)

home_elements = [
    back_button
]

# Hide all elements at first
for element in onboarding_elements:
    element.hide()

back_button.hide()