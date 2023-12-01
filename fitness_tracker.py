"""
Add new workout categories to the database
#Create custom routine by selecting from list of exercises
#Update a workout category
#Delete a workout category from the database
#Add a workout goal
#Add goal categories
#Delete a goal category from the database
#Calculate fitness goal progress based on the workouts and goals provided

"""
## SORRY! I know it's spaghetti and needs refactoring :( and some resturcture I've run out of time :(

import sqlite3
import csv
import os
import datetime
from datetime import date
from exercise import Exercise
from workout import Workout
from goals import Goal, LoseWeight, Strength_Flexibility
from user import User
        
        
# TO DO Clean up imported data: look into importing from CSV
def populate_list(filename, list):
    try:
        with open(filename, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                line = line.split(", ")
                if line[0] not in list:
                    list.append(line)
    except:
        print("Something went wrong when opening the file")
        

def populate_table(filename, list):
    populate_list(filename, list)
    #Insert data into database exercise, workout or goals tables
    cursor.executemany('''INSERT or IGNORE INTO exercise(exercise_id, exercise_category, repetitions, sets) VALUES(?,?,?,?)''', exercise_data)
    db.commit()
    cursor.executemany('''INSERT or IGNORE INTO workout(workout_id, workout_name, workout_category, workout_minutes, date_completed) VALUES(?,?,?,?,?)''', workout_data)
    db.commit()
    cursor.executemany('''INSERT or IGNORE INTO goals(goals_id, goal_name, goal_category, days_per_week, start_date, end_date) VALUES(?,?,?,?,?,?)''', goals_data)
    db.commit()
    cursor.executemany('''INSERT or IGNORE INTO user_goal_milestones(milestone_id, user_name, user_height_metres, current_weight, 
                       current_flexibility, current_strength, current_endurance, user_goal_category, current_date) 
                       VALUES(?,?,?,?,?,?,?,?,?)''', user_data)
    db.commit()
    

def export_to_csv(fileName, selection):
    try:
        csvFile = csv.writer(open(fileName, 'w', newline=''),
                             delimiter=',', lineterminator='\r\n',
                             quoting=csv.QUOTE_ALL, escapechar='\\')
        csvFile.writerows(selection)
        print("Data export successful.")
    except:
        print("Data export unsuccessful.")
        quit()
    finally: 
        db.close()
    
    
def input_number():
    while True:
        try:
            num = float(input("\n    Enter number: ").strip())
            break
        except ValueError:
            print("\n   Oops! That was not a valid entry. Try again...\n")
    return num


def confirm_choice(user_confirmation):
    if user_confirmation == 'Y':
        return True
    elif user_confirmation == 'N': 
        return False
    else:
       print("\n    No book was updated or deleted. You must enter Y or N only")


def search_database(query, table, column_title):
    if query.isnumeric():
        cursor.execute('''SELECT * FROM {table} WHERE id LIKE ?''', (query,))
        search_result = cursor.fetchall()
        if search_result == []:
            return None
        else:
            return search_result
    elif query.isnumeric() == False:
        db_search_query = f'%{query}%'
        cursor.execute(f'''SELECT * FROM {table} WHERE {column_title} LIKE ?''', (db_search_query,))
        search_result = cursor.fetchall()
        if search_result == []:
            return None
        else:
            return search_result
    else:
        print("    Value entered not recognised. Try searching again.")


def count_workouts_completed():
    recordCount = 0
    workout_list =  cursor.execute('''SELECT * from workout ORDER BY date_completed ''')
    #print(f"{current_date.day}-{current_date.month}-{current_date.year}")
    for workout in workout_list:
        recordCount +=1
        print('     {0} : {1} : {2} : {3} : {4}'.format(workout[0], workout[1], workout[2], workout[3], workout[4]))
    print(f"    \n   You have completed {recordCount} workouts since you started tracking your workouts")       
    

# Initialise empty lists to store imported data from text files
exercise_data = []
workout_data  = []
goals_data = []
user_data = []
#for use with Goals progress. 
#TO DO: Buld endurance not yet covered in Goals classes
exercise_goal_categories = ['Lose weight', 'Build strength', 'Increase flexibility', 'Stick to exercise plan', 'Build endurance']
#setting global user profile that can be updated as part of option 7
new_user = User("Tess", 1.7, 63.5, 2, 1.2, 6)

#Connect to the database
#Create a db called fitness_db with 4 tables, exercise, workout and goals, user goal milestones
try:
    db = sqlite3.connect('fitness_db')
    cursor = db.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS exercise(exercise_id INTEGER NOT NULL PRIMARY KEY, 
                                                        exercise_category TEXT,
                                                        repetitions INTEGER DEFAULT 1,
                                                        sets INTEGER DEFAULT 1)
                    ''')
    db.commit()
except Exception as DatabaseError:
    raise DatabaseError

try:
    db = sqlite3.connect('fitness_db')
    cursor = db.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS workout(workout_id INTEGER NOT NULL PRIMARY KEY, 
                                                        workout_name TEXT,
                                                        workout_category TEXT,
                                                        workout_minutes INTEGER, 
                                                        date_completed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                        FOREIGN KEY (workout_category) REFERENCES exercise(exercise_id))

                    ''')
    db.commit()
