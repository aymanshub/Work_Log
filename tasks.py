import datetime
import csv
import sys

class Task:

    def __init__(self, date=None, name=None, duration=0, notes=None):
        self.date = datetime.datetime.now() if date is None else date
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
        # verify if file exists, with the right header
        with open(filename, "a", newline='') as csvfile:
            fieldnames = ['date', 'task name', 'time spent', 'notes']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({
                'date': self.date,
                'task name': self.name,
                'time spent': self.duration,
                'notes': self.notes,
            })



def _flog_exists(filename='work_log.csv'):
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                print(row)
        except csv.Error as e:
            sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))
