class User:
    def __init__(self, name, height, weight, flexibility, strength, endurance):
        #super().__init__()
        self.name = name
        self.height = height
        self.weight = weight
        self.flexibility = flexibility
        self.strength = strength
        self.endurance = endurance
    
    def get_start_height(self):
        return self.height
    
    def set_start_weight(self, new_start_height):
        self.height = new_start_height
    
    def get_start_weight(self):
        return self.weight
    
    def set_start_weight(self, new_start_weight):
        self.weight = new_start_weight 
    
    def get_start_flexibility(self):
        return self.flexibility
    
    def set_start_flexibility(self, new_start_flexibility):
        self.flexibility = new_start_flexibility
        
    def get_start_strength(self):
        return self.strength
    
    def set_start_strength(self, new_start_stength):
        self.strength = new_start_stength
        
    def get_start_endurance(self):
        return self.endurance
    
    def set_start_endurance(self, new_start_endurance):
        self.endurance = new_start_endurance
    
   
