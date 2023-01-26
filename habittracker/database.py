
import sqlite3

from habittracker import model
from typing import List

def connect_db(db_name=None):
    """
    Connect to a database.

    Args:
        db_name (str, optional): The name of the database file. Defaults to 'habit.db'.

    Returns:
        sqlite3.Connection: A connection to the database.

    """
    db_name = db_name or "habit.db"
    db = sqlite3.connect(db_name)
    create_tables(db)
    return db

def create_tables(db):
    """
    Create tables in a database.

    Args:
        db (sqlite3.Connection): A connection to the database.

    """
    cur = db.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS habitbase (
        habit TEXT PRIMARY KEY,
        description TEXT,
        periodicity TEXT,
        starting_date TEXT,
        startdate_weekly TEXT,
        completed INTEGER,
        datetime_completed TEXT,
        streak INTEGER,
        max_streak INTEGER
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS habitlog (
        habit TEXT,
        completed INT,
        streak INTEGER DEFAULT 0,
        datetime_completed TIME,
        max_streak INTEGER DEFAULT 0,
        FOREIGN KEY (habit) REFERENCES habitbase(habit)
    )""")
    db.commit()


def insert_habit(db, habit, description, periodicity, starting_date, startdate_weekly, completed, datetime_completed, streak, max_streak):
    """
    Insert a new habit into the 'habitbase' table in the database.

    Args:
        db (sqlite3.Connection): A connection to the database.
        habit (str): The name of the habit.
        description (str): A description of the habit.
        periodicity (str): The periodicity of the habit (e.g. daily, weekly).
        starting_date (str): The starting date of the habit.
        startdate_weelöy (str): The starting date for a weekly habit.
        completed (int): The number of times the habit has been completed.
        datetime_completed (str): The date and time that the habit was last completed.
        streak (int): The current streak of consecutive days the habit has been completed.
        max_streak (int): The longest streak of consecutive days the habit has been completed.

    """
    cur = db.cursor()
    cur.execute("INSERT INTO habitbase VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (habit, description, periodicity, starting_date, startdate_weekly, completed, datetime_completed, streak, max_streak))
    db.commit()

def delete_habit(db, habit):
    """
    Delete a habit from the 'habitbase' table in the database.

    Args:
        db (sqlite3.Connection): A connection to the database.
        habit (str): The name of the habit to be deleted.
    """
    cur = db.cursor()
    cur.execute("DELETE FROM habitbase WHERE habit = ?", (habit,))
    db.commit()
    reset_log(db, habit)

def all_habits(db) -> List[model.Habit]:
    """
    Retrieve all habits from the 'habitbase' table in the database.

    Args:
        db (sqlite3.Connection): A connection to the database.

    Returns:
        List[model.Habit]: A list of `Habit` objects representing the habits in the 'habitbase' table.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habitbase")
    results = cur.fetchall()
    habits = []
    for result in results:
        habits.append(model.Habit(*result))
    return habits 

def all_log(db) -> List[model.LogEntry]:
    """
    Retrieve all log entries from the 'habitlog' table in the database.

    Args:
        db (sqlite3.Connection): A connection to the database.

    Returns:
        List[model.LogEntry]: A list of `LogEntry` objects representing the log entries in the 'habitlog' table.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habitlog")
    results = cur.fetchall()
    logs = [model.LogEntry(*row) for row in results]
    return logs

def certain_periodicity(db, periodicity) -> List[model.Habit]:
    """
    Retrieve all habits with a certain periodicity from the 'habitbase' table in the database.

    Args:
        db (sqlite3.Connection): A connection to the database.
        periodicity (str): The periodicity to filter the habits by.

    Returns:
        List[model.Habit]: A list of `Habit` objects representing the habits with the specified periodicity in the 'habitbase' table.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habitbase WHERE periodicity = ?", (periodicity,))
    results = cur.fetchall()
    periodicitys = []
    for result in results:
        periodicitys.append(model.Habit(*result))
    return periodicitys

def periodicity_of_habit(db, habit):
    """
    Retrieve the periodicity of a habit from the 'habitbase' table in the database.

    Args:
        db (sqlite3.Connection): A connection to the database.
        habit (str): The name of the habit.

    Returns:
        str: The periodicity of the habit.
    """
    cur = db.cursor()
    cur.execute("SELECT periodicity FROM habitbase WHERE habit = ?", (habit,))
    result = cur.fetchone()
    return result[0]

def habit_existing_check(db, habit):
    """
    Check if a habit exists in the 'habitbase' table in the database.

    Args:
        db (sqlite3.Connection): A connection to the database.
        habit (str): The name of the habit.

    Returns:
        bool: `True` if the habit exists, `False` if it does not.
    """
    cur = db.cursor()
    cur.execute("SELECT * FROM habitbase WHERE habit = ?", (habit,))
    result = cur.fetchone()
    return True if result is not None else False

def habit_completed_check(db, habit):
    """
    Check the completion status of a habit in the 'habitbase' table in the database.

    Args:
        db (sqlite3.Connection): A connection to the database.
        habit (str): The name of the habit.

    Returns:
        int: The completion status of the habit. 1 if the habit is not completed, 2 if it is.
    """
    cur = db.cursor()
    cur.execute("SELECT completed FROM habitlog WHERE habit = ?", (habit,))
    completed = cur.fetchone()[0]
    return completed

def insert_habitlog(db, habit, completed, streak, datetime_completed, max_streak):
    """
    Insert a new log entry for a habit into the 'habitlog' table in the database.

    Args:
        db (sqlite3.Connection): A connection to the database.
        habit (str): The name of the habit.
        completed (int): The completion status of the habit.
        streak (int): The current streak count for the habit.
        datetime_completed (str): The date and time that the habit was completed.
        max_streak (int): The maximum streak count for the habit.
    """
    cur = db.cursor()
    cur.execute("INSERT INTO habitlog VALUES (?, ?, ?, ?, ?)", (habit, completed, streak, datetime_completed, max_streak))
    db.commit()

def update_habitlog(db, habit, completed, streak, datetime_completed, max_streak):
    """
    Update the log entry for a habit in the 'habitlog' table in the database.

    Args:
        db (sqlite3.Connection): A connection to the database.
        habit (str): The name of the habit.
        completed (int): The completion status of the habit.
        streak (int): The current streak count for the habit.
        datetime_completed (str): The date and time that the habit was completed.
        max_streak (int): The maximum streak count for the habit.
    """
    cur = db.cursor()
    cur.execute("UPDATE habitlog SET completed = ?, streak = ?, datetime_completed = ?, max_streak = ? WHERE habit = ?", (completed, streak, datetime_completed, max_streak, habit))
    db.commit()

def set_habitlog_uncompleted(db, habit, completed):
    """
    Set the completion status of a habit's log entry in the 'habitlog' table to incomplete.

    Args:
        db (sqlite3.Connection): A connection to the database.
        habit (str): The name of the habit.
        completed (int): The completion status of the habit.
    """
    cur = db.cursor()
    cur.execute("UPDATE habitlog SET completed = ? WHERE habit = ?", (completed, habit))
    db.commit()

def streak_count(db, habit):
    """
    Given a database connection object (db) and a habit name, returns the current streak count for the habit from 'habitbase' table.
    If no streak count is found, returns None.
    If there is an sqlite3 error, it prints the error and returns None
    
    :param db: sqlite3 database connection object
    :type db: sqlite3.Connection
    :param habit: name of the habit to retrieve streak count for
    :type habit: str
    :return: the current streak count for the habit, or None if not found or an error occurred
    :rtype: int or None
    """
    cur = db.cursor()
    cur.execute("SELECT streak FROM habitbase WHERE habit = ?", (habit,))
    count = cur.fetchone()
    return count[0]


def max_streak_count(db, habit):
    """
    Retrieve the maximum streak count for a habit from the 'habitbase' table in the database.
    
    :param db: sqlite3 database connection object
    :type db: sqlite3.Connection
    :param habit: name of the habit to retrieve maximum streak count for
    :type habit: str
    :return: the maximum streak count for the habit, or None if not found or an error occurred
    :rtype: int or None
    """
    cur = db.cursor()
    try:
        cur.execute("SELECT max_streak FROM habitbase WHERE habit = ?", (habit,))
        count = cur.fetchone()
        if count:
            return count[0]
        else:
            return None
    except sqlite3.Error as e:
        print(e)
        return None

def reset_habitlog_streak(db, habit):
    cur = db.cursor()
    cur.execute("UPDATE habitlog SET streak = 0 WHERE habit = ?", (habit,))
    db.commit()

def reset_habitbase_streak(db, habit):
    cur = db.cursor()
    cur.execute("UPDATE habitbase SET streak = 0 WHERE habit = ?", (habit,))
    db.commit()

def update_habit_streak(db, habit, streak, max_streak, datetime_completed = None):
    """
    Updates the streak and maximum streak of a habit in the habitbase table.
    If a value for datetime_completed is provided, it also updates the datetime_completed column in the habitbase table.
    
    Parameters:
    db (sqlite3.Connection): The database connection object.
    habit (str): The habit to update.
    streak (int): The current streak for the habit.
    max_streak (int): The maximum streak for the habit.
    datetime_completed (datetime.datetime, optional): The date and time the habit was completed. Defaults to None.
    
    Returns:
    None

    """
    cur = db.cursor()
    cur.execute("UPDATE habitbase SET streak = ?, max_streak = ?, datetime_completed = ?  WHERE habit = ?", (streak, max_streak, datetime_completed, habit))
    db.commit()

def reset_log(db, habit):
    """
    Deletes all rows from the habitlog table for a given habit.
    
    Parameters:
    db (sqlite3.Connection): The database connection object.
    habit (str): The habit to reset the log for.
    
    Returns:
    None
    """
    cur = db.cursor()
    cur.execute("DELETE FROM habitlog WHERE habit = ?", (habit,))
    db.commit()

def habit_completed_time(db, habit):
    """
    Returns the datetime_completed for the most recent completion of the habit from the habitlog table.
    
    Parameters:
    db (sqlite3.Connection): The database connection object.
    habit (str): The habit to get the completion time for.
    
    Returns:
    datetime.datetime: The datetime_completed for the most recent completion of the habit.
    """
    cur = db.cursor()
    cur.execute("SELECT datetime_completed FROM habitbase WHERE habit = ?", (habit,))
    result = cur.fetchone()
    return result[0]

def complete_habit(db, habit):
    """
    Mark the habit as completed in the database.

    Parameters:
    db (sqlite3.Connection): The connection to the habits database.
    habit (str): The habit to mark as completed.

    Returns:
    None
    """
    cur = db.cursor()
    cur.execute("UPDATE habitbase SET completed = 2 WHERE habit = ?", (habit,))
    db.commit()

def uncomplete_habit(db, habit):
    """
    Mark the habit as not completed in the database.

    Parameters:
    db (sqlite3.Connection): The connection to the habits database.
    habit (str): The habit to mark as not completed.

    Returns:
    None
    """
    cur = db.cursor()
    cur.execute("UPDATE habitbase SET completed = 1 WHERE habit = ?", (habit,))
    db.commit()
    
def set_startdate_weekly(db, habit, startdate_weekly):
    """
    This function updates the startdate_weekly in the habitsbase table of the database specified by 'db' for the habit specified by 'habit' with the new startdate_weekly value specified by 'startdate_weekly'.
    
    Arguments:
    db (object) : database object
    habit (str) : habit name
    startdate_weekly (str) : new startdate_weekly value
    
    Methods called:
    execute() from cursor object
    commit() from database object
    
    Returns: None
    """
    cur= db.cursor()
    cur.execute("UPDATE habitbase SET startdate_weekly = ? WHERE habit = ?", (startdate_weekly, habit))
    db.commit()

def get_startdate_weekly(db, habit):
    """
    This function retrieves the startdate_weekly from the habitbase table of the database specified by 'db' for the habit specified by 'habit'
    
    Arguments:
    db (object) : database object
    habit (str) : habit name
    
    Methods called:
    execute() from cursor object
    fetchone() from cursor object
    
    Returns:
    result[0] (str) : startdate_weekly value of the habit
    """
    cur = db.cursor()
    cur.execute("SELECT startdate_weekly FROM habitbase WHERE habit = ?", (habit,))
    result = cur.fetchone()
    return result[0]

def get_starting_date(db, habit):
    """
    This function retrieves the starting_date from the habitbase table of the database specified by 'db' for the habit specified by 'habit'
    
    Arguments:
    db (object) : database object
    habit (str) : habit name
    
    Methods called:
    execute() from cursor object
    fetchone() from cursor object

    Returns:
    result[0] (str) : starting_date value of the habit
    """
    cur = db.cursor()
    cur.execute("SELECT starting_date FROM habitbase WHERE habit = ?", (habit,))
    result = cur.fetchone()
    return result[0]
    

def collect_habits_choices(db):
    """
    Collect the habit choices from the database.

    Parameters:
    db (sqlite3.Connection): The connection to the habits database.

    Returns:
    List[str] or None: A list of habit choices, or None if there are no habits in the database.
    """
    cur = db.cursor()
    cur.execute("SELECT habit FROM habitbase")
    result = cur.fetchall()
    return [i[0].capitalize() for i in list(result)] if len(result) >0 else None

def collect_periodicity_habit_choices(db, periodicity):
    """
    Collect the habit choices from the database with a specific periodicity.

    Parameters:
    db (sqlite3.Connection): The connection to the habits database.
    periodicity (str): The periodicity of the habits to collect.

    Returns:
    List[str] or None: A list of habit choices with the specified periodicity, or None if there are no matching habits in the database.
    """
    cur = db.cursor()
    cur.execute("SELECT habit FROM habitbase WHERE periodicity = ?", (periodicity,))
    result = cur.fetchall()
    return [i[0].capitalize() for i in list(result)] if len(result) >0 else None

def collect_uncompleted_habits_choices(db):
    """
    Collect the uncompleted habit choices from the database.

    Args:
    db (sqlite3.Connection): The connection to the habits database.

    Returns:
    List[str] or None: A list of uncompleted habit choices, or None if there are no uncompleted habits in the database.
    """
    cur = db.cursor()
    cur.execute("SELECT habit FROM habitbase WHERE completed = 1")
    result = cur.fetchall()
    return [i[0].capitalize() for i in list(result)] if len(result) >0 else None