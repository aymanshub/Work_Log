"""
Python Web Development Techdegree
Project 3 - Work Log
--------------------------------
Developed by: Ayman Said
Feb-2019
"""

import os
import datetime
from tasks import Task

running_program = True


def main_menu():

    welcome_msg = "Welcome To Work Log"

    print("-" * len(welcome_msg))
    print(welcome_msg)
    print("-" * len(welcome_msg))

    main_menu_selection = input("What would you like to do?\n"
                                "a) Add new entry\n"
                                "b) Search in existing entries\n"
                                "c) Quit program\n"
                                "")

    return main_menu_selection


def add_new_entry():
    # set task date
    date_input = input("Date of the task:\nPlease use DD/MM/YYYY: ")  # get the task date from the user
    task_date = datetime.datetime.strptime(date_input,'%d/%m/%Y')
    # ToDo validate date correctness

    # set task name
    task_name = input("Title of the task: ")
    # ToDo clean trailing white-spaces

    # set task duration
    task_duration = int(input("Time spent (rounded minutes): "))
    # ToDo validate correctness

    # set task note
    task_notes = input("Notes (Optional, you can leave this empty): ")

    new_entry = Task(date=task_date,
                     name=task_name,
                     duration=task_duration,
                     notes=task_notes)

    new_entry.write_to_csv()
    print("The following entry has been added:")
    print(new_entry)

    # writeToCSV


def search_in_existing_entries():
    pass


if __name__ == '__main__':

    while running_program:

        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")

        user_selection = main_menu()

        if user_selection.upper() in ["QUIT", "C"]:
            print("Quitting...Hope to see you soon!")
            break

        elif user_selection.upper() in ["ADD", "A"]:
            # call add new entry function
            add_new_entry()
            break

        elif user_selection.upper() in ["SEARCH", "B"]:
            search_in_existing_entries()

