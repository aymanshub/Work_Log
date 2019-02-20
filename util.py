import os
import datetime
from tasks import Task

date_fmt = '%d/%m/%Y'


def main_menu():
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        welcome_msg = "Welcome To Work Log"

        print("-" * len(welcome_msg))
        print(welcome_msg)
        print("-" * len(welcome_msg))

        user_selection = input("What would you like to do?\n"
                               "a) Add new entry\n"
                               "b) Search in existing entries\n"
                               "c) Quit program\n"
                               "")

        if user_selection.upper() in ["ADD", "A"]:
            add_new_entry()  # call add new entry function
        elif user_selection.upper() in ["SEARCH", "B"]:
            search_menu()
        elif user_selection.upper() in ["QUIT", "C"]:
            print("Quitting...Hope to see you soon!")
            break


def search_menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")  # clear the screen
        user_selection = input("Please select your desirable search method:\n"
                               "a) Select a Date\n"
                               "b) Range of Dates\n"
                               "c) Time spent\n"
                               "d) Exact Search\n"
                               "e) Regex Pattern\n"
                               "f) Return to Main menu\n")

        if user_selection.upper() in ["Select a Date".upper(), "A"]:
            search_by_date()  # call search by date function
        elif user_selection.upper() in ["Range of Dates".upper(), "B"]:
            search_range_of_dates()  # call search by range of dates function
        elif user_selection.upper() in ["Time spent".upper(), "C"]:
            search_time_spent()  # call search by time spent function
        elif user_selection.upper() in ["Exact Search".upper(), "D"]:
            search_exact_value()  # call search by exact value function
        elif user_selection.upper() in ["Regex Pattern".upper(), "E"]:
            search_regex_pattern()  # call search by regex pattern function
        elif user_selection.upper() in ["Return to Main menu".upper(), "F"]:
            break


def add_new_entry(for_edit=False):
    if not for_edit:
        os.system("cls" if os.name == "nt" else "clear")  # clear the screen
    while True:
        # set task date
        date_input = input("Date of the task:\nPlease use DD/MM/YYYY: ")  # get the task date from the user
        try:
            task_date = datetime.datetime.strptime(date_input, date_fmt).date()
        except ValueError:
            input("Invalid date!!!, press Enter to try again...")
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
            input("Invalid value!!!, press Enter to try again...")
            continue
        else:
            break

    # set task note
    task_notes = input("Notes (Optional, you can leave this empty): ").strip()

    # create a new task instance
    new_task = Task(date=task_date,
                    name=task_name,
                    duration=task_duration,
                    notes=task_notes)

    # check for duplicates, task should not be more than once in the log.
    tasks_dict = Task.load_from_log()
    if new_task.date.strftime(date_fmt) in tasks_dict.keys() and \
            new_task in tasks_dict[new_task.date.strftime(date_fmt)]:
        if not for_edit:
            print("Such task already exists!")
    else:
        # write task to log file
        new_task.add_task_to_file()
        if for_edit:
            print("\nTask edit completed successfully.")
        else:
            print("\nThe task has been added successfully.")

    input("Press enter to continue...")


def display_selected_tasks(tasks):
    i = 0
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        print(tasks[i])
        print("\nResult {} of {}\n".format(i+1, len(tasks)))
        commands = "[E]dit, [D]elete, [R]eturn to search menu"
        if i < len(tasks) - 1:
            # Add Next command
            commands = "[N]ext, " + commands
            if i > 0:
                # Add Back command
                commands = "[B]ack, " + commands
        elif i > 0:
            # Add Back command
            commands = "[B]ack, " + commands
        print(commands)
        option = input()

        if option.lower() in ['n', 'next']:
            if i < len(tasks) - 1:
                i += 1
        elif option.lower() in ['b', 'back']:
            if i > 0:
                i -= 1
        elif option.lower() in ['e', 'edit']:
            # clear the screen
            os.system("cls" if os.name == "nt" else "clear")
            print("Please edit the following task:\n{}".format(tasks[i]))
            tasks[i].delete_task_from_log()
            add_new_entry(for_edit=True)
            break  # back to search menu
        elif option.lower() in ['d', 'Delete']:
            # call delete function
            tasks[i].delete_task_from_log()
            break  # back to search menu
        elif option.lower() in ['r', 'return']:
            break  # back to search menu


def search_by_date():
    # get the whole exiting tasks from the tasks log file and loads it into a dictionary
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        tasks_dict = Task.load_from_log()  # loads all existing tasks in the work log CSV file
        print("From below dates list\nPlease select a date index:")
        dates = enumerate(tasks_dict.keys(), start=1)
        for i, date in dates:
            print('{}) {}'.format(i, date))
        max_index = len(tasks_dict)+1
        print('{}) Return to Search menu'.format(max_index))
        try:
            index = int(input())
            if 1 <= index <= max_index: # range of valid selections
                if index == max_index:
                    break # return to Search menu
                else:
                    selected_tasks = tasks_dict[list(tasks_dict.keys())[index - 1]]
            else:
                raise ValueError
        except ValueError:
            input("Invalid selection, please press Enter to try again...")
            continue
        else:
            display_selected_tasks(selected_tasks)
            return # go back to Search menu


def search_range_of_dates():
    while True:
        print("Please enter dates range, use DD/MM/YYYY format")
        try:
            from_date = input("From date: ")
            to_date = input("To date: ")
        except ValueError:
            input("Invalid date!!!, press Enter to try again...")
            continue
        else:
            break

    # get tasks
    # display using display_selected_tasks(tasks)


def search_time_spent():
    while True:
        try:
            time_spent = input("Please enter the time spent value (rounded minutes): ")
        except ValueError:
            input("Invalid value!!!, press Enter to try again...")
            continue
        else:
            break

    # get tasks by time spent
    # display using display_selected_tasks(tasks)


def search_exact_value():
    pass


def search_regex_pattern():
    pass
