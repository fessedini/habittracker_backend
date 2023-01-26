"""
    The main entry point for the habit tracker app. It calls the cli module's app function and sets the app's name as the program name.

    :param prog_name: The name of the app, which is passed from the habittracker module's __app_name__ variable.
    :type prog_name: str
"""

from habittracker import cli, __app_name__

def main():
    cli.app(prog_name=__app_name__)

if __name__ == "__main__":
    main()