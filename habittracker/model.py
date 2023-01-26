import datetime

from habittracker import database

class Habit:
    """A class representing a habit.

    Attributes:
        habit (str): The name of the habit.
        description (str): A description of the habit.
        periodicity (str): The periodicity of the habit (e.g. daily, weekly).
        starting_date (str): The date that the habit was started.
        completed (int): The number of times the habit has been completed.
        datetime_completed (str): The date and time that the habit was last completed.
        streak (int): The current streak of consecutive days the habit has been completed.
        max_streak (int): The longest streak of consecutive days the habit has been completed.
        db (str): The path to the database file.
        current_time (str): The current time as a string in the format '%d %b %Y %H:%M:%S'.
        current_date (str): The current date as a string in the format '%d %b %Y'.

    """
    def __init__(self, habit: str = None, description: str = None, periodicity: str = None, starting_date = None, startdate_weekly= None, completed = None, datetime_completed = None, streak = None, max_streak = None, db=None ):
        """
        Initialize a Habit object.

        Args:
            habit (str, optional): The name of the habit. Defaults to None.
            description (str, optional): A description of the habit. Defaults to None.
            periodicity (str, optional): The periodicity of the habit. Defaults to None.
            starting_date (str, optional): The date that the habit was started. Defaults to the current date.
            completed (int, optional): The number of times the habit has been completed. Defaults to 1.
            datetime_completed (str, optional): The date and time that the habit was last completed. Defaults to None.
            streak (int, optional): The current streak of consecutive days the habit has been completed. Defaults to 0.
            max_streak (int, optional): The longest streak of consecutive days the habit has been completed. Defaults to 0.
            db (str, optional): The path to the database file. Defaults to 'habit.db'.

        """
        self.habit = habit
        self.description = description
        self.periodicity = periodicity
        self.starting_date = starting_date if starting_date is not None else datetime.datetime.now().strftime("%d %b %Y")
        self.startdate_weekly = startdate_weekly if startdate_weekly is not None else None
        self.completed = completed if completed is not None else 1
        self.datetime_completed = datetime_completed if datetime_completed is not None else None
        self.streak = streak if streak is not None else 0
        self.max_streak = max_streak if max_streak is not None else 0
        self.db = db
        self.current_time = datetime.datetime.now().strftime("%d %b %Y %H:%M:%S")
        self.current_date = datetime.datetime.now().strftime("%d %b %Y")


    def add_habit(self, db_name):
        """
        Add a habit to the database.

        Inserts the habit and its details into the 'habits' table, and inserts a row into the 'habitlog' table with initial values.

        """
        if self.periodicity == "Daily":
            self.db = database.connect_db(db_name=db_name)
            database.insert_habit(self.db, self.habit, self.description, self.periodicity, self.starting_date, self.startdate_weekly, self.completed, self.datetime_completed, self.streak, self.max_streak)
            database.insert_habitlog(self.db, self.habit, 1, 0, self.datetime_completed, 0)
        else:
            self.db = database.connect_db(db_name=db_name)
            database.insert_habit(self.db, self.habit, self.description, self.periodicity, self.starting_date, self.current_date, self.completed, self.datetime_completed, self.streak, self.max_streak)
            database.insert_habitlog(self.db, self.habit, 1, 0, self.datetime_completed, 0)


    def delete_habit(self, db_name):
        """
        Delete a habit from the database.

        Removes the habit from the 'habits' table and removes all related rows from the 'habitlog' table.

        """
        self.db = database.connect_db(db_name=db_name)
        database.delete_habit(self.db, self.habit)
        database.reset_log(self.db, self.habit)

    def increment_streak(self, db_name):
        """
        Increment the current streak for a habit.

        Updates the `streak` and `max_streak` attributes for the habit, using the current streak and maximum streak values from the database.

        """
        self.db = database.connect_db(db_name)
        self.streak = database.streak_count(self.db, self.habit) + 1
        self.max_streak = database.max_streak_count(self.db, self.habit)
        if self.streak > self.max_streak:
            self.max_streak = self.streak
            self.max_streak = max(self.max_streak, self.streak)
            self.update_max_streak()

    def update_max_streak_in_database(self, db_name):
        """Update the maximum streak value in the database."""
        self.db = database.connect_db(db_name)
        database.update_habit_streak(self.db, self.habit, database.streak_count(self.db, self.habit), self.max_streak, self.current_date)
        database.update_habitlog(self.db, self.habit, 2, database.streak_count(self.db, self.habit), self.current_time, self.max_streak)

    def update_streak(self, db_name, current_date):
        """Update the streak information for a habit in the database.

        Increments the current streak, updates the `completed` attribute, and updates the streak and maximum streak values in the 'habits' and 'habitlog' tables in the database.

        """
        self.db = database.connect_db(db_name)
        self.set_habit_completed(db_name)
        self.increment_streak(db_name)
        database.update_habit_streak(self.db, self.habit, self.streak, self.max_streak, current_date)
        database.update_habitlog(self.db, self.habit, 2, database.streak_count(self.db, self.habit), self.current_time, database.max_streak_count(self.db, self.habit))

    def reset_streak(self, db_name):
        """
        Reset the current streak for a habit.

        Sets the `streak` attribute to 0 and updates the streak value in the 'habitsbase' and 'habitlog' tables in the database.

        """
        self.db = database.connect_db(db_name)
        self.streak = database.streak_count(self.db, self.habit)
        self.streak = 0
        database.reset_habitbase_streak(self.db, self.habit)
        database.reset_habitlog_streak(self.db, self.habit)

    def update_max_streak(self):
        """
        This function updates the attribute 'max_streak' with the current value of 'streak' if 'streak' is greater than 'max_streak'. It also updates the max_streak in the database.
        
        Attributes:
        self.streak (int) : current streak value
        self.max_streak (int) : max streak value
        
        Methods called:
        update_max_streak_in_database(db_name="habit.db")

        Returns: None
        """
        if self.streak > self.max_streak:
            self.max_streak = self.streak
            self.update_max_streak_in_database(db_name="habit.db")

    def set_habit_completed(self, db_name):
        """
        Mark a habit as completed in the database.

        Sets the `completed` attribute to 2 and updates the 'habits' table in the database.

        """
        self.db = database.connect_db(db_name)
        self.completed = 2
        database.complete_habit(self.db, self.habit)

    def set_habit_uncomplete(self, db_name):
        """
        Mark a habit as not completed in the database.

        Sets the `completed` attribute to 1 and updates the 'habits' and 'habitlog' tables in the database.

        """
        self.db = database.connect_db(db_name)
        self.completed = 1
        database.uncomplete_habit(self.db, self.habit)
        database.set_habitlog_uncompleted(self.db, self.habit, 1)

    def set_new_startdate_weekly(self, db_name):
        """
        This function sets a new startdate_weekly attribute to the current date and updates the startdate_weekly in the database.
        
        Attributes:
        self.db (object) : database object
        self.startdate_weekly (str) : current startdate_weekly value
        self.habit (str) : habit name
        self.current_date (str): current date
        
        Methods called:
        connect_db(db_name) from module 'database'
        set_startdate_weekly(self.db, self.habit, self.startdate_weekly) from module 'database'

        Returns: None
        """
        self.db = database.connect_db(db_name)
        self.startdate_weekly = self.current_date
        database.set_startdate_weekly(self.db, self.habit, self.startdate_weekly)
        
    def __repr__(self) -> str:
        """
        Return a string representation of the habit object.

        Returns:
            str: A string representation of the habit object, in the format '(habit, description, periodicity, starting_date, completed, datetime_completed, streak)'.

        """
        return f"({self.habit}, {self.description}, {self.periodicity}, {self.starting_date}, {self.startdate_weekly}, {self.completed}, {self.datetime_completed}, {self.streak})"


