

class User:
    def __init__(self, 
                 age: int, 
                 injuries: str, 
                 disabilities: str, 
                 time_availability: int, 
                 other_information: str):
        
        self.data = {
            "age": age, 
            "injuries": injuries, 
            "disabilities": disabilities, 
            "availability": time_availability, 
            "other_information": other_information
        }
    