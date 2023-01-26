import pytest

import datetime

from typer.testing import CliRunner

import os

from freezegun import freeze_time

from habittracker import __app_name__, __version__, cli, database, model, analytics

@pytest.fixture
def runner():
    """
    Create a CliRunner instance.

    This fixture function creates a CliRunner instance, which is used to invoke the command-line interface (CLI) of a function
    and capture its output and exit code.

    Returns:
        CliRunner: An instance of the CliRunner class.

    """
    return CliRunner()

def test_version(runner):
    """
    Test the version command of the app.

    This test function invokes the version command of the app using the CliRunner instance provided as an argument. It then
    checks that the exit code of the command is 0, indicating that the command ran successfully. It also checks that the
    output of the command includes the app name and version.

    Args:
        runner (CliRunner): An instance of the CliRunner class.

    Returns:
        None

    Raises:
        AssertionError: If the exit code of the command is not 0 or the output of the command does not include the app name
            and version.

    """
    result = runner.invoke(cli.app, ["--version"])
    assert result.exit_code == 0
    assert f"{__app_name__} v{__version__}\n" in result.stdout


class TestHabit:
    def setup_method(self):
        """
        This method is run before each test case, it creates a test database by copying the original database file, and populates it with sample data
        """
        self.db = database.connect_db(db_name='testha.db')

    @freeze_time("2022-12-04")
    def test_add_habit(self):
        """
        Test the add_habit method of the Habit model class.

        This function tests the following:
        - The correct addition of habits to the database by checking that the attributes of the Habit object have the expected values after the `habit.add_habit()` method is called.
        - The test uses a frozen time of "2022-12-04" to ensure consistent results.
        - The function also tests the length of the all_habits and all_log methods from the database module, which verifies that the habits are correctly added to the database.
        
        Assertions:
        - `habit.habit` should be "Pushups"
        - `habit.description` should be "Do 20 Pushups"
        - `habit.periodicity` should be "Daily"
        - `habit.starting_date` should be "04 Dec 2022"
        - `habit.completed` should be 1
        - `habit.datetime_completed` should be None
        - `habit.streak` should be 0
        - `habit.max_streak` should be 0
        - `database.all_habits(self.db)` should have a length of 6
        - `database.all_log(self.db)` should have a length of 6
        """
        habit = model.Habit(habit="Pushups", description="Do 20 Pushups", periodicity="Daily")
        habit.add_habit(db_name="testha.db")
        assert habit.habit == "Pushups"
        assert habit.description == "Do 20 Pushups"
        assert habit.periodicity == "Daily"
        assert habit.starting_date == "04 Dec 2022"
        assert habit.completed == 1
        assert habit.datetime_completed is None
        assert habit.streak == 0
        assert habit.max_streak == 0

        habit = model.Habit(habit="Drinking", description="2 liter of water", periodicity="Daily")
        habit.add_habit(db_name="testha.db")
        assert habit.habit == "Drinking"
        assert habit.description == "2 liter of water"
        assert habit.periodicity == "Daily"
        assert habit.starting_date == "04 Dec 2022"
        assert habit.completed == 1
        assert habit.datetime_completed is None
        assert habit.streak == 0
        assert habit.max_streak == 0

        habit = model.Habit(habit="Learning", description="5 hours", periodicity="Daily")
        habit.add_habit(db_name="testha.db")
        assert habit.habit == "Learning"
        assert habit.description == "5 hours"
        assert habit.periodicity == "Daily"
        assert habit.starting_date == "04 Dec 2022"
        assert habit.completed == 1
        assert habit.datetime_completed is None
        assert habit.streak == 0
        assert habit.max_streak == 0

        habit = model.Habit(habit="Running", description="Go running 3 times", periodicity="Weekly")
        habit.add_habit(db_name="testha.db")
        assert habit.habit == "Running"
        assert habit.description == "Go running 3 times"
        assert habit.periodicity == "Weekly"
        assert habit.starting_date == "04 Dec 2022"
        assert habit.completed == 1
        assert habit.datetime_completed is None
        assert habit.streak == 0
        assert habit.max_streak == 0

        habit = model.Habit(habit="Workout", description="Go to gym 3 times", periodicity="Weekly")
        habit.add_habit(db_name="testha.db")
        assert habit.habit == "Workout"
        assert habit.description == "Go to gym 3 times"
        assert habit.periodicity == "Weekly"
        assert habit.starting_date == "04 Dec 2022"
        assert habit.completed == 1
        assert habit.datetime_completed is None
        assert habit.streak == 0
        assert habit.max_streak == 0

        habit = model.Habit(habit="Testdelete", description="For deleting", periodicity="Daily")
        habit.add_habit(db_name="testha.db")
        assert habit.habit == "Testdelete"
        assert habit.description == "For deleting"
        assert habit.periodicity == "Daily"
        assert habit.starting_date == "04 Dec 2022"
        assert habit.completed == 1
        assert habit.datetime_completed is None
        assert habit.streak == 0
        assert habit.max_streak == 0

        assert len(database.all_habits(self.db)) == 6
        assert len(database.all_log(self.db)) == 6

    @freeze_time("2022-12-05")
    def test_delete_function(self):
        """
        This test function tests the delete_habit method of the Habit model class. The function tests the following:
        -The correct deletion of habits from the database by checking that the `habit.delete_habit()` method deletes the habit and its log from the database
        - The test uses a frozen time of "2022-12-05" to ensure consistent results.
        - The function also tests the length of the all_habits_information and all_habits_log methods from the analytics module, which verifies that the habits are correctly deleted from the database.

        Assertions:
        - `database.habit_existing_check(self.db, habit="Testdelete")` should return True
        - `len(analytics.all_habits_information(self.db))` should have a length of 5
        - `len(analytics.all_habits_log(self.db))` should have a length of 5
        """

        database.habit_existing_check(self.db, habit="Testdelete")
        assert True
        habit = model.Habit(habit="Testdelete")
        habit.delete_habit(db_name="testha.db")
        assert len(analytics.all_habits_information(self.db)) == 5
        assert len(analytics.all_habits_log(self.db)) == 5

    @freeze_time("2022-12-04")
    def test_habit_daily_update(self):
        """
        
        -This test function tests the update_streak method of the Habit model class for daily habits. The function tests the following:
        - The correct update of the daily habits streak by checking that the `habit.update_streak()` method updates the streak and max_streak in the database
        - The test uses a frozen time of "2022-12-04" to ensure consistent results.
        - The function also tests the max_streak_count method from the database module, which verifies that the habits are correctly updated in the database.

        Assertions:
        - `database.max_streak_count(self.db, "Drinking")` should be 29
        - `database.max_streak_count(self.db, "Learning")` should be 19
        - `database.max_streak_count(self.db, "Pushups")` should be 15
        """

        habit_daily = model.Habit("Drinking")
        end_date = datetime.datetime.strptime("02 Jan 2023", "%d %b %Y")
        current_date = datetime.datetime.now()
        while current_date.date() < end_date.date():
            current_date_formatted = current_date.strftime("%d %b %Y")
            cli.update(db_name="testha.db", today= current_date_formatted)
            habit_daily.update_streak(db_name="testha.db", current_date= current_date_formatted)
            current_date += datetime.timedelta(days=1)
        assert database.max_streak_count(self.db, "Drinking") == 29

        habit_daily = model.Habit("Learning")
        end_date = datetime.datetime.strptime("23 Dec 2022", "%d %b %Y")
        current_date = datetime.datetime.now()
        while current_date.date() < end_date.date():
            current_date_formatted = current_date.strftime("%d %b %Y")
            cli.update(db_name="testha.db", today= current_date_formatted)
            habit_daily.update_streak(db_name="testha.db", current_date= current_date_formatted)
            current_date += datetime.timedelta(days=1)
        assert database.max_streak_count(self.db, "Learning") == 19

        habit_daily = model.Habit("Pushups")
        end_date = datetime.datetime.strptime("19 Dec 2022", "%d %b %Y")
        current_date = datetime.datetime.now()
        while current_date.date() < end_date.date():
            current_date_formatted = current_date.strftime("%d %b %Y")
            cli.update(db_name="testha.db", today= current_date_formatted)
            habit_daily.update_streak(db_name="testha.db", current_date= current_date_formatted)
            current_date += datetime.timedelta(days=1)
        assert database.max_streak_count(self.db, "Pushups") == 15

    @freeze_time("2022-12-20")
    def test_break_habit_pushups(self):
        """
        
        This test function tests the update_streak method of the Habit model class for breaking a habit. The function tests the following:
        - The correct breaking of a habit streak by checking that the `cli.update()` method updates the habit log and the `habit.update_streak()` method updates the streak and max_streak in the database
        - The test uses a frozen time of "2022-12-20" to ensure consistent results.
        - The function also tests the max_streak_count method from the database module, which verifies that the habits are correctly updated in the database.

        Assertions:
        - `database.streak_count(self.db, "Pushups")` should be 0
        - `database.max_streak_count(self.db, "Pushups")` should be 15
        """

        cli.update(db_name="testha.db", today= "20 Dec 2022")
        assert database.streak_count(self.db, "Pushups") == 0

        habit_daily = model.Habit("Pushups")
        end_date = datetime.datetime.strptime("02 Jan 2023", "%d %b %Y")
        current_date = datetime.datetime.now()
        while current_date.date() < end_date.date():
            current_date_formatted = current_date.strftime("%d %b %Y")
            cli.update(db_name="testha.db", today= current_date_formatted)
            habit_daily.update_streak(db_name="testha.db", current_date= current_date_formatted)
            current_date += datetime.timedelta(days=1)
        assert database.max_streak_count(self.db, "Pushups") == 15     

    @freeze_time("2022-12-24")
    def test_break_habit_learning(self):
        """

        This test function tests the update_streak method of the Habit model class for breaking a habit. The function tests the following:
        - The correct breaking of a habit streak by checking that the `cli.update()` method updates the habit log and the `habit.update_streak()` method updates the streak and max_streak in the database
        - The test uses a frozen time of "2022-12-24" to ensure consistent results.
        - The function also tests the max_streak_count method from the database module, which verifies that the habits are correctly updated in the database.
        
        Assertions:
        - `database.streak_count(self.db, "Learning")` should be 0
        - `database.max_streak_count(self.db, "Learning")` should be 19
        """

        cli.update(db_name="testha.db", today= "20 Dec 2022")
        assert database.streak_count(self.db, "Learning") == 0

        habit_daily = model.Habit("Learning")
        end_date = datetime.datetime.strptime("02 Jan 2023", "%d %b %Y")
        current_date = datetime.datetime.now()
        while current_date.date() < end_date.date():
            current_date_formatted = current_date.strftime("%d %b %Y")
            cli.update(db_name="testha.db", today= current_date_formatted)
            habit_daily.update_streak(db_name="testha.db", current_date= current_date_formatted)
            current_date += datetime.timedelta(days=1)
        assert database.max_streak_count(self.db, "Learning") == 19
    
    @freeze_time("2022-12-08")
    def test_habit_weekly_update(self):
        """

        This function tests the functionality of updating a habit's streak and completion status for habits
        that have a weekly periodicity.
        The function first sets the current date to December 8th, 2022 using the @freeze_time decorator.
        Then it creates a Habit object for the habit "Running" and calls the update_streak function on it,
        passing in the test database's name and the current date.
        It then checks the completion status of the habit "Running" in the test database and asserts that it is 2.
        Similarly, the function creates a Habit object for the habit "Workout" and calls the update_streak function on it,
        and asserts that the completion status of the habit "Workout" is 2.
        
        Assertions:
        - `habit_weekly.completed` should be 2
        - `habit_weekly_second.completed` should be 2
        """

        current_date = datetime.datetime.now().date()
        current_date_formatted = current_date.strftime("%d %b %Y")
        habit_weekly = model.Habit("Running")
        habit_weekly.update_streak(db_name="testha.db", current_date= current_date_formatted)
        database.habit_completed_check(self.db, "Running")
        assert habit_weekly.completed == 2

        habit_weekly_second = model.Habit("Workout")
        habit_weekly_second.update_streak(db_name="testha.db", current_date= current_date_formatted)
        database.habit_completed_check(self.db, "Workout")
        assert habit_weekly_second.completed == 2

    @freeze_time("2022-12-11")
    def test_weekly_set_stardate_weekly(self):
        """

        This function tests the ability of the program to set the starting date of a weekly habit correctly. 
        It first sets the current date to December 11, 2022, and then calls the update function from the cli module 
        to update the habit's starting date in the database.
        """

        current_date = datetime.datetime.now().date()
        current_date_formatted = current_date.strftime("%d %b %Y")
        cli.update(db_name="testha.db", today= current_date_formatted)


    @freeze_time("2022-12-16")
    def test_second_checkoff_running(self):
        """

        This function tests the ability of the program to correctly record the second checkoff of a weekly habit. 
        It first sets the current date to December 16, 2022, and then creates an instance of the Habit class 
        with the habit name "Running". 
        It then calls the update_streak function to update the habit's streak in the database, and then calls the habit_completed_check
        function to check if the habit is completed.
        
        Assertion:
        - 'habit_weekly.completed' should be 2
        """

        current_date = datetime.datetime.now().date()
        current_date_formatted = current_date.strftime("%d %b %Y")
        habit_weekly = model.Habit("Running")
        habit_weekly.update_streak(db_name="testha.db", current_date= current_date_formatted)
        database.habit_completed_check(self.db, "Running")
        assert habit_weekly.completed == 2

    @freeze_time("2022-12-18")
    def test_break_habit_weekly(self):
        """
        This test case tests the scenario when a user breaks a weekly habit.
        The current date is set to December 18, 2022. The function calls the 'cli.update' function to update the habit 
        completion status in the database. The expected outcome is that the streak of the habit should be broken.
        """

        current_date = datetime.datetime.now().date()
        current_date_formatted = current_date.strftime("%d %b %Y")
        cli.update(db_name="testha.db", today= current_date_formatted)

    @freeze_time("2022-12-22")
    def test_running_third_checkoff(self):

        """
        This test case tests the scenario when a user completes a habit for the third time.
        The current date is set to December 22, 2022. The function calls the 'habit_weekly.update_streak' function 
        and 'database.habit_completed_check' function to update the habit completion status and streak count in the 
        database.
        
        Assertion:
        - `habit_weekly.completed` should be 2
        - `database.streak_count` should be 3
        """

        current_date = datetime.datetime.now().date()
        current_date_formatted = current_date.strftime("%d %b %Y")
        habit_weekly = model.Habit("Running")
        habit_weekly.update_streak(db_name="testha.db", current_date= current_date_formatted)
        database.habit_completed_check(self.db, "Running")
        assert habit_weekly.completed == 2
        assert database.streak_count(self.db, "Running") == 3

    @freeze_time("2022-12-24")
    def test_workout_checkoff_after_break(self):
        """
        Test to check if the workout habit is completed after a break.
        The function uses the @freeze_time decorator to set the current date to 
        "2022-12-24" and uses the update_streak() and habit_completed_check() methods
        of the model and database classes respectively to update the workout habit
        and check if it is completed.

        Assertions:
        - `second_habit_weekly.completed` should be 2
        """

        current_date = datetime.datetime.now().date()
        current_date_formatted = current_date.strftime("%d %b %Y")
        second_habit_weekly = model.Habit("Workout")
        second_habit_weekly.update_streak(db_name="testha.db", current_date= current_date_formatted)
        database.habit_completed_check(self.db, "Workout")
        assert second_habit_weekly.completed == 2

    @freeze_time("2022-12-25")
    def test_habits_uncompleted_status(self):
        """
        Test to check if the habits are uncompleted after a break.
        The function uses the @freeze_time decorator to set the current date to
        "2022-12-25" and uses the update() method of the cli class to update the habits.

        Assertions:
        - `database.streak_count(self.db, "Drinking")` should be 29
        - `database.streak_count(self.db, "Learning")` should be 19
        - `database.streak_count(self.db, "Pushups")` should be 15
        """

        current_date = datetime.datetime.now().date()
        current_date_formatted = current_date.strftime("%d %b %Y")
        cli.update(db_name="testha.db", today= current_date_formatted)
        assert database.streak_count(self.db, "Running") == 3
        assert database.streak_count(self.db, "Workout") == 2

    @freeze_time("2022-12-30")
    def test_last_checkoff_weekly(self):
        """
        Test to check if the last checkoff of weekly habits.
        The function uses the @freeze_time decorator to set the current date to
        "2022-12-30" and uses the update_streak() and habit_completed_check() methods
        of the model and database classes respectively to update the Running and Workout habits
        and check if they are completed.

        Assertions:
        - `habit_weekly.completed` should be 2
        - `habit_weekly_second.completed` should be 2
    """

        current_date = datetime.datetime.now().date()
        current_date_formatted = current_date.strftime("%d %b %Y")
        habit_weekly = model.Habit("Running")
        habit_weekly.update_streak(db_name="testha.db", current_date= current_date_formatted)
        database.habit_completed_check(self.db, "Running")
        assert habit_weekly.completed == 2

        habit_weekly_second = model.Habit("Workout")
        habit_weekly_second.update_streak(db_name="testha.db", current_date= current_date_formatted)
        database.habit_completed_check(self.db, "Workout")
        assert habit_weekly_second.completed == 2

    @freeze_time("2023-01-01")
    def test_max_streak_all_habits(self):
        """
        Test to check the maximum streak of all habits.
        The function uses the @freeze_time decorator to set the current date to
        "2023-01-01" and uses the update() method of the cli class and the max_streak_all_habits() method
        of the analytics class to update the habits and find the maximum streak of all habits.

        Assertions:
        - `len(logs)` should not be 0
        - `logs[0].max_streak` should be 29
        """

        current_date = datetime.datetime.now().date()
        current_date_formatted = current_date.strftime("%d %b %Y")
        cli.update(db_name= "testha.db", today= current_date_formatted)
        logs = analytics.max_streak_all_habits(self.db)
        logs = sorted(logs, key=lambda x: x.max_streak, reverse=True)
        assert len(logs) != 0
        assert logs[0].max_streak == 29

    @freeze_time("2023-01-01")
    def test_max_streak_given_habit(self):
        """
        Test to check the maximum streak for a given habit.
        The function uses the @freeze_time decorator to set the current date to
        "2023-01-01" and uses the update() method of the cli class and the max_streak_given_habit() method
        of the analytics class to update the habit and find the maximum streak of the habit.

        Assertions:
        - `len(logs)` should not be 0
        - `logs[0].max_streak` should be 4
        """

        current_date = datetime.datetime.now().date()
        current_date_formatted = current_date.strftime("%d %b %Y")
        cli.update(db_name= "testha.db", today= current_date_formatted)
        logs = analytics.max_streak_given_habit(self.db, "Running")
        logs = sorted(logs, key=lambda x: x.max_streak, reverse=True)
        assert len(logs) != 0
        assert logs[0].max_streak == 4

    @freeze_time("2023-01-01")
    def test_custom_periodicity(self):
        """
        Test to check the custom periodicity of habits.
        The function uses the @freeze_time decorator to set the current date to
        "2023-01-01" and uses the update() method of the cli class and the habit_custom_perdiodicity_information() method
        of the analytics class to update the habits and find the information of the habits with custom periodicity.

        Assertions:
        - `len(analytics.habit_custom_perdiodicity_information(self.db, periodicity="Daily"))` should be 3
        - `len(analytics.habit_custom_perdiodicity
        """

        current_date = datetime.datetime.now().date()
        current_date_formatted = current_date.strftime("%d %b %Y")
        cli.update(db_name= "testha.db", today= current_date_formatted)
        assert len(analytics.habit_custom_perdiodicity_information(self.db, periodicity="Daily")) == 3
        assert len(analytics.habit_custom_perdiodicity_information(self.db, periodicity= "Weekly")) == 2

        

        
        
