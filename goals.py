import datetime

class Goal:
    def __init__(self, name, category, days_per_week, start_date, end_date):
        #super().__init__()
        self.name = name
        self.category = category
        self.days_per_week = days_per_week
        self.start_date = start_date
        self.end_date = end_date
        
    def get_days(self):
        return self.days_per_week
    
    def set_days(self, new_days_number):
        self.days_per_week = new_days_number
        
    def get_start_date(self):
        return self.start_date
    
    def set_start(self, new_start_date):
        self.start_date = new_start_date
    
    def get_end_date(self):
        return self.end_date
    
    def set_end_date(self, new_end_date):
        self.end_date = new_end_date

    
    def getTimedDiff(self):
        diff = datetime(self.start_date) - datetime(self.end_date)
        return diff
    
    def target_workout_number_for_goal(self):
        #TO DO - Doesn't work right now - convert start and end times to timestamps?
        start = datetime.datetime(self.start_date) #format should be 2023,10,13 for this to work
        end = datetime.datetime(self.end_date)
        num_of_weeks = (end.day- start.day)/7
        total = num_of_weeks * self.days_per_week
        return total
        
class LoseWeight(Goal):
    def __init__(self, name, category, days_per_week, start_date, end_date, current_weight_kgs):
        super().__init__(name, category, days_per_week, start_date, end_date)
        self.current_weight_kgs = current_weight_kgs
        
    def get_current_weight(self):
        return self.current_weight_kgs
    
    def set_current_weight(self, new_current_weight):
        self.current_weight_kgs = new_current_weight
    
    def getBMI(self, height):
        bmi = self.current_weight_kgs/(height**2)
        return bmi
         
    def getWeightDiff(self, start):
        diff = start - self.current_weight_kgs
        if start > self.current_weight_kgs:
            print(f"\n  You have lost {diff} kgs.")
        elif self.current_weight_kgs > start:
            print(f"\n  You have gained {diff} kgs.")
        elif start == self.current_weight_kgs:
            print(f"\n Your weight has stayed the same.")
        else:
            print("Something went wrong with our calculations.")
            
class Strength_Flexibility(Goal):
    def __init__(self, name, category, days_per_week, start_date, end_date, current_distance_in_cms):
        super().__init__(name, category, days_per_week, start_date, end_date)
        self.current_distance_in_cms = current_distance_in_cms
        
    def getDistanceDff(self, distance):
        diff = self.current_distance_in_cms - distance
        
        if self.current_distance_in_cms > distance:
            print(f"\n  You have increased your score by {diff} cms ({diff}/100 m)!")
        elif distance > self.current_distance_in_cms:
            print(f"\n  You have decreased your score by {diff} cms ({diff}/100 m). Maybe you have an injury?")
        elif distance == self.current_distance_in_cms:
            print(f"\n  Your score hasn't changed. Keep at it!")
        else:
            print("Something went wrong with our calculations.")