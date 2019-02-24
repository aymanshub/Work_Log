"""
Utilities module for the work log:
    1. add_new_entry
    2. display_tasks
    3. search_by_date
    4. search_range_of_dates
    5. search_time_spent
    6. search_exact_value
    7. search_regex_pattern

"""
import os
import datetime
import csv
import re
import params
from tasks import Task

def verify_log(filename = 'log.csv'):
    # ensure correct log:
    # to verify if log file exists if not to create one
    # 1. if log file exists to verify it being correct:
    #   correct:
    #                   1.first row(header) has exact correct fields
    #               2. if not to open for write with 'w' (truncate), and write header

    fieldnames = ['date', 'task name', 'time spent', 'notes']
    if os.path.exists(filename):
    # check content correctness
        pass
        # check if header exist
        try:
            with open(filename, 'r', newline='') as file:
                reader = csv.DictReader(file)
                if reader.fieldnames[:len(fieldnames)] == fieldnames:
                #if reader.fieldnames == fieldnames:
                    input("GREATTTT we have a an existing {}\n"
                          "with the right field names:{}"
                          .format(filename, fieldnames))
                else:
                    raise ValueError
        except (ValueError, Exception) as e:
            print("The existing {} header\n"
                  "Doesn't comply with expected field names: {}\n{}"
                  .format(filename, fieldnames, e))
            result = False
        else:
            result = True

    else:
        # create new and write header
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
        except Exception as e:
            print("Unable to create a new file: {}\n{}".format(filename, e))
            result = False
        else:
            result = True

    return result


def add_new_entry(for_edit=False):
    """
    Adds new entry\task to the work log file (supporting duplicate-free tasks)
    by taking the new task attributes from the user screen
    :param for_edit: True if the function is used for task editing context
    of an existing task
    :return: None
    """
    if not for_edit:
        os.system("cls" if os.name == "nt" else "clear")  # clear the screen
    while True:
        # set task date
        date_input = input("Date of the task ([{}] to return to Main menu)\n"
                           "Please use DD/MM/YYYY: "
                           .format(params.previous_menu_key.upper()))
        if date_input.upper() == params.previous_menu_key.upper():
            return
        else:
            try:
                task_date = datetime.datetime.strptime(date_input,
                                                       params.date_fmt).date()
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
    if new_task.date.strftime(params.date_fmt) in tasks_dict.keys() and \
            new_task in tasks_dict[new_task.date.strftime(params.date_fmt)]:
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
    """
    Display the selected tasks resulted by a user search criteria.
    :param tasks: list of Task instances
    :return: None
    """
    i = 0
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        commands = "[R]eturn to search menu"
        if not len(tasks):
            print("no tasks have been found.".upper())
        else:
            print(tasks[i])
            print("\nResult {} of {}\n".format(i + 1, len(tasks)))
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
    """
    Displays all the distinct tasks dates to the user in an ascending order,
    where the user should select a date to view all the tasks holding the same
    selected date.
    :param tasks_dict: A dictionary holding all the existing tasks in the log
    file.
    The dictionary keys: the distinct tasks dates values we have in the log
    The dictionary values: all the corresponding tasks that holds the same date
    key.
    :return:None
    """

    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        if tasks_dict:
            print("From below dates list\nPlease select a date index:")
        else:
            print("No existing entries!")
        sorted_dates = sorted(
            [datetime.datetime.strptime(key, params.date_fmt).date()
             for key in tasks_dict.keys()])
        dates = enumerate(sorted_dates, start=1)
        for i, date in dates:
            print('{})\t{}'.format(i, date.strftime(params.date_fmt))
                  .expandtabs(2))

        print('[{}] Return to Search menu'.format(
            params.previous_menu_key.upper()))
        user_input = input()
        if user_input.upper() == params.previous_menu_key.upper():
            return  # return to Search menu
        else:
            try:
                index = int(user_input)
                if 1 <= index <= len(tasks_dict):  # range of selections
                    selected_tasks = tasks_dict[
                        sorted_dates[index - 1].strftime(params.date_fmt)]
                else:
                    raise ValueError
            except ValueError:
                input("Invalid selection, please press Enter to try again...")
                continue
            else:
                display_tasks(selected_tasks)
                return  # go back to Search menu


def search_range_of_dates(tasks_dict):
    """
    Search and displays all tasks found in the date range given by the user.
    :param tasks_dict: A dictionary holding all the existing tasks in the log
    file.
    The dictionary keys: the distinct tasks dates values we have in the log
    The dictionary values: all the corresponding tasks that holds the same date
    key.
    :return: None
    """
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        print("Please enter dates range, use DD/MM/YYYY format\n"
              "Enter [{}] to Return to Search menu"
              .format(params.previous_menu_key.upper()))
        from_date = input("From date: ")
        to_date = input("To date: ")
        if params.previous_menu_key.upper() in (from_date.upper(),
                                                to_date.upper()):
            return  # go back to Search menu
        try:
            from_date = datetime.datetime.strptime(from_date,
                                                   params.date_fmt).date()
            to_date = datetime.datetime.strptime(to_date,
                                                 params.date_fmt).date()
        except ValueError:
            input("Invalid date!!!, press Enter to try again...")
            continue
        else:
            selected_tasks = []
            for key in tasks_dict.keys():
                key_date = datetime.datetime.strptime(key,
                                                      params.date_fmt).date()
                if from_date <= key_date <= to_date:
                    selected_tasks.extend(tasks_dict[key])
            display_tasks(selected_tasks)
            return  # go back to Search menu


def search_time_spent(tasks_dict):
    """
    Search and displays all tasks having the same time spent value given
    by the user.
    :param tasks_dict: A dictionary holding all the existing tasks in the log
    file.
    The dictionary keys: the distinct tasks dates values we have in the log
    The dictionary values: all the corresponding tasks that holds the same date
    key.
    :return: None
    """
    while True:
        # clear the screen
        os.system("cls" if os.name == "nt" else "clear")
        time_spent = input(
            "Please enter a time spent value (rounded minutes)\n"
            "Enter [{}] to Return to Search menu:".format(
                params.previous_menu_key.upper()))
        if time_spent.upper() == params.previous_menu_key.upper():
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
    """
    Search and displays all tasks having the exact value given by the user
    in the task title or notes fields.
    :param tasks_dict: A dictionary holding all the existing tasks in the
    log file.
    The dictionary keys: the distinct tasks dates values we have in the log
    The dictionary values: all the corresponding tasks that holds the same
    date key.
    :return: None
    """
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


def search_regex_pattern(tasks_dict):
    """
    Search and displays all tasks matching the regular-expression value
    given by the user
    in the task title or notes fields.
    :param tasks_dict: A dictionary holding all the existing tasks in the
    log file.
    The dictionary keys: the distinct tasks dates values we have in the log
    The dictionary values: all the corresponding tasks that holds the same
    date key.
    :return: None
    """
    # clear the screen
    os.system("cls" if os.name == "nt" else "clear")
    user_regex = input("Please enter your regex pattern:\n")

    selected_tasks = []
    for i, tasks in tasks_dict.items():
        for task in tasks:
            if re.search(user_regex, task.name) or re.search(user_regex,
                                                             task.notes):
                selected_tasks.append(task)
    display_tasks(selected_tasks)
    return  # go back to Search menu
