import datetime
import csv
import sys


class Task:

    def __init__(self, date=None, name=None, duration=0, notes=None):
        self.date = datetime.date.today() if date is None else date
        self.name = name
        self.duration = duration
        self.notes = notes

    def __str__(self):
        return "Date: {date}\n" \
               "Title: {title}\n" \
               "Time Spent: {duration}\n" \
               "Notes: {notes}".format(date=datetime.datetime.strftime(self.date,'%d/%m/%Y'),
                                       title=self.name,
                                       duration=self.duration,
                                       notes=self.notes)

    def write_to_csv(self, filename='work_log.csv'):

        f_exit = True  # indicates if the program should be terminated due to potential errors on file open\write
        # verify if file exists, with the right header
        try:
            with open(filename, "a", newline='') as csvfile:
                fieldnames = ['date', 'task name', 'time spent', 'notes']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({
                    'date': self.date,
                    'task name': self.name,
                    'time spent': self.duration,
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

    @classmethod
    def load_from_log(cls, filename='work_log.csv'):
        tasks_Dict = {}
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new_task = cls(row['date'], row['task name'], row['time spent'], row['notes'])
                if row['date'] not in tasks_Dict:
                    tasks_Dict[row['date']] = []
                tasks_Dict[row['date']].append(new_task)

        return tasks_Dict


def _flog_exists(filename='work_log.csv'):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                print(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
