
from typing import Optional

from habittracker import __app_name__, __version__, database, model, get, analytics

import questionary

import datetime

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer()

console = Console()

qt = questionary


def version_callback(value: bool) -> None:
    """
    Displays the name and the version of the application. Afterwards it raises a typer.Exit exception to exit the application cleanly.

    Args:
        value (bool): A flag indicating whether the version should be displayed.

    Returns:
        None

    """
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


"""
main - callback function for the application

This function is a callback function for the application and is executed when the application is run. It takes in one optional parameter:

version (bool, Optional): A flag to indicate whether to show the application's version and exit. Default is None. If provided, the version_callback function will be executed.

Returns:
None
"""
@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=version_callback,
        is_eager=True
    )
) -> None:
    return


    

@app.command(short_help="Start your very own habittracker")
def start():
    """
    Start the habittracker app.

    Args:
        None

    Returns:
        None

    Raises:
        None

    """
    start_function()


### Additional functions to support the running programm after starting app !!

habit_name = get.habit_entry
description_name = get.habit_description
periodicity_name = get.habit_periodicity
operating_habit = get.habits_of_database
managing_habit = get.uncompleted_habits
get_periodicity_name = get.analyze_habit_periodicity


def exit_or_start_question():
    """
    Prompts the user to confirm if they want to exit the application or go back to the start.
    If the user chooses to go back to the start, the start_without_update() function is called.
    If the user chooses to exit, the application is closed.

    Args:
        None
    
    Returns:
        None
        
    Raises:
        typer.Exit: If the user chooses to exit the application.
    """
    typer.secho("\n You're about to leave the application !\n",
    fg=typer.colors.BRIGHT_YELLOW)
    confirming_quit_question = qt.confirm("Are you sure you want to Exit ?").ask()
    if confirming_quit_question:
        typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET ABOUT YOUR HABITS !\n",
        fg = typer.colors.BRIGHT_CYAN)
        raise typer.Exit()
    else:
        second_try_start = qt.select("Do you want to go back to start or exit ?",
        choices=["Go to Start", "Exit"],
        ).ask()
        if second_try_start == "Go to Start":
            start_without_update()
        else:
            typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET ABOUT YOUR HABITS !\n",
            fg = typer.colors.BRIGHT_CYAN)
            raise typer.Exit()


def for_start_add_function():
    """
    Prompts the user to add their first habit to the tracker.
    Asks the user for the habit name, description, and periodicity.
    If the user confirms their entry, the habit is added to the tracker and the user is shown the starting page.
    If the user does not confirm their entry, they are given the option to try again or go back to the starting page.

    Args:
        None
    
    Returns:
        None
        
    Raises:
        typer.Exit: If the user chooses to exit the application.
    """
    typer.secho("\nGOOD DECISION !!!\n\nIt's time to add your first habit to your tracker !\n",
    fg=typer.colors.BRIGHT_GREEN)
    starting_is_on = True
    while starting_is_on:
        habit_entry = habit_name()
        description_entry = description_name()
        periodicity_entry = periodicity_name()
        adding_entry = model.Habit(habit_entry, description_entry, periodicity_entry)
        if get.adding_confirmation(habit_entry, description_entry, periodicity_entry):
            model.Habit.add_habit(adding_entry, db_name="habit.db")
            show(None)
            typer.secho(f"\nCONGRATULATIONS !!!\n",
            fg=typer.colors.BRIGHT_GREEN)
            console.print(f"You just added your first habit '{habit_entry}' with the description '{description_entry}' as '{periodicity_entry}' to your tracker!!\n")
            typer.secho("With your first habit added to your Habittracker, there are more functions waiting for you at the starting page !\n",fg=typer.colors.BRIGHT_YELLOW)
            redirecting_question = qt.select("Do you want to be redirected to the starting page or exit ?",
            choices=["Starting Page", "Exit"],
            ).ask()
            if redirecting_question == "Starting Page":
                starting_is_on = False
                start_without_update()
            else:
                starting_is_on = False
                exit_or_start_question()

        else:
            continue_start_question = qt.confirm("Did you make a mistake and want to change your entry ?").ask()
            if continue_start_question:
                continue
            else:
                starting_is_on = False
                exit_or_start_question()


def delete_function():
    """
    Prompts the user to delete a habit from the tracker.
    Asks the user to confirm the delete operation.
    If the user confirms, the habit is deleted from the tracker.
    If the tracker is empty after the delete operation, the user is shown the starting page.

    Args:
        None

    Returns:
        None
        
    Raises:
        ValueError: If there are no habits in the tracker.
        Start: If there is no habit inside the application.
    """
    start_delete_question = qt.confirm("Do you want to delete a habit ?")
    if start_delete_question:
        deleting_is_on = True
        try:
            db = database.connect_db()
        except Exception as e:
            typer.secho(f"\nError: Could not connect to the database. {e}\n",
            fg=typer.colors.BRIGHT_RED)
            return
        while deleting_is_on:
            deleting_habit_name= operating_habit()
            if database.habit_existing_check(db, deleting_habit_name) is True:
                if get.delete_confirmation(deleting_habit_name):
                    deleting_entry = model.Habit(deleting_habit_name)
                    model.Habit.delete_habit(deleting_entry, db_name="habit.db")
                    database.reset_log(db, deleting_habit_name)
                    if len(database.all_habits(db)) > 0:
                        show(None)
                        console.print(f"\nThe habit '{deleting_habit_name}' is deleted!\n")
                                
                        continue_deleting_question = qt.confirm("Do you want to delete more habits?").ask()
                        if continue_deleting_question is True:
                            continue
                        else:
                            deleting_is_on = False
                            continue_editing_question()
                                            
                    else:
                        deleting_is_on = False
                        console.print(f"\nThe habit '{deleting_habit_name}' is deleted!\n")
                        typer.secho("There are no more habits in your database that could be seen in your overview !\n",
                        fg=typer.colors.BRIGHT_RED)
                        exit_question = qt.confirm("Do you want to go back to start?").ask()
                        if exit_question:
                            start_function()
                        else:
                            exit_or_start_question()
                else:
                    console.print(f"\nThe habit '{deleting_habit_name}' wont be deleted!\n")
                    continue_deleting_question = qt.confirm("Do you want to delete more habits?").ask()
                    if continue_deleting_question is True:
                        continue
                    else:
                        deleting_is_on = False
                        continue_editing_question()

            else:
                typer.secho(f"\nThe habit '{deleting_habit_name}' is not existing ! Please try again !\n", fg=typer.colors.BRIGHT_RED)
                continue_editing_question()
    else:
        continue_editing_question()


