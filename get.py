
import questionary

from habittracker import database

qt = questionary


def habit_entry():
    return qt.text("Please enter the habit you want to store in one word:",
    validate=lambda habit: True if habit.isalpha() and len(habit) >1 and habit[0].isupper()
    else "Your choice is not valid ! Validiation = Start with capital letter, only alphabetic characters, more then one character! Please try again !").ask()


def habit_description():
    return qt.text("Please enter a short description with max. 5 words to your habit:").ask()


def habit_periodicity():
    return qt.select("Please select a suitable periodicity for your habit:",
    choices = ["Daily", "Weekly"]
    ).ask()

def analyze_habit_periodicity():
    return qt.select("Please select the periodicity to be analyzed:",
    choices=["Daily", "Weekly"]
    ).ask()

def habit_periodicity_change():
    return qt.select("Please select the new suitable periodicity for your habit:",
    choices=["Daily", "Weekly"]
    ).ask()

def periodicity_change_confirmation():
    return qt.confirm("A change of the periodicity is accompanied with a setback of your streak ! Are you sure you want to change the periodicity?").ask()


def old_periodicity_of_habit(habit_old_periodicity):
    db =database.connect_db()
    periodicity = database.periodicity_of_habit(db, habit_old_periodicity)
    return periodicity


def habits_of_database():
    db = database.connect_db()
    all_habits = database.collect_habits_choices(db)
    if all_habits is not None:
        return qt.select("Please select one habit:",
        choices = sorted(all_habits)).ask()
    else:
        raise ValueError("There is no habit in your database! Please add a habit first!")


def adding_confirmation(habit_to_add, description_to_add, periodicity_to_add):
    return qt.confirm(f"Are you sure you want to add the habit '{habit_to_add}' with the description '{description_to_add}' as '{periodicity_to_add}' ?").ask()


def delete_confirmation(habit_to_delete):
    return qt.confirm(f"Are you sure you want to delete the habit '{habit_to_delete}' ?").ask()


def check_off_confirmation(habit_to_checkoff):
    return qt.confirm(f"Are you sure you want to check-off the habit '{habit_to_checkoff}' ?").ask()


def set_back_confirmation(habit_to_setback):
    return qt.confirm(f"Are you sure you want to set-back the habit '{habit_to_setback}' ?").ask()


def habit_streak_confirmation(habit_streak_name):
    return qt.confirm(f"Do you want to analyze the longest streak of the habit '{habit_streak_name}' ?").ask()


def habit_choices():
    habit_choice = qt.select("Which overview do you want to analyze?",
    choices = ["All currently tracked habits", "All daily habits", "All weekly habits"],
    ).ask()
    return habit_choice


def streak_choice():
    streak_question = qt.select("Which longest run streak should be analyzed?",
    choices =["Of all definded habits", "For a given habit"],
    ).ask()
    return streak_question