class LogEntry:
    """
    A class representing a log entry for a habit.

    Attributes:
        habit (str): The name of the habit.
        completed (int): The number of times the habit has been completed.
        streak (int): The current streak of consecutive days the habit has been completed.
        datetime_completed (str): The date and time that the habit was last completed.
        max_streak (int): The longest streak of consecutive days the habit has been completed.

    """
    def __init__(self, habit, completed, streak, datetime_completed, max_streak):
        """
        Initialize a LogEntry object.

        Args:
            habit (str): The name of the habit.
            completed (int, optional): The number of times the habit has been completed. Defaults to 1.
            streak (int, optional): The current streak of consecutive days the habit has been completed. Defaults to 0.
            datetime_completed (str, optional): The date and time that the habit was last completed. Defaults to None.
            max_streak (int, optional): The longest streak of consecutive days the habit has been completed. Defaults to 0.

        """
        self.habit = habit
        self.completed = completed if completed is not None else 1
        self.streak = streak if streak is not None else 0
        self.datetime_completed = datetime_completed if datetime_completed is not None else None
        self.max_streak = max_streak if max_streak is not None else 0


    def __repr__(self) -> str:
        """
        Return a string representation of the log entry object.

        Returns:
            str: A string representation of the log entry object, in the format '(habit, completed, streak, datetime_completed, max_streak)'.

        """
        return f"({self.habit}, {self.completed}, {self.streak}, {self.datetime_completed}, {self.max_streak})"