def continue_editing_question():
    """
    Prompts the user to choose whether to continue editting habits, go to the starting page, or exit the application.

    Args:
        None

    Returns:
        None
        
    Raises:
        typer.Exit: If the user chooses to exit the application.

    """
    continue_editing_question = qt.select("Do you want to continue editing or exit?",
    choices=["Continue editing", "Go to Start", "Exit"],
    ).ask()
    if continue_editing_question == "Continue editing":
        edit()
    elif continue_editing_question == "Go to Start":
        start_without_update()
    else:
        exit_app_question()


def add_function():
    """
    Add a habit to the tracker.
    
    Prompts the user to confirm if they want to add a habit, and if so, 
    prompts for the habit name, description, and periodicity. If the habit does
    not already exist in the database, it is added and the user is shown a 
    confirmation message. If the habit already exists, the user is prompted to 
    try again or stop adding habits. If the user does not want to add a habit, 
    the function continues_edditing_question() is called.

    Args:
        None

    Returns:
        None
    
    Raises:
        ValueError: If there are no habits in the database.

    """
    start_add_question = qt.confirm("Do you want to add a habit?").ask()
    if start_add_question:
        adding_is_on = True
        try:
            db = database.connect_db()
        except Exception as e:
            typer.secho(f"\nError: Could not connect to the database. {e}\n",
            fg=typer.colors.BRIGHT_RED)
            return
        while adding_is_on:
            try:
                habit_entry_name = habit_name()
                if database.habit_existing_check(db, habit_entry_name) is False:
                    description_entry = description_name()
                    periodicity_entry = periodicity_name()
                    if get.adding_confirmation(habit_entry_name, description_entry, periodicity_entry):
                        adding_entry = model.Habit(habit_entry_name, description_entry, periodicity_entry)
                        model.Habit.add_habit(adding_entry, db_name="habit.db")
                        show(None)
                        console.print(f"\nYou added the habit '{habit_entry_name}' with the description '{description_entry}' as '{periodicity_entry}' to your tracker!!\n")
                        continue_adding_question = qt.confirm("Do you want to add more habits?").ask()
                        if continue_adding_question:
                            continue
                        else:
                            adding_is_on = False
                            continue_editing_question()
                    else:
                        typer.secho(f"\nThe habit '{habit_entry_name}' was NOT added to your tracker !\n", fg=typer.colors.BRIGHT_RED)
                        adding_is_on = False
                        try_again_question = qt.confirm("Do you want to try again ?").ask()
                        if try_again_question:
                            add_function()
                        else:
                            continue_editing_question()
                else:
                    typer.secho(f"\nThe habit '{habit_entry_name}' already exists! Please try another one!\n", fg=typer.colors.BRIGHT_RED)
                    continue_adding_second_question = qt.confirm("Do you want to add another habit?").ask()
                    if continue_adding_second_question is True:
                        continue
                    else:
                        adding_is_on = False
                        continue_editing_question()

            except ValueError:
                typer.secho(f"\nThere is no habit in your database ! Please add one first!\n", fg=typer.colors.BRIGHT_RED)
                raise start()

    else:
        continue_editing_question()


def start_without_update():
    """
    Start the habit tracker without updating the progress of existing habits.
    
    Calls the function show(None) to display the current progress of all habits
    in the tracker. Prints a message to the console to encourage the user to work
    on their habits. Calls the function ask_for_intention_no_start() to prompt
    the user for their intentions for using the habit tracker.

    Args:
        None
    
    Returns:
        None

    """
    try:
        show(None)
        typer.secho("\nTIME TO WORK ON YOUR HABITS !!!\n",fg=typer.colors.BRIGHT_YELLOW)
        ask_for_intention_no_start()
    except ValueError:
        typer.secho("\nThere are no habits in your database ! Please add one first !",
        fg = typer.colors.BRIGHT_RED)
        raise typer.Exit()

