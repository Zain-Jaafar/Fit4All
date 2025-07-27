

class User:
    def __init__(self, 
                 age: int, 
                 injuries: str, 
                 disabilities: str, 
                 time_availability: int, 
                 other_information: str):
        
        self.age = age
        self.injuries = injuries
        self.disabilities = disabilities
        self.time_availability = time_availability
        self.other_information = other_information
    