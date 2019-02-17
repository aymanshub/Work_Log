import datetime

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