def manage_for_update():
    checking_is_on = True
    try:
        db = database.connect_db()
    except Exception as e:
        typer.secho(f"\nError: Could not connect to the database. '{e}'\n",
        fg=typer.colors.BRIGHT_RED)
        return
        
    while checking_is_on:             
        check_off_habit = managing_habit()
        try:
            if database.periodicity_of_habit(db,check_off_habit) == "Daily":
                habit_daily = model.Habit(check_off_habit)
                if get.check_off_confirmation(check_off_habit):
                    today = datetime.datetime.now().date()
                    today_formatted = today.strftime("%d %b %Y")
                    habit_daily.update_streak(db_name="habit.db", current_date= today_formatted)
                    show(None)
                    typer.secho(f"\nCONGRATULATIONS !!!\n",
                    fg=typer.colors.BRIGHT_GREEN)
                    console.print(f"You completed the habit '{check_off_habit}' today ! Keep it going!\n")
                else:
                    console.print(f"\nYou did not set the habit '{check_off_habit}' to completed !\n")
                check_off_continue_question = qt.confirm("Do you want to check off more habits ?").ask()
                if check_off_continue_question is True:
                    if database.collect_uncompleted_habits_choices(db) is not None:
                        continue
                    else:
                        checking_is_on = False
                        typer.secho("\nThere are no uncompleted habits in your database !\n",
                        fg=typer.colors.BRIGHT_RED)
                        ask_for_intention()

                else:
                    checking_is_on = False
                    start_without_update()

            elif database.periodicity_of_habit(db,check_off_habit) == "Weekly":
                habit_weekly = model.Habit(check_off_habit)
                if get.check_off_confirmation(check_off_habit):
                    database.complete_habit(db,check_off_habit)
                    habit_weekly.update_streak(db_name="habit.db", current_date= today_formatted)
                    show(None)
                    typer.secho(f"\nCONGRATULATIONS !!!",
                    fg=typer.colors.BRIGHT_GREEN)
                    console.print(f"\nYou completed the habit '{check_off_habit}' this week ! Keep it going!\n")
                else:
                    console.print(f"\nYou did not set the habit '{check_off_habit}' to completed !\n")
                check_off_continue_question = qt.confirm("Do you want to check off more habits ?").ask()
                if check_off_continue_question is True:
                    continue
                else:
                    checking_is_on = False
                    start_without_update()
        except ValueError:
            typer.secho("\nThere is no habit with the periodicity you choosed ! Please add one first !\n",
            fg = typer.colors.BRIGHT_RED)




def manage_function():
    """
    Manage the progress of habits in the tracker.
    
    Connects to the database and prompts the user to select a habit to mark as
    completed. If the selected habit has a periodicity of "Daily", the function
    checks if the habit has already been completed today and updates the streak
    accordingly. If the selected habit has a periodicity of "Weekly", the function
    checks if the habit has already been completed this week and updates the
    streak accordingly. After the user has marked a habit as completed, they are
    prompted to continue managing or exit the function.

    Args:
        None
    
    Returns:
        None

    Raises:
        NameError: If the `db` or `Database` variables are not defined.
        AttributeError: If the `periodicity_of_habit` method does not exist or is not callable.
        TypeError: If the `Database` object is not a valid object with the `periodicity_of_habit` method.
        ValueError: If the `check_off_habit` argument is not a valid value.
    """
    checking_is_on = True
    try:
        db = database.connect_db()
    except Exception as e:
        typer.secho(f"\nError: Could not connect to the database. '{e}'\n",
        fg=typer.colors.BRIGHT_RED)
        return
        
    while checking_is_on:             
        check_off_habit = managing_habit()
        try:
            if database.periodicity_of_habit(db,check_off_habit) == "Daily":
                habit_daily = model.Habit(check_off_habit)
                if get.check_off_confirmation(check_off_habit):
                    today = datetime.datetime.now().date()
                    today_formatted = today.strftime("%d %b %Y")
                    habit_daily.update_streak(db_name="habit.db", current_date= today_formatted)
                    show(None)
                    typer.secho(f"\nCONGRATULATIONS !!!\n",
                    fg=typer.colors.BRIGHT_GREEN)
                    console.print(f"You completed the habit '{check_off_habit}' today ! Keep it going!\n")
                else:
                    console.print(f"\nYou did not set the habit '{check_off_habit}' to completed !\n")
                check_off_continue_question = qt.confirm("Do you want to check off more habits ?").ask()
                if check_off_continue_question is True:
                    if database.collect_uncompleted_habits_choices(db) is not None:
                        continue
                    else:
                        checking_is_on = False
                        typer.secho("\nThere are no uncompleted habits in your database !\n",
                        fg=typer.colors.BRIGHT_RED)
                        ask_for_intention()

                else:
                    checking_is_on = False
                    for_check_off_second_question = qt.select("Do you want to keep on managing or exit?",
                    choices=["Keep managing", "Go to Start", "Exit"],
                    ).ask()
                    if for_check_off_second_question == "Keep managing":
                        manage()
                    elif for_check_off_second_question == "Go to Start":
                        start_without_update()
                    else:
                        exit_app_question()

            elif database.periodicity_of_habit(db,check_off_habit) == "Weekly":
                habit_weekly = model.Habit(check_off_habit)
                if get.check_off_confirmation(check_off_habit):
                    database.complete_habit(db,check_off_habit)
                    habit_weekly.update_streak(db_name="habit.db", current_date= today_formatted)
                    show(None)
                    typer.secho(f"\nCONGRATULATIONS !!!",
                    fg=typer.colors.BRIGHT_GREEN)
                    console.print(f"\nYou completed the habit '{check_off_habit}' this week ! Keep it going!\n")
                else:
                    console.print(f"\nYou did not set the habit '{check_off_habit}' to completed !\n")
                check_off_continue_question = qt.confirm("Do you want to check off more habits ?").ask()
                if check_off_continue_question is True:
                    if database.collect_uncompleted_habits_choices(db) is not None:
                        continue
                    else:
                        checking_is_on = False
                        typer.secho("\nThere are no uncompleted habits in your database !\n",
                        fg=typer.colors.BRIGHT_RED)
                        ask_for_intention()
                else:
                    checking_is_on = False
                    for_check_off_second_question = qt.select("Do you want to keep on managing or exit?",
                    choices=["Keep managing", "Go to Start", "Exit"],
                    ).ask()
                    if for_check_off_second_question == "Keep managing":
                        manage()
                    elif for_check_off_second_question == "Go to Start":
                        start_without_update()
                    else:
                        exit_app_question()
        except ValueError:
            typer.secho("\nThere is no habit with the periodicity you choosed ! Please add one first !\n",
            fg = typer.colors.BRIGHT_RED)



