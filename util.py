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

        # loads all existing tasks in the work log CSV file
        tasks_dict = Task.load_from_log()

        if user_selection.upper() in ["Select a Date".upper(), "A"]:
            search_by_date(tasks_dict)  # call search by date function
        elif user_selection.upper() in ["Range of Dates".upper(), "B"]:
            search_range_of_dates(tasks_dict)  # call search by range of dates function
        elif user_selection.upper() in ["Time spent".upper(), "C"]:
            search_time_spent(tasks_dict)  # call search by time spent function
        elif user_selection.upper() in ["Exact Search".upper(), "D"]:
            search_exact_value(tasks_dict)  # call search by exact value function
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
            # set task time_spent
            time_spent = int(input("Time spent (rounded minutes): "))
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
                    time_spent=time_spent,
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


def display_tasks(tasks):
    i = 0
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        commands = "[R]eturn to search menu"
        if not len(tasks):
            print("no tasks have been found.".upper())
        else:
            print(tasks[i])
            print("\nResult {} of {}\n".format(i+1, len(tasks)))
            commands = "[E]dit, [D]elete, " + commands
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

        if option.lower() in ['n', 'next'] and i < len(tasks) - 1:
                i += 1
        elif option.lower() in ['b', 'back'] and i > 0:
                i -= 1
        elif option.lower() in ['e', 'edit'] and len(tasks):
            # clear the screen
            os.system("cls" if os.name == "nt" else "clear")
            print("Please edit the following task:\n{}".format(tasks[i]))
            # edit is equivalent to delete existing and make new entry
            tasks[i].delete_task_from_log()
            add_new_entry(for_edit=True)
            return  # back to search menu
        elif option.lower() in ['d', 'Delete'] and len(tasks):
            # call delete method
            tasks[i].delete_task_from_log()
            return  # back to search menu
        elif option.lower() in ['r', 'return']:
            return  # back to search menu


def search_by_date(tasks_dict):
    # get the whole exiting tasks from the tasks log file and loads it into a dictionary
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
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
                    return  # return to Search menu
                else:
                    selected_tasks = tasks_dict[list(tasks_dict.keys())[index - 1]]
            else:
                raise ValueError
        except ValueError:
            input("Invalid selection, please press Enter to try again...")
            continue
        else:
            display_tasks(selected_tasks)
            return  # go back to Search menu


def search_range_of_dates(tasks_dict):
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        print("Please enter dates range, use DD/MM/YYYY format\nEnter [R] to Return to Search menu")
        from_date = input("From date: ")
        to_date = input("To date: ")
        if 'R' in (from_date.upper(), to_date.upper()):
            return  # go back to Search menu
        try:
            from_date = datetime.datetime.strptime(from_date, date_fmt).date()
            to_date = datetime.datetime.strptime(to_date, date_fmt).date()
        except ValueError:
            input("Invalid date!!!, press Enter to try again...")
            continue
        else:
            selected_tasks = []
            for key in tasks_dict.keys():
                key_date = datetime.datetime.strptime(key, date_fmt).date()
                if from_date <= key_date <= to_date:
                    selected_tasks.extend(tasks_dict[key])
            display_tasks(selected_tasks)
            return  # go back to Search menu


def search_time_spent(tasks_dict):
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        time_spent = input("Please enter a time spent value (rounded minutes)\nEnter [R] to Return to Search menu:")
        if time_spent.upper() == 'R':
            return  # go back to Search menu
        try:
            time_spent = int(time_spent)
        except ValueError:
            input("Invalid value!!!, press Enter to try again...")
            continue
        else:
            selected_tasks = []
            for tasks in tasks_dict.values():
                for task in tasks:
                    if task.time_spent == time_spent:
                        selected_tasks.append(task)
            display_tasks(selected_tasks)
            return  # go back to Search menu


def search_exact_value(tasks_dict):
    # clear the screen
    os.system("cls" if os.name == "nt" else "clear")
    text = input("Please enter any text to find in the Work Log:\n")
    selected_tasks = []
    for tasks in tasks_dict.values():
        for task in tasks:
            if text in task.name or text in task.notes:
                selected_tasks.append(task)
    display_tasks(selected_tasks)
    return  # go back to Search menu


def search_regex_pattern():
    pass
