
from habittracker import database, model
from typing import List

def all_habits_information(db) -> List[model.Habit]:
   """
    Collect all habit information from the database.

    Parameters:
    db (sqlite3.Connection): The connection to the habits database.

    Returns:
    List[model.Habit]: A list of all habit information in the database.
    """
   cur = db.cursor()
   cur.execute("SELECT * FROM habitbase")
   results = cur.fetchall()
   all_data = []
   for result in results:
      all_data.append(model.Habit(*result))
   return all_data

def all_habits_log(db) -> List[model.LogEntry]:
   """
    Collect the log entries for all habits in the database.

    Parameters:
    db (sqlite3.Connection): The connection to the habits database.

    Returns:
    List[model.LogEntry]: A list of log entries for all habits in the database.
    """
   cur = db.cursor()
   cur.execute("SELECT * FROM habitlog")
   results = cur.fetchall()
   logs = [model.LogEntry(*row) for row in results]
   return logs

def max_streak_all_habits(db) -> List[model.LogEntry]:
   """
    Collect the log entries with the maximum streak from the database.

    Parameters:
    db (sqlite3.Connection): The connection to the habits database.

    Returns:
    List[model.LogEntry]: A list of log entries with the maximum streak in the database.
    """
   cur = db.cursor()
   cur.execute("SELECT * FROM habitlog WHERE max_streak = (SELECT MAX(max_streak) FROM habitlog)")
   results = cur.fetchall()
   logs = [model.LogEntry(*row) for row in results]
   return logs

def max_streak_given_habit(db, habit) -> List[model.LogEntry]:
   """
    Collect the log entries for a specific habit with the maximum streak from the database.

    Parameters:
    db (sqlite3.Connection): The connection to the habits database.
    habit (str): The habit to collect log entries for.

    Returns:
    List[model.LogEntry]: A list of log entries for the specified habit with the maximum streak in the database.
    """
   cur = db.cursor()
   cur.execute(f"SELECT * FROM habitlog WHERE habit = ?", (habit,))
   results = cur.fetchall()
   logs = [model.LogEntry(*row) for row in results]
   return logs

def habit_custom_perdiodicity_information(db, periodicity) -> List[model.Habit]:
   """
    Collect habit information from the database with a specific periodicity.

    Parameters:
    db (sqlite3.Connection): The connection to the habits database.
    periodicity (str): The periodicity of the habits to collect.

    Returns:
    List[model.Habit]: A list of habit information with the specified periodicity in the database.
    """
   cur = db.cursor()
   cur.execute("SELECT * FROM habitbase WHERE periodicity = ?", (periodicity,))
   results = cur.fetchall()
   periodicitys = []
   for result in results:
      periodicitys.append(model.Habit(*result))
   return periodicitys