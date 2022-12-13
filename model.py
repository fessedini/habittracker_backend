
from datetime import datetime

from habittracker import database

class Habit:
    def __init__(self, habit: str = None, description: str = None, periodicity: str = None, starting_date = None, completed = None, datetime_completed = None, streak = None, breaking_habit = None, db="habit.db"):
        self.habit = habit
        self.description = description
        self.periodicity = periodicity
        self.starting_date = starting_date if starting_date is not None else datetime.now().strftime("%c")
        self.completed = completed if completed is not None else 1
        self.datetime_completed = datetime_completed if datetime_completed is not None else None
        self.streak = streak if streak is not None else 0
        self.breaking_habit = breaking_habit if breaking_habit is not None else None
        self.db = database.connect_db()
        self.current_time = datetime.now().strftime("%c")


    def add_habit(self):
        database.insert_habit(self.db, self.habit, self.description, self.periodicity, self.starting_date, self.completed, self.datetime_completed, self.streak, self.breaking_habit)
        database.insert_habitlog(self.db, self.habit, 1, 0, self.datetime_completed, self.breaking_habit)


    def delete_habit(self):
        database.delete_habit(self.db, self.habit)
        database.reset_log(self.db, self.habit)

    def increment_streak(self):
        self.streak = database.streak_count(self.db, self.habit)
        self.streak += 1

    
    def decrease_streak(self):
        self.streak = database.streak_count(self.db, self.habit)
        self.streak = 0


    def downdate_streak(self):
        self.decrease_streak()
        database.update_habit_streak(self.db, self.habit, self.streak)
        database.update_log(self.db, self.habit, 1, database.streak_count(self.db, self.habit), self.datetime_completed, self.breaking_habit)


    def update_streak(self):
        self.increment_streak()
        database.update_habit_streak(self.db, self.habit, self.streak, self.current_time)
         


    def reset_streak(self):
        self.streak = database.streak_count(self.db, self.habit)
        self.streak = 0
        database.update_habit_streak(self.db, self.habit, self.streak)
        database.update_log(self.db, self.habit, 1 , 0 , self.datetime_completed, self.breaking_habit)


    def set_habit_completed(self):
        self.completed == 2
        database.complete_habit(self.db, self.habit)


    def set_habit_uncomplete(self):
        self.completed == 1
        database.uncomplete_habit(self.db, self.habit)
        database.update_log(self.db, self.habit, 1, 1, self.datetime_completed, self.breaking_habit)


    def check_habit_off(self):
        self.set_habit_completed()
        self.update_streak()
        database.update_habitlog(self.db, self.habit, 2, 1, self.datetime_completed, self.breaking_habit)



    def daily_streak_verification(self):
        last_completion = database.habit_completed_time(self.db, self.habit)
        current_streak = database.streak_count(self.db, self.habit)
        if current_streak == 0 or last_completion is None:
            return 1
        else:
            today = self.current_time
            date = datetime.strptime(today, "%c") - datetime.strptime(last_completion, "%c")
            return date.days


    def weekly_streak_verification(self):
        last_completion = database.habit_completed_time(self.db, self.habit)
        current_streak = database.streak_count(self.db, self.habit)
        if current_streak == 0 or last_completion is None:
            return 2
        else:
            today = self.current_time
            date = datetime.strptime(today, "%c") - datetime.strptime(last_completion,"%c")
            week = 3 if (date.days + 1) > 14 else (2 if (date.days + 1) > 7 else 1)
            return week


    def update_periodicity(self):
        database.change_habit_periodicity(self.db, self.habit, self.periodicity)
        database.update_log(self.db, self.habit, 1, 0, self.datetime_completed, self.breaking_habit)


    def __repr__(self) -> str:
        return f"({self.habit}, {self.description}, {self.periodicity}, {self.starting_date}, {self.completed}, {self.datetime_completed}, {self.streak}, {self.breaking_habit})"