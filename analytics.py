
from habittracker import database, model
from typing import List

def all_habits_information(db) -> List[model.Habit]:
   cur = db.cursor()
   cur.execute("SELECT * FROM habitbase")
   results = cur.fetchall()
   all_data = []
   for result in results:
      all_data.append(model.Habit(*result))
   return all_data


def habit_custom_perdiodicity_information(db, periodicity) -> List[model.Habit]:
   cur = db.cursor()
   cur.execute("SELECT * FROM habitbase WHERE periodicity = ?", (periodicity,))
   results = cur.fetchall()
   periodicitys = []
   for result in results:
      periodicitys.append(model.Habit(*result))
   return periodicitys


def habit_information(db, habit) -> List[model.Habit]:
   cur = db.cursor()
   cur.execute("SELECT * FROM habitbase WHERE habit = ?", (habit,))
   results = cur.fetchall()
   return results


def longest_habit_streak(db, habit) -> int:
   cur = db.cursor()
   cur.execute("SELECT MAX(streak) FROM habitlog WHERE habit = ?", (habit,))
   results = cur.fetchone()
   return results[0]


def habit_log(db, habit) -> List[model.Habit]:
   cur = db.cursor()
   cur.execute("SELECT * FROM habitlog WHERE habit = ?", (habit,))
   results = cur.fetchall()
   return results