def keep_analyzing():
    """
    Prompt the user to decide whether to keep analyzing or go back to the start.

    The user is presented with a choice of three options: "Keep analyzing", "Go to Start", or "Exit".
    If the user selects "Keep analyzing", the function calls the `analyze` function.
    If the user selects "Go to Start", the function calls the `start_without_update` function.
    If the user selects "Exit", the function calls the `exit_app_question` function.

    Args:
        None
    
    Returns:
        None

    """
    analyze_continue_question = qt.select("Do you want to keep analyzing?",
    choices=["Keep analyzing", "Go to Start", "Exit"],
    ).ask()
    if analyze_continue_question == "Keep analyzing":
        analyze()
    elif analyze_continue_question == "Go to Start":
        start_without_update()
    else:
        exit_app_question()


def ask_for_intention():
    """Prompt the user to choose an action from a list of options.

    The user is presented with a choice of six options: "Editting", "Managing", "Analyzing", "Go to Start", "Show Log", or "Exit".
    If the user selects "Editting", the function calls the `edit` function.
    If the user selects "Managing", the function calls the `manage` function.
    If the user selects "Analyzing", the function calls the `analyze` function.
    If the user selects "Go to Start", the function calls the `start_without_update` function.
    If the user selects "Show Log", the function calls the `log_function` function.
    If the user selects "Exit", the function calls the `exit_app_question` function.

    Args:
        None
    
    Returns:
        None

    """
    what_to_do_question = qt.select("What do you want to do?",
    choices=["Editing", "Managing", "Analyzing", "Go to Start", "Show Log", "Exit"],
    ).ask()
    if what_to_do_question == "Editing":
        edit()
    elif what_to_do_question == "Managing":
        manage()
    elif what_to_do_question == "Analyzing":
        analyze()
    elif what_to_do_question == "Go to Start":
        start_without_update()
    elif what_to_do_question == "Show Log":
        log_function()
    else:
        exit_app_question()


def ask_for_intention_no_start():
    """
    Ask the user what they want to do without going back to start, and call the corresponding function.

    Args:
        None
    
    Returns:
        None

    """
    what_to_do_question = qt.select("What do you want to do?",
    choices=["Editing", "Managing", "Analyzing", "Show Log", "Exit"],
    ).ask()
    if what_to_do_question == "Editing":
        edit()
    elif what_to_do_question == "Managing":
        manage()
    elif what_to_do_question == "Analyzing":
        analyze()
    elif what_to_do_question == "Show Log":
        log_function()
    else:
        exit_app_question()
        

def exit_app_question():
    """Prompt the user to confirm that they want to exit the app.

    The user is presented with a confirmation question asking if they want to exit the app.
    If the user confirms, the function displays a farewell message and exits the app.
    If the user does not confirm, the function presents the user with a list of options and asks them to choose an action.
    The user can choose from the following options: "Editting", "Managing", "Analyzing", "Go to Start", "Show Log", or "Exit".
    If the user selects "Editting", the function calls the `edit` function.
    If the user selects "Managing", the function calls the `manage` function.
    If the user selects "Analyzing", the function calls the `analyze` function.
    If the user selects "Go to Start", the function calls the `start_without_update` function.
    If the user selects "Show Log", the function calls the `log_function` function.
    If the user selects "Exit", the function prompts the user to confirm again.

    Args:
        None
    
    Returns:
        None

    Raises:
        typer.Exit: If the user confirms that they want to exit the app.

    """
    typer.secho("\nYou're about to leave the app !\n",
    fg=typer.colors.BRIGHT_YELLOW)
    exit_question = qt.confirm("Are you sure you want to exit ?").ask()
    if exit_question:
        typer.secho("\nHAVE A NICE DAY ! AND DON'T FORGET YOUR HABITS !\n",
        fg=typer.colors.BRIGHT_CYAN)
        raise typer.Exit()
    else:
        ask_for_intention()


