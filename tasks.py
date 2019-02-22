import os
import datetime
import csv

date_fmt = '%d/%m/%Y'


class Task:

    def __init__(self, date=None, name=None, time_spent=0, notes=None):
        self.date = datetime.date.today() if date is None else date
        self.name = name
        self.time_spent = time_spent
        self.notes = notes

    def __str__(self):
        return "Date: {date}\n" \
               "Title: {title}\n" \
               "Time Spent: {time_spent}\n" \
               "Notes: {notes}".format(date=datetime.date.strftime(self.date, date_fmt),
                                       title=self.name,
                                       time_spent=self.time_spent,
                                       notes=self.notes)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return self.__dict__ != other.__dict__

    def add_task_to_file(self, filename='log.csv'):

        f_exit = True  # indicates if the program should be terminated due to potential errors on file open\write
        # verify if file exists, with the right header
        try:
            with open(filename, "a", newline='') as csvfile:
                fieldnames = ['date', 'task name', 'time spent', 'notes']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                    'date': self.date.strftime(date_fmt),
                    'task name': self.name,
                    'time spent': self.time_spent,
                    'notes': self.notes,
                })
        except FileNotFoundError:
            print("The file: {} is not found.".format(filename))
        except Exception as e:
            print("Error in input file: {}\n{}".format(filename, e))
        else:
            f_exit = False

        if f_exit:
            exit(1)  # Exits the program due to the caught errors

    def delete_task_from_log(self, filename='log.csv', tempfile='temp.csv'):

        with open(filename, newline='') as original, open(tempfile, 'w', newline='') as output:
            fieldnames = ['date', 'task name', 'time spent', 'notes']
            reader = csv.DictReader(original)
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            i = 1  # rows counter used for error handling
            for row in reader:
                i += 1
                # create task object from row
                try:
                    date = datetime.datetime.strptime(row['date'], date_fmt).date()
                    row_task = self.__class__(date, row['task name'], int(row['time spent']), row['notes'])
                except ValueError:
                    print("invalid record in {} , see line#{}\n skipping task!".format(filename, i))
                else:
                    # ignoring the task for deletion so it will not be copied to the new log
                    if self != row_task:
                        writer.writerow(row)
        # Rename tempfile to filename, first remove existing filename then rename temp file
        os.remove(filename)
        os.rename(tempfile, filename)

    @classmethod
    def load_from_log(cls, filename='log.csv'):
        tasks_dict = {}
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            i = 0
            for row in reader:
                i += 1
                try:
                    date = datetime.datetime.strptime(row['date'], date_fmt).date()
                    new_task = cls(date, row['task name'], int(row['time spent']), row['notes'])
                except ValueError:
                    print("invalid record in {} , see line#{}\n skipping task!".format(filename, i))
                else:
                    if row['date'] not in tasks_dict:
                        tasks_dict[row['date']] = []
                    tasks_dict[row['date']].append(new_task)

        return tasks_dict
