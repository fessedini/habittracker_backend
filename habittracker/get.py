
import typer

import questionary

from habittracker import database

qt = questionary


def habit_entry():
    """
    Prompt the user to enter a habit in one word.

    Returns:
    str: The user-entered habit.
    """
    return qt.text("Please enter the habit you want to store in one word:",
    validate=lambda habit: True if habit.isalpha() and len(habit) > 1 and habit[0].isupper()
    else "Your choice is not valid ! Validiation = Start with capital letter, only alphabetic characters, more then one character and only one word! Please try again !").ask()
    
def habit_description():
    """
    Prompt the user to enter a description in five words.

    Returns:
    str: The user-entered description.
    """
    return qt.text("Please enter a description in max five words:",
    validate=lambda description: True if (description[0].isupper() or description[0].isnumeric()) and (len(description.split()) <= 5)
    else "Your choice is not valid ! Validiation = Start with capital letter or number and use only letters and numbers !!"
    ).ask()

def habit_periodicity():
    """
    Prompt the user to select a periodicity for a habit.

    Returns:
    str: The selected periodicity.
    """
    return qt.select("Please select a suitable periodicity for your habit:",
    choices = ["Daily", "Weekly"]
    ).ask()

def analyze_habit_periodicity():
    """
    Prompt the user to select a periodicity to be analyzed.

    Returns:
    str: The selected periodicity.
    """
    return qt.select("Please select the periodicity to be analyzed:",
    choices=["Daily", "Weekly"]
    ).ask()

def habits_of_database():
    """
    Prompt the user to select a habit from the database.

    Returns:
    str: The selected habit.
    """
    db = database.connect_db()
    all_habits = database.collect_habits_choices(db)
    if all_habits is not None:
        return qt.select("Please select one habit:",
        choices = sorted(all_habits)).ask()
    else:
        typer.secho("\nThere is no habit in your database! Please add a habit first!\n",
        fg=typer.colors.BRIGHT_RED)

def uncompleted_habits():
    """
    This function retrieves all the uncompleted habits from the habitsbase table of the database, and display them to the user to select one of them.
    
    Methods called:
    connect_db() from module 'database'
    collect_uncompleted_habits_choices(db) from module 'database'
    select() from module 'qt'
    ask() from module 'qt'
    secho() from module 'typer'
    
    Returns:
    The selected habit name (str) if there are any uncompleted habits in the habitsbase table, otherwise None.
    """
    db = database.connect_db()
    all_uncompleted_habits = database.collect_uncompleted_habits_choices(db)
    if all_uncompleted_habits is not None:
        return qt.select("Please select one habit:",
        choices= sorted(all_uncompleted_habits)).ask()
    else:
        typer.secho("\nThere is no habit in your database! Please add a habit first!\n",
        fg=typer.colors.BRIGHT_RED)

def adding_confirmation(habit_to_add, description_to_add, periodicity_to_add):
    """
    Prompt the user to confirm the addition of a habit.

    Parameters:
    habit_to_add (str): The habit to be added.
    description_to_add (str): The description of the habit to be added.
    periodicity_to_add (str): The periodicity of the habit to be added.

    Returns:
    bool: True if the user confirms the addition, False otherwise.
    """
    return qt.confirm(f"Are you sure you want to add the habit '{habit_to_add}' with the description '{description_to_add}' as '{periodicity_to_add}' ?").ask()

def delete_confirmation(habit_to_delete):
    """
    Prompt the user to confirm that they want to delete the specified habit.

    Parameters:
    - habit_to_delete (str): The name of the habit that the user is being asked to confirm for deletion.

    Returns:
    - bool: True if the user confirms the deletion, False if they cancel or close the prompt.
    """
    return qt.confirm(f"Are you sure you want to delete the habit '{habit_to_delete}' ?").ask()

def check_off_confirmation(habit_to_checkoff):
    """
    Prompt the user to confirm that they want to check off the specified habit.

    Parameters:
    - habit_to_checkoff (str): The name of the habit that the user is being asked to confirm for check off.

    Returns:
    - bool: True if the user confirms the check off, False if they cancel or close the prompt.
    """
    return qt.confirm(f"Are you sure you want to check-off the habit '{habit_to_checkoff}' ?").ask()