def analyze_habits_same_periodicity():
    """
    Analyze habits with the same periodicity in the database.
    
    This function connects to the database, gets the periodicity name, and displays a summary of the habits with the
    specified periodicity. If no habits with the specified periodicity are found, it prints an appropriate message.
    If there is an error connecting to the database, it prints an appropriate error message.

    Args:
        None

    Returns:
        None

    """
    try:
        db = database.connect_db()
    except Exception as e:
        console.print(f"\nError retrieving habits from database: {e}\n")
        return

    periodicity_analyze_name = get_periodicity_name()
    if len(analytics.habit_custom_perdiodicity_information(db, periodicity_analyze_name)) > 0 :
        if periodicity_analyze_name == "Daily":
            show(periodicity="Daily")
            console.print(f"\nHere is an overview of your habits with the periodicity '{periodicity_analyze_name}' !\n")
            keep_analyzing()

        elif periodicity_analyze_name =="Weekly":
            show(periodicity="Weekly")
            console.print(f"\nHere is an overview of your habits with the periodicity '{periodicity_analyze_name}' !\n")
            keep_analyzing()

        else:
            console.print(f"\nNo matching habits with the periodicity '{periodicity_analyze_name}' found in your database!\n")

    else:
        typer.secho(f"\nThere are no habits with the periodicity '{periodicity_analyze_name}' in your database !\n")
        keep_analyzing()

                
def analyze_all():
    """
    Analyze all habits currently tracked in the database.

    Connects to the database and retrieves information about all habits using the
    `all_habits_information` function from the `analytics` module. If there are
    any habits found, the `show` function is called and the habits are displayed
    to the user. If no habits are found, the `start_without_update` function is
    called. If there is an error connecting to the database, an error message is
    printed to the console.

    Args:
        None
    
    Returns:
        None

    """
    try:
        db = database.connect_db()
    except Exception as e:
        console.print(f"\nError retrieving habits from database: {e}\n")
        return

    habits_analyze_data = analytics.all_habits_information(db)
    if len(habits_analyze_data) > 0:
        show(None)
        typer.secho("\nThese are all habits that are currently tracked for you !\n",
        fg=typer.colors.BRIGHT_GREEN)
        keep_analyzing()
    else:
        start_without_update()


def show_all():
    """
    Displays all habits in the database in a table. If the database is empty, calls start_without_update().
    
    Handles any errors that may occur when connecting to the database.

    Args:
        None
    
    Returns:
        None

    """
    try:
        db = database.connect_db()
    except Exception as e:
        console.print(f"\nError retrieving habits from database: {e}\n")
        return

    if len(database.all_habits(db)) > 0:
        entries_list = database.all_habits(db)
        table = Table(title="\nYOUR HABITTRACKER\n", show_header=True, show_lines=True)
        table.add_column("Habit", min_width=12, justify="center")
        table.add_column("Description", min_width=20, justify="center")
        table.add_column("Periodicity", min_width=12, justify="center")
        table.add_column("Started", min_width=12, justify="center")
        table.add_column("Startdate_Weekly", min_width=12, justify="center")
        table.add_column("Completed", min_width=12, justify="center")
        table.add_column("Streak", min_width=12, justify="center")

        for entry in entries_list:
            is_completed_str = 'Yes' if entry.completed == 2 else 'No'
            weekly_date_str = '-' if entry.startdate_weekly is None else entry.startdate_weekly
            table.add_row(entry.habit, entry.description, entry.periodicity, entry.starting_date, weekly_date_str, is_completed_str, str(entry.streak))
        console.print(table)

    else:
        start_without_update()


def show_daily(periodicity):
    """Displays a table of daily habits.

    Args:
        periodicity (str): The periodicity of the habits to display (e.g. "Daily").

    Returns:
        None

    """
    try:
        db = database.connect_db()
    except Exception as e:
        console.print(f"\nError retrieving habits from database: {e}\n")
        return
    if len(database.all_habits(db)) > 0:
        data_list = analytics.habit_custom_perdiodicity_information(db,periodicity)
        table = Table(title="\nYOUR HABITTRACKER\n", show_header=True, show_lines=True)
        table.add_column("Habit", min_width=12, justify="center")
        table.add_column("Description", min_width=20, justify="center")
        table.add_column("Periodicity", min_width=12, justify="center")
        table.add_column("Started", min_width=12, justify="center")
        table.add_column("Completed", min_width=12, justify="center")
        table.add_column("Streak", min_width=12, justify="center")

        for data in data_list:
            completed_daily_str = 'Yes' if data.completed == 2 else 'No'
            table.add_row(data.habit, data.description, data.periodicity, data.starting_date, completed_daily_str, str(data.streak))
        console.print(table)

    else:
        start_without_update()
       

def show_weekly(periodicity):
    """Displays a table of habits based on their periodicity.

    Args:
        periodicity (str): The periodicity of the habits to display (e.g. "Weekly").

    Returns:
        None

    """
    try:
        db = database.connect_db()
    except Exception as e:
        console.print(f"\nError retrieving habits from database: {e}\n")
        return
    if len(database.all_habits(db)) > 0:
        periodicity_list = analytics.habit_custom_perdiodicity_information(db,periodicity)
        table = Table(title="\nYOUR HABITTRACKER\n", show_header=True, show_lines=True)
        table.add_column("Habit", min_width=12, justify="center")
        table.add_column("Description", min_width=20, justify="center")
        table.add_column("Periodicity", min_width=12, justify="center")
        table.add_column("Started", min_width=12, justify="center")
        table.add_column("Startdate_Weekly", min_width=12, justify="center")
        table.add_column("Completed", min_width=12, justify="center")
        table.add_column("Streak", min_width=12, justify="center")

        for period in periodicity_list:
            completed_weekly_str = 'Yes' if period.completed == 2 else 'No'
            weekly_date_str = '-' if period.startdate_weekly is None else period.startdate_weekly
            table.add_row(period.habit, period.description, period.periodicity, period.starting_date, weekly_date_str, completed_weekly_str, str(period.streak))
        console.print(table)

    else:
        start_without_update()