except Exception as DatabaseError:
    raise DatabaseError

try:
    db = sqlite3.connect('fitness_db')
    cursor = db.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS goals(goals_id INTEGER NOT NULL PRIMARY KEY, 
                                                    goal_name TEXT,
                                                    goal_category TEXT,
                                                    days_per_week INTEGER,
                                                    start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                    end_date TIMESTAMP)                          
                    ''')
    db.commit()
except Exception as DatabaseError:
    raise DatabaseError

                                                        
try:
    db = sqlite3.connect('fitness_db')
    cursor = db.cursor()
    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_goal_milestones(milestone_id INTEGER NOT NULL PRIMARY KEY, 
                                                            user_name TEXT,
                                                            user_height_metres REAL DEFAULT 1.7,
                                                            current_weight REAL,
                                                            current_flexibility REAL,
                                                            current_strength REAL,
                                                            current_endurance REAL,
                                                            user_goal_category TEXT,                                                      
                                                            current_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                                            FOREIGN KEY (user_goal_category) REFERENCES goals(goals_id))
                    ''')
    db.commit()
except Exception as DatabaseError:
    raise DatabaseError

# Call the function to populate the database exercise, workout and goals tables for further use in the program.
populate_table("input_data/exercise_input.txt", exercise_data)
populate_table("input_data/workout_input.txt", workout_data)
populate_table("input_data/goals_input.txt", goals_data)
populate_table("input_data/user_goal_milestones.txt", user_data)

"""user_weight_kg REAL, 
                                                            user_bmi REAL,
                                                            flexibility_distance_cm REAL,
                                                            strength_distance_metres REAL,
                                                            endurance_time REAL,"""

