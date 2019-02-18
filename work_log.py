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


def display_tasks(tasks):
    for i, task in enumerate(tasks, start=1):
        while True:
            # clear the screen
            os.system("cls" if os.name == "nt" else "clear")
            print(task)
            print("\nResult {} of {}\n".format(i, len(tasks)))
            # Next, Edit, Delete, Return to search menu
            if i < len(tasks):
                print("[N]ext, [E]dit, [D]elete, [R]eturn to search menu")
            else:
                print("[E]dit, [D]elete, [R]eturn to search menu")
            option = input()

            if option.lower() in ['n', 'next'] and i < len(tasks):
                continue
            elif option.lower() in ['e', 'edit']:
                # call edit function
                break  # back to main menu
            elif option.lower() in ['d', 'Delete']:
                # call delete function
                break  # back to main menu
            elif option.lower() in ['r', 'return']:
                pass


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
    while True:
        # set task date
        date_input = input("Date of the task:\nPlease use DD/MM/YYYY: ")  # get the task date from the user
        try:
            task_date = datetime.datetime.strptime(date_input, '%d/%m/%Y').date()
        except ValueError:
            print("Invalid date!!!, try again...")
            continue
        else:
            break

    while True:
        # set task name
        task_name = input("Title of the task: ").strip()
        if not task_name:
            print("Please enter a meaningful title!")
            continue
        else:
            break

    while True:
        try:
            # set task duration
            task_duration = int(input("Time spent (rounded minutes): "))
        except ValueError:
            print("Please enter a valid time duration in minutes!")
            continue
        else:
            break

    # set task note
    task_notes = input("Notes (Optional, you can leave this empty): ").strip()

    new_entry = Task(date=task_date,
                     name=task_name,
                     duration=task_duration,
                     notes=task_notes)

    # write entry to CSV
    new_entry.write_to_csv()
    print("The following entry has been added:")
    print(new_entry)


def search_menu():
    os.system("cls" if os.name == "nt" else "clear")  # clear the screen
    print("Do you want to search by:")

    search_menu_selection = input("What would you like to do?\n"
                                  "a) Exact Date\n"
                                  "b) Range of Dates\n"
                                  "c) Exact Search\n"
                                  "d) Regex Pattern\n"
                                  "e) Return to menu\n")
    return search_menu_selection

def search_existing_entries():
    tasks_dict = Task.load_from_log()  # loads all existing tasks in the work log CSV file
    print("From below dates list\nPlease select a date index:")
    dates = enumerate(tasks_dict.keys(), start=1)
    for i, date in dates:
        print('{}) {}'.format(i, date))
    index = input()
    selected_tasks = tasks_dict[list(tasks_dict.keys())[int(index) - 1]]
    # display_tasks


if __name__ == '__main__':

    while running_program:

        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")

        user_selection = main_menu()

        if user_selection.upper() in ["QUIT", "C"]:
            print("Quitting...Hope to see you soon!")
            break

        elif user_selection.upper() in ["ADD", "A"]:
            os.system("cls" if os.name == "nt" else "clear")  # clear the screen
            add_new_entry()  # call add new entry function
            break

        elif user_selection.upper() in ["SEARCH", "B"]:
            search_menu()
            # search_existing_entries()  # call search existing entries function
            break
