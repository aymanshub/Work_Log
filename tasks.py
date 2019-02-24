"""
tasks module defines the Task class
"""
import os
import datetime
import csv
import params


class Task:
    """
    Task class and all it's attributes & methods:
        Task instance attributes:
            date, name, time_spent, notes
        Task methods:
            add_task_to_file
            delete_task_from_log
            load_from_log
        Object overridden instance methods:
            __init__, __str__, __eq__,__ne__
    """

    def __init__(self, date=None, name=None, time_spent=0, notes=None):
        self.date = datetime.date.today() if date is None else date
        self.name = name
        self.time_spent = time_spent
        self.notes = notes

    def __str__(self):
        return "Date: {date}\n" \
               "Title: {title}\n" \
               "Time Spent: {time_spent}\n" \
               "Notes: {notes}"\
            .format(date=datetime.date.strftime(self.date, params.date_fmt),
                    title=self.name,
                    time_spent=self.time_spent,
                    notes=self.notes)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def add_task_to_file(self, filename=params.log_file_name):
        """
        Adds and writes the task instance to the given log file
        :param filename: log csv filename
        :return: None
        """

        f_exit = True  # to exit program due to errors on file open\write

        try:
            with open(filename, "a", newline='') as csvfile:
                fieldnames = ['date', 'task name', 'time spent', 'notes']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                    'date': self.date.strftime(params.date_fmt),
                    'task name': self.name,
                    'time spent': self.time_spent,
                    'notes': self.notes,
                })
        except FileNotFoundError:
            print("The file: {} is not found.".format(filename))
        except Exception as e:
            print("Error in file: {}\n{}".format(filename, e))
        else:
            f_exit = False

        if f_exit:
            exit(1)  # Exits the program due to the caught errors

    def delete_task_from_log(self,
                             filename=params.log_file_name,
                             tempfile='temp.csv'):
        """
        Deletes the task instance from the log file.
        The deletion is made by using a temp file for copying all entries
        except for the selected entry for deletion, and then deletes
        the original log and renames the temp log to the original log filename.
        :param filename:
        :param tempfile:
        :return:
        """
        try:
            with open(filename, newline='') as original, \
                    open(tempfile, 'w', newline='') as output:
                fieldnames = ['date', 'task name', 'time spent', 'notes']
                reader = csv.DictReader(original)
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                i = 1  # rows counter used for error handling
                for row in reader:
                    i += 1
                    # create task object from row
                    try:
                        date = datetime.datetime\
                            .strptime(row['date'], params.date_fmt).date()
                        row_task = self.__class__(date,
                                                  row['task name'],
                                                  int(row['time spent']),
                                                  row['notes'])
                    except ValueError:
                        print("invalid record in {} , "
                              "see line#{}\n skipping task!"
                              .format(filename, i))
                    else:
                        # ignoring copying the task for deletion to tempfile
                        if self != row_task:
                            writer.writerow(row)
        except FileNotFoundError:
            print("The file: {} is not found.".format(filename))
        except Exception as e:
            print("Error in file: {} or {}\n{}".format(filename, tempfile, e))
        else:
            # Rename tempfile to filename,
            # first remove existing filename then rename temp file
            os.remove(filename)
            os.rename(tempfile, filename)

    @classmethod
    def load_from_log(cls, filename=params.log_file_name):
        """
        Class method that reads all the log file entries and load then
        into a tasks dictionary where the dictionary keys are: the distinct
        tasks dates values we have in the log.
        :param filename:
        :return:
        """
        tasks_dict = {}
        try:
            with open(filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                i = 0
                for row in reader:
                    i += 1
                    try:
                        date = datetime.datetime\
                            .strptime(row['date'], params.date_fmt).date()
                        new_task = cls(date,
                                       row['task name'],
                                       int(row['time spent']),
                                       row['notes'])
                    except ValueError:
                        print("invalid record in {} , see line#{}\n"
                              "skipping task!".format(filename, i))
                    else:
                        if row['date'] not in tasks_dict:
                            tasks_dict[row['date']] = []
                        tasks_dict[row['date']].append(new_task)
        except FileNotFoundError:
            print("The file: {} is not found.".format(filename))
        except Exception as e:
            print("Error in file: {}\n{}".format(filename, e))
        else:
            return tasks_dict
