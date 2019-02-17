"""
Python Web Development Techdegree
Project 3 - Work Log
--------------------------------
Developed by: Ayman Said
Feb-2019
"""

import os

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
    pass


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

        elif user_selection.upper() in ["SEARCH", "B"]:
            search_in_existing_entries()