def check_completed_habits():
    """Checks if any habits are marked as completed.

    Args:
        None

    Returns:
        bool: True if at least one habit is marked as completed, False otherwise.

    """
    db = database.connect_db()
    habits = database.all_habits(db)
    # Loop through the habits and check if any are completed
    for habit in habits:
        if habit.completed == 1:
            return True
    return False


def start_function():
    """Starts the habit tracker by showing the user their habits and allowing them to manage their habits.

    If the habit tracker is empty, the user is given the option to add a habit. If there are any habits that are marked as
    not completed, the user is given the option to check them off. Otherwise, the user is asked for their intention.

    Args:
        None
    
    Returns:
        None

    """
    db = database.connect_db()
    habits = database.all_habits(db)
    if len(habits) == 0:
        handle_empty_habit_tracker()
    elif len(habits) > 0:
        handle_existing_habits()


def handle_empty_habit_tracker():
    """
    Handles the case when the habit tracker is empty. It displays a message to the user
    welcoming them to the habit tracker and asking them if they want to add a habit. 
    If the user confirms, the function `for_start_add_function` is called. If not, the
    `exit_or_start_question` function is called.

    Args:
        None

    Returns:
        None
    """
    typer.secho("\nWELCOME !!! TIME TO WORK ON YOUR HABITS !!!",fg=typer.colors.BRIGHT_YELLOW)
    typer.secho("\nRight now your habittracker is empty,\n", fg=typer.colors.BRIGHT_RED)
    start_question = qt.confirm("Do you want to add a habit to your tracker ?").ask()
    if start_question:
        for_start_add_function()
    else:
        exit_or_start_question()

def handle_existing_habits():
    """
    Handles the case when the habit tracker is not empty. It updates the habits, displays them to the user,
    displays a message welcoming the user to the updated habit tracker, and checks if there are any habits
    that have not been completed. If there are, the user is asked if they want to check them off. If not, the
    `ask_for_intention_no_start` function is called.

    Args:
        None
    
    Returns:
        None
    """
    update()
    show(None)
    typer.secho("\nWELCOME to your updated habittracker !!\n",
    fg=typer.colors.BRIGHT_YELLOW)
    typer.secho("See the messages above the table ! Don't loose your streaks and check off in time !!\n",fg=typer.colors.BRIGHT_WHITE)
    if check_completed_habits():
        typer.secho("There are habits that are not completed !\n", fg=typer.colors.BRIGHT_YELLOW)
        check_off_question = qt.confirm("Do you want to check off habits ?").ask()
        if check_off_question:
            manage_for_update()
        else:
            show(None)
            ask_for_intention_no_start()
    else:
        ask_for_intention_no_start()
        

def log_function():
    """
    Displays a table of habits and their log information, and allows the user to choose how to continue.

    Args:
        None

    Returns:
        None

    """
    db = database.connect_db()
    if len(database.all_log(db)) != 0:
        results = database.all_log(db)
        table = Table(title = "\nHABITLOG\n", show_header=True, show_lines=True)
        table.add_column("Habit", min_width=12, justify="center")
        table.add_column("Completed", min_width=12, justify="center")
        table.add_column("Streak", min_width=12, justify="center")
        table.add_column("Last_Completed_Date", min_width=12, justify="center")
        table.add_column("Max_Streak", min_width=12, justify="center")
        
        for result in results:
            completed_str = 'Yes' if result.completed == 2 else 'No'
            table.add_row(result.habit, completed_str, str(result.streak),result.datetime_completed, str(result.max_streak))
        console.print(table)
        
        typer.secho("\nThis is your habitlog overview !\n",
        fg=typer.colors.BRIGHT_GREEN)

        log_question = qt.select("How do you want to continue ?",
        choices=["Editting", "Managing", "Analyzing", "Go to Start", "Exit"],
        ).ask()
        if log_question == "Editting":
            edit()
        elif log_question == "Managing":
            manage()
        elif log_question == "Analyzing":
            analyze()
        elif log_question == "Go to Start":
            start_without_update()
        else:
            exit_app_question()
    else:
        start_without_update()


def update_check_daily(db_name = None, today = None):
    """
    Check the habits that have a periodicity of "Daily" and update the list of habits that need to be completed today.

    Args:
        None
    
    Returns:
    - results (list): A list of tuples, where each tuple contains an integer and a string.
        The integer represents the number of days since the habit was last completed,
        and the string represents the name of the habit.

    """
    try:
        db = database.connect_db(db_name)
    except Exception as e:
        console.print(f"\nError retrieving habits from database: {e}\n")
        return
    habits_to_check = database.certain_periodicity(db, periodicity="Daily")
    results = []
    if habits_to_check is not None:
        if today is None:
            today = datetime.datetime.now().date()
        else:
            today = datetime.datetime.strptime(today, "%d %b %Y").date()

        for habit in habits_to_check:
            if habit.datetime_completed is not None:
                last_completion = datetime.datetime.strptime(database.habit_completed_time(db, habit.habit), "%d %b %Y").date()
                if today - last_completion == datetime.timedelta(days=0):
                    results.append((1, habit.habit))
                elif today - last_completion == datetime.timedelta(days=1):
                    results.append((2,habit.habit))
                elif today - last_completion >= datetime.timedelta(days=2):
                    results.append((3,habit.habit))
            else:
                results.append((0,habit.habit))
        return results
    else:
        pass

