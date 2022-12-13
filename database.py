
import sqlite3
import datetime

from habittracker import model
from typing import List

def connect_db(db_name="habit.db"):
    db = sqlite3.connect(db_name)
    create_tables(db)
    return db

def create_tables(db):
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habitbase (
        habit TEXT PRIMARY KEY,
        description TEXT,
        periodicity TEXT,
        starting_date TEXT,
        completed INTEGER,
        datetime_completed TEXT,
        streak INTEGER,
        breaking_habit TEXT
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS habitlog (
        habit TEXT,
        completed INT,
        streak INTEGER DEFAULT 0,
        datetime_completed TIME,
        breaking_habit TIME,
        FOREIGN KEY (habit) REFERENCES habitbase(habit)
    )""")
    db.commit()


def insert_habit(db, habit, description, periodicity, date_added, datetime_completed, completed, streak, breaking_habit):
    cur = db.cursor()
    cur.execute("INSERT INTO habitbase VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (habit, description, periodicity, date_added, datetime_completed, completed, streak, breaking_habit))
    db.commit()


def delete_habit(db, habit):
    cur = db.cursor()
    cur.execute("DELETE FROM habitbase WHERE habit = ?", (habit,))
    db.commit()
    reset_log(db, habit)


def all_habits(db) -> List[model.Habit]:
   cur = db.cursor()
   cur.execute("SELECT * FROM habitbase")
   results = cur.fetchall()
   habits = []
   for result in results:
    habits.append(model.Habit(*result))
   return habits 


def all_log(db) -> List[model.Habit]:
    cur = db.cursor()
    cur.execute("SELECT * FROM habitlog")
    results = cur.fetchall()
    logs = []
    for result in results:
        logs.append(model.Habit(*result))
    return logs
        

def certain_habit(db, habit) -> List[model.Habit]:
    cur = db.cursor()
    cur.execute("SELECT * FROM habitbase WHERE habit = ?", (habit,))
    result = cur.fetchone()
    return result


def certain_periodicity(db, periodicity) -> List[model.Habit]:
    cur = db.cursor()
    cur.execute("SELECT * FROM habitbase WHERE periodicity = ?", (periodicity,))
    results = cur.fetchall()
    periodicitys = []
    for result in results:
        periodicitys.append(model.Habit(*result))
    return periodicitys


def periodicity_of_habit(db, habit):
    cur = db.cursor()
    cur.execute("SELECT periodicity FROM habitbase WHERE habit = ?", (habit,))
    result = cur.fetchone()
    return result[0]


def change_habit_periodicity(db, habit, new_periodicity):
    cur = db.cursor()
    cur.execute("UPDATE habitbase SET periodicity = ?, streak = 0, datetime_completed = NULL WHERE habit = ?", (habit, new_periodicity))
    db.commit()
    reset_log(db, habit)
    

def habit_existing_check(db, habit):
    cur = db.cursor()
    cur.execute("SELECT * FROM habitbase WHERE habit = ?", (habit,))
    result = cur.fetchone()
    return True if result is not None else False


def periodicity_existing_check(db, periodicity):
    cur = db.cursor()
    cur.execute("SELECT * FROM habitbase WHERE periodicity = ?", (periodicity,))
    result = cur.fetchall()
    return True if result is not None else False


def habit_completed_check(db, habit):
    cur = db.cursor()
    cur.execute("SELECT completed FROM habitbase WHERE habit = ?", (habit,))
    result = cur.fetchone()
    return True if result == 2 else False


def insert_habitlog(db, habit, completed, streak, datetime_completed, breaking_habit):
    cur = db.cursor()
    cur.execute("INSERT INTO habitlog VALUES (?, ?, ?, ?, ?)", (habit, completed, streak, datetime_completed, breaking_habit))
    db.commit()


def update_habitlog(db, habit, completed, streak, datetime_completed, breaking_habit):
    cur = db.cursor()
    cur.execute("UPDATE habitlog SET completed = ?, streak = ?, datetime_completed = ?, breaking_habit = ? WHERE habit = ?", (completed, streak, datetime_completed,breaking_habit, habit))
    db.commit()


def streak_count(db, habit):
    cur = db.cursor()
    cur.execute("SELECT streak FROM habitbase WHERE habit = ?", (habit,))
    count = cur.fetchall()
    return count[0][0]


def update_habit_streak(db, habit, streak, datetime_completed=None):
    cur = db.cursor()
    cur.execute("UPDATE habitbase SET streak = ?, datetime_completed = ?  WHERE habit = ?", (streak, datetime_completed, habit))
    db.commit()


def reset_log(db, habit):
    cur = db.cursor()
    cur.execute("DELETE FROM habitlog WHERE habit = ?", (habit,))
    db.commit()


def habit_completed_time(db, habit):
    cur = db.cursor()
    cur.execute("SELECT datetime_completed FROM habitbase WHERE habit = ?", (habit,))
    result = cur.fetchone()
    return result[0]


def complete_habit(db, habit):
    cur = db.cursor()
    cur.execute("UPDATE habitbase SET completed = 2, datetime_completed = DATETIME('now', 'localtime') WHERE habit = ?", (habit,))
    db.commit()


def uncomplete_habit(db, habit):
    cur = db.cursor()
    cur.execute("UPDATE habitbase SET completed = 1 WHERE habit = ?", (habit,))
    db.commit()


def collect_habits_choices(db):
    cur = db.cursor()
    cur.execute("Select habit FROM habitbase")
    result = cur.fetchall()
    return [i[0].capitalize() for i in list(result)] if len(result) >0 else None