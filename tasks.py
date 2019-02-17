import datetime

class Task:

    def __init__(self, date=None, name, duration, notes):
        if not date:
            self.date = datetime.datetime.now()

        elif date