def update_check_weekly(db_name = None, today=None):
    """
    Check the habits that have a periodicity of "Weekly" and update the list of habits that need to be completed this week.

    Args:
        None
    
    Returns:
    - results (list): A list of tuples, where each tuple contains an integer and a string.
        The integer represents the completion status of the habit for the current week,
        and the string represents the name of the habit.

    """
    try:
        db = database.connect_db(db_name)
    except Exception as e:
        console.print(f"\nError retrieving habits from database: {e}\n")
        return
    habits = database.certain_periodicity(db, periodicity="Weekly")
    results = []
    if habits is not None:
        if today is None:
            today = datetime.datetime.now().date()
        else:
            today = datetime.datetime.strptime(today, "%d %b %Y").date()
        for habit in habits:
            starting_date_str = datetime.datetime.strptime(habit.starting_date, "%d %b %Y").date()
            starting_week_end = starting_date_str + datetime.timedelta(days=6)
            if habit.datetime_completed is None:
                if today <= starting_week_end:
                    results.append((0,habit.habit))
                else:
                    results.append((3, habit.habit))
            else:
                new_startdate_week = database.get_startdate_weekly(db, habit.habit)
                startdate = database.get_starting_date(db, habit.habit)
                if new_startdate_week == startdate:
                    if today <= starting_week_end:
                        results.append((1, habit.habit))
                    elif today == (starting_week_end + datetime.timedelta(days=1)):
                        results.append((2, habit.habit))
                    elif today >= (starting_week_end + datetime.timedelta(days=2)):
                        results.append((3, habit.habit))
                else:
                    startdate_weekly_str = datetime.datetime.strptime(database.get_startdate_weekly(db, habit.habit), "%d %b %Y").date()
                    startdate_week_end = startdate_weekly_str + datetime.timedelta(days=6)
                    last_completion = datetime.datetime.strptime(database.habit_completed_time(db, habit.habit), "%d %b %Y").date()
                    if today <= startdate_week_end and last_completion < startdate_weekly_str:
                        results.append((0, habit.habit))
                    elif today <= startdate_week_end and last_completion >= startdate_weekly_str :
                        results.append((1, habit.habit))
                    elif today == startdate_week_end + datetime.timedelta(days=1) and last_completion > startdate_weekly_str:
                        results.append((2, habit.habit))
                    elif today >= startdate_week_end + datetime.timedelta(days=1) and last_completion < startdate_weekly_str:
                        results.append((3, habit.habit))
                    
        return results

    else:
        pass

def update_check_daily_results(db_name = None):
    results = update_check_daily(db_name)
    for result, habit in results:
        habit = model.Habit(habit)
        if result == 1:
            console.print(f"\nThe habit '{habit.habit}' is checked off !\n")
        elif result == 2:
            model.Habit.set_habit_uncomplete(habit, db_name)
        elif result == 3:
            console.print(f"\nOhnoo...The habit '{habit.habit}' was not checked off in time ! Your streak will be reseted !\n")
            model.Habit.reset_streak(habit, db_name)
            model.Habit.set_habit_uncomplete(habit, db_name)
        else:
            console.print(f"\nThe habit '{habit.habit}' has not been checked off yet !\n")
                 

def update_check_weekly_results(db_name = None):
    """
    Updates the completion status and streaks for habits with a "Daily" or "Weekly" periodicity.
    
    Prints messages indicating the status of each habit. Additionally the habit will be set to uncompleted, or will be reseted according to the result.

    Args:
        None
    
    Returns:
        None

    """
    results = update_check_weekly(db_name)
    for result, habit in results:
        habit = model.Habit(habit)
        if result == 1:
            console.print(f"\nThe habit '{habit.habit}' is checked off !\n")
        elif result == 2:
            model.Habit.set_habit_uncomplete(habit, db_name)
            model.Habit.set_new_startdate_weekly(habit, db_name)
        elif result == 3:
            console.print(f"\nOhnoo...The habit '{habit.habit}' was not checked off in time ! Your streak will be reseted !\n")
            model.Habit.reset_streak(habit, db_name)
            model.Habit.set_habit_uncomplete(habit, db_name)
            model.Habit.set_new_startdate_weekly(habit, db_name)
        else:
            console.print(f"\nThe habit '{habit.habit}' has not been checked off yet !\n")


def analyze_longest_streak_all_habits():
    """
    Analyze the longest streak for all habits.
    
    This function retrieves all habits from the database and displays a table with the maximum
    streak for each habit. It also prints the row with the highest maximum streak. If there are no
    habits in the database, it displays an error message and raises the `start` function.

    Args:
        None
    
    Returns:
        None
    
    Raises:
        Exception: If there is an error retrieving habits from the database.
        start: If there are no habits in the database.

    """
    try:
        db = database.connect_db()
    except Exception as e:
        console.print(f"\nError retrieving habits from database: {e}\n")
        return

    if len(analytics.all_habits_log(db)) != 0:
        results = analytics.all_habits_log(db)
        results = sorted(results, key=lambda x: x.max_streak, reverse=True)
        row_with_highest_max_streak = results[0]

        datas = analytics.max_streak_all_habits(db)
        table = Table(title = "\nHABITLOG\n", show_header=True, show_lines=True)
        table.add_column("Habit", min_width=12, justify="center")
        table.add_column("Max_Streak", min_width=12, justify="center")

        for data in datas:
            table.add_row(data.habit, str(data.max_streak))
        console.print(table)
        console.print("\nRow with the highest max_streak:",row_with_highest_max_streak, "\n")
        keep_analyzing()
        
    else:
        typer.secho("\nThere are no habits in your database !! Please add one first !!\n",
        fg=typer.colors.BRIGHT_RED)
        raise start()