while True:
    # Present the user with choice menu
    # TO DO: Update 2. View exercise by category - restructue: add name to category database, so we also have types of exercises per category
    # TO DO: ^ This would also range: i.e., entering Yoga as an option for Balance, cardio, as well as strength
    # TO DO: Realised that 5 means I should create a weekly schedule? Would make more sense for user
    print("""\nWould you like to:
    1. Add exercise category
    2. View exercise by category 
    3. Delete exercise by category
    4. Create Workout Routine
    5. View Workout Routine
    6. View Exercise Progress
    7. Set Fitness Goals
    8. View Progress towards Fitness Goals
    9. Quit
""")
    user_choice = input_number()
       
    if user_choice == 1:
        #Add an exercise category to the database
        #View categories before adding one
        #TO DO: Allow user to update repetitions and sets numbers for the new category
        view_categories = search_database("", "exercise", "exercise_category")
        print("\n   The current categories are: ")
        for exercise in view_categories:
                print('     {0} : {1}'.format(exercise[0], exercise[1]))
        new_exercise_category = input("\n    Enter the new category to add: ")
        search_result = search_database(new_exercise_category, 'exercise', 'exercise_category')
        if search_result == None:
            print("\n   Enter recommended repetitions of exercise per routine: ")
            repetitions = input_number()
            print("\n   Enter number of sets to complete for each routine: ")
            sets = input_number()
            new_exercise = Exercise(new_exercise_category.strip(), repetitions, sets)
            cursor.execute('''INSERT or IGNORE INTO exercise(exercise_category, repetitions, sets) VALUES(?,?,?)''', (new_exercise.exercise_category,
                                                                                                                  new_exercise.repetitions,
                                                                                                                  new_exercise.sets))
            db.commit()
            print(f'\n   {new_exercise.exercise_category} added!')
        else:
            print("    Sorry this category already exists: ")
            for exercise in search_result:
                print('     {0} : {1} : {2} : {3}'.format(exercise[0], exercise[1], exercise[2], exercise[3]))
        db.commit()
       
    elif user_choice == 2:
        #View exercise by category
        #Only exercise workouts completed and logged by the user will be shown
        search_query = input("""    
                             Enter the category of exercise you wish to view: 
                             (Press enter to show all completed exercise/workouts completed)
                             """)
        print('\n      **** SEARCH RESULTS ****: \n')
        print('\n      **** ID ** EXERCISE ** CATEGORY ** MINUTES ** DATE COMPLETED ****')
        print('      _______________________________________________________________')
        search_result = search_database(search_query, 'workout', 'workout_category')
        db.commit()
        if search_result == None:
            print("    Sorry, no matches for your search")
        else:
            for workout in search_result:
                print('     {0} : {1} : {2} : {3} : {4}'.format(workout[0], workout[1], workout[2], workout[3], workout[4]))
        db.commit()
    
    
    elif user_choice == 3:
        #Delete exercise by category
        category_to_delete = input("    Enter catergory of exercises you wish to delete: ").strip()
        user_confirmation = input("\n   Are you sure you want to delete this category of exercises? Enter Y or N: ").strip().upper()
        choice = confirm_choice(user_confirmation)
        if choice:
            #  check category given by user is in db
            search_result = search_database(category_to_delete, 'exercise', 'exercise_category')
            if search_result == None: 
                print("   Sorry, no matches found with that exercise category. Try again.")
            else: 
                cursor.execute('''DELETE FROM exercise WHERE exercise_category = ? ''', (category_to_delete,))
                print(f'\n    Excercise category {category_to_delete} deleted!')
        elif choice == False:
             print('\n  Exercise category not deleted')
        else:
            print("\n   Oops! Something went wrong. Try again.")
    
    elif user_choice == 4:
        #Create workout routine
        new_workout_name = input("    Enter the name of the workout: ")
        workout_category = input("    Enter the category name for this routine: ")
        search_result = search_database(workout_category, 'workout', 'workout_category')
        if search_result == None:
            print(f"    Sorry, no matching category exists for {workout_category}")
            ##TO DO: FUNCTION - VIEW CATEGORIES
            continue
        else:
            print("     How long is/was the workout in minutes? ")
            length_in_minutes = input_number()
            new_workout_details = Workout(new_workout_name, workout_category, length_in_minutes)
            print(new_workout_details.name)
            cursor.execute('''INSERT or IGNORE INTO workout(workout_name, 
                                                            workout_category, workout_minutes) VALUES(?,?,?)''', 
                                                            (new_workout_details.name, new_workout_details.workout_category, 
                                                             new_workout_details.minutes))
            db.commit()
            print(f'\n   Exercise routine added to your workouts!')
        db.commit()
       
    elif user_choice == 5:
        # View workout routines
        search_query = input("    Enter the name of the routine you want to view (Hit return to view all): ")
        print('\n      ****SEARCH RESULTS****: \n')
        print('\n      ** NAME ** CATEGORY ** LENGTH(MINS) ** DATE COMPLETED **')
        print('      _______________________________________________________________')
        search_result = search_database(search_query, 'workout', 'workout_name')
        if search_result == None:
            print("    Sorry, no matches for workout search exist")
        else:
            for workout in search_result:
                print('     {0} : {1} : {2} : {3} : {4}'.format(workout[0], workout[1], workout[2], workout[3], workout[4]))
        db.commit()
        
        
    elif user_choice == 6:
        #View Exercise progress
        current_date = date.today()
        workout_count = count_workouts_completed()
        db.commit()
    
    
    elif user_choice == 7:
        user_confirmation = input('\n   Do want to reset your user profile, Y or N? ').strip()
        choice = confirm_choice(user_confirmation)
        if choice: 
            new_user.name = input("    Enter your name: ")
            print('\n   Enter your current measurements starting with : ')
            print('\n   Your current weight in kgs: ')
            new_user.weight = input_number()
            print('\n   Your flexibility score in cms: ')
            new_user.flexibility = input_number()
            print('\n   Your strength score in cms: ')
            new_user.strength = input_number()
            print('\n   Your endurance score in minutes: ')
            new_user.endurance = input_number()

        # Set Fitness goals
        new_goal_category = input("\n    Name your goal categry: ")
        print("\n     Days per week you want to exercise: ")
        days = input_number()
        current_date = datetime.datetime.now()
        print("\n     Goal end date YYYY-MM-DD: ")
        #TO DO: REFINE DATE ENTRY AND HANDING
        end_date = "2030-12-31"
        new_goal = Goal(new_user.name, new_goal_category, days, current_date, end_date)
        
        #Save new goal data to database
        cursor.execute('''INSERT or IGNORE INTO goals(goal_name, goal_category, days_per_week, start_date, end_date) VALUES(?,?,?,?,?)''', 
                        (new_user.name, new_goal_category, days, current_date, end_date))
        db.commit()
        print(f'\n   New goal added!')
        
        #Track User goal milestone, add to database so user can analyse previous entries
        cursor.execute('''INSERT or IGNORE INTO user_goal_milestones(user_name, user_height_metres, current_weight, 
                       current_flexibility, current_strength, current_endurance, user_goal_category, current_date) VALUES(?,?,?,?,?,?,?,?)''', 
                        (new_user.name, new_user.height, new_user.weight, new_user.flexibility, new_user.strength, new_user.endurance, new_goal.category, current_date))
        db.commit()
    
    
    elif user_choice == 8:
        #View progress towards fitness goals
        #Enter current stats so that they can be compared to a user's previous goal and milestone data
        name = input('\n    Enter your name: ')
        search_result = search_database(name, 'user_goal_milestones', 'user_name')
        db.commit()
        if search_result == None:
            print("    Sorry, no matches for your search")
        else:
            print("   Your current records show: ")
            for milestone in search_result:
                print('     {0} : {1} : {2} : {3} : {4} : {5} : {6} : {7} : {8}'.format(milestone[0], milestone[1], milestone[2], 
                                                                                        milestone[3], milestone[4], milestone[5],
                                                                                        milestone[6], milestone[7], milestone[8]))
        db.commit()
        #TO DO: Refactor - this field should logically go with User profile not Goal setting
        #Otherwise I have to ask the user to update this here so I can work with goal progress
        print('\n   Enter goal exercise days per week: ')
        days = input_number()
        date = date.today()
        
        #set current user profile for use with choice selected  
        #height can be same as new_user profile as won't change
        current_user_stats = User(name, new_user.height, new_user.weight, new_user.flexibility, new_user.strength, new_user.endurance)
        
        while True: 
            print('''\nWhich goal do you want to see overall progress for?:
                    1. Lose weight
                    2. Build Strength
                    3. Increase Flexibility
                    4. Stick to an exercise plan
                    0. Exit
                ''')
            goal_choice = input_number()
                
            if goal_choice == 1:
                goal = exercise_goal_categories[0]
                print('\n   Your current weight in kgs: ')
                weight = input_number()
                lose_weight_now = LoseWeight(current_user_stats.name, goal, days, date, date, weight)
                lose_weight_now.getWeightDiff(new_user.weight)
                bmi = lose_weight_now.getBMI(current_user_stats.height)
                print(f"\n  Your BMI is {bmi}")
             
            if goal_choice == 2:
                goal = exercise_goal_categories[1]
                print('\n   Your strength score in cms: ')
                strength = input_number()
                strength_flexibility_now = Strength_Flexibility(current_user_stats.name, goal, days, date, date, strength)
                diff = strength_flexibility_now.getDistanceDff(new_user.strength) #diff between original user profile score and now
                
                
            if goal_choice == 3: 
                goal = exercise_goal_categories[2]
                print('\n   Your flexibility score in cms: ')
                flexibility = input_number()
                strength_flexibility_now = Strength_Flexibility(current_user_stats.name, goal, days, date, date, flexibility)
                diff = strength_flexibility_now.getDistanceDff(new_user.flexibility) #diff between original user profile score and now
                
            if goal_choice == 4:
                goal = exercise_goal_categories[3]
                count_workouts_completed()
                #days_goal = Goal(current_user_stats.name, goal, days, date, date)
                #diff = days_goal.target_workout_number_for_goal()
                #print(f"\n You should have completed {diff} workouts.")
                        
            if goal_choice == 0:
                print("    Exiting updates. Returning to main menu.")
                break   
    
    
    elif user_choice == 9:
        workout_search_result = search_database("", 'workout', 'workout_category')
        export_to_csv('workout_output.csv', workout_search_result)
        print("\nClosing database connection. Goodbye")
        db.close()
        break
    
    else:
        print("    Oops - Incorrect input.")