def analyze_streak_given_habit():
    """
    Analyze the maximum streak for a given habit.

    Args:
        None

    Returns:
        None

    Raises:
        IndexError: If there are no records for the given habit.
    """
    try:
        db = database.connect_db()
        given_habit = operating_habit()
        results = analytics.max_streak_given_habit(db, given_habit)
        results = sorted(results, key=lambda x: x.max_streak, reverse=True)
        row_with_highest_max_streak = results[0]

        datas = analytics.max_streak_given_habit(db, given_habit)
        table = Table(title = "\nHABITLOG\n", show_header=True, show_lines=True)
        table.add_column("Habit", min_width=12, justify="center")
        table.add_column("Max_Streak", min_width=12, justify="center")

        for data in datas:
            table.add_row(data.habit, str(data.max_streak))
        console.print(table)
        highest_max_streak = row_with_highest_max_streak.max_streak
        console.print(f"\nThe max. streak for the habit '{given_habit}' is:", highest_max_streak, "\n")
        keep_analyzing()

    except IndexError:
        # If there are no rows in the results list
        typer.secho("\nThere are no records for the given habit !\n")


def update(db_name = None, today = None):
    """
    Check the status of daily and weekly habits and update their completion status in the database.
    Then display the results of the update process.
    
    Args:
        None
        
    Returns:
        None
        
    Raises:
        None
    """
    update_check_daily(db_name, today)
    update_check_weekly(db_name, today)
    update_check_daily_results(db_name)
    update_check_weekly_results(db_name)
    

def log():
    """
    Displays the log of habits in the database.
    
    Args:
        None

    Returns:
        None

    Raises:
        None

    """
    log_function()


def show(periodicity: Optional[str] = typer.Argument(None)):
    """
    Display a list of all habits in the database, or a list of habits with a certain periodicity.

    Args:
        periodicity (str): The desired periodicity of the habits to be displayed. Accepted values are "Daily" and "Weekly".

    Returns:
        None

    Raises:
        Exception: An error occurred while attempting to display the habits.
    """
    if periodicity is None:
        show_all()

    elif periodicity == "Daily":
        show_daily(periodicity)

    elif periodicity == "Weekly":
        show_weekly(periodicity)

    else:
        start_without_update()
            

def edit():
    """
    Edit habit data in the database. This function allows the user to add or delete habits from the database.
    If there are no habits in the database, the function will start the application.
    If there is an error while trying to edit the habit data, it will raise an exception.
    
    Args:
        None
    
    Returns:
        None
    
    Raises:
        Exception: An error occurred while trying to edit the habit data.

    """
    try:
        db = database.connect_db()
    except Exception as e:
        console.print(f"\nError retrieving habits from database: {e}\n")
        return

    if len(database.all_habits(db)) > 0:
        edit_question = qt.select("What do you want to edit?",
        choices=["Add", "Delete", "Go to Start", "Exit"],
        ).ask()

        if edit_question == "Add":
            add_function()
        elif edit_question == "Delete":
            delete_function()
        elif edit_question == "Go to Start":
            start_without_update()
        else:
            exit_app_question()

    else:
        start()


def manage():
    """
    Prompts the user to confirm whether they want to check off their habits. If they confirm, calls the `manage_function` 
    to allow the user to check off their habits. If they do not confirm, prompts the user with options to continue 
    managing their habits or to return to the start menu. If there are no habits in the database, returns to the start 
    menu.

    Args:
        None
    
    Returns:
        None
    
    Raises:
        Exception: An error occurred when attempting to access the database.

    """
    try:
        db = database.connect_db()
    except Exception as e:
        console.print(f"\nError retrieving habits from database: {e}\n")
        return

    if len(database.all_habits(db)) > 0:
        manage_question = qt.confirm("Do you want to Check-off your habits ?").ask()
        if manage_question:
            if database.collect_uncompleted_habits_choices(db) is not None:
                manage_function()
            else:
                typer.secho("\nThere are no uncompleted habits in your database !\n",
                fg=typer.colors.BRIGHT_RED)
                ask_for_intention()
        else:
            start_without_update()
    else:
        start_without_update()


def analyze():
    """
    This function allows the user to choose from a list of options to analyze different aspects of their habits.
    It handles potential errors that may occur while attempting to retrieve or display the requested data.
    
    Args:
        None
    
    Returns:
        None
    
    Raises:
        Exception: If an error occurs while accessing the database or while analyzing the habits.

    """
    try:
        db = database.connect_db()
    except Exception as e:
        console.print(f"\nError retrieving habits from database: {e}\n")
        return

    if len(database.all_habits(db)) > 0:
        analyze_question = qt.select("What do you want to analyze?",
        choices=["All currently tracked habits", "All habits with same periodicity", "Longest streak all habits",
        "Longest streak given habit", "Go to start", "Exit"],
        ).ask()

    if analyze_question == "All currently tracked habits":
        analyze_all()

    elif analyze_question == "All habits with same periodicity":
        analyze_habits_same_periodicity()

    elif analyze_question == "Longest streak all habits":
        analyze_longest_streak_all_habits()

    elif analyze_question == "Longest streak given habit":
        analyze_streak_given_habit()

    elif analyze_question == "Go to start":
        start_without_update()

    else:
        exit_app_question()

if __name__ == "__main__":
    app()