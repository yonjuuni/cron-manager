from datetime import date
from datetime import datetime


class Task(object):

    def __init__(self, minute, hour, day_of_month, month, day_of_week, action):
        
        self.minute = self.__chech_minute(minute)
        self.hour = self.__chech_hour(hour)
        self.day_of_month = self.__check_day_of_month(day_of_month)
        self.month = self.__check_month(month)
        self.day_of_week = self.__check_day_of_the_week(day_of_week)
        self.action = action
        self._id = None

    def __chech_minute(self, minute):
        if minute not in range(0, 60):
            print 'minute not in range'
            minute = '*'
            return minute
        return minute

    def __chech_hour(self, hour):
        if hour not in range(0, 24):
            print 'hour not in range'
            hour = '*'
            return hour
        return hour

    def __chech_date(self):
        if self.day_of_month != '*' and self.month != '*':
            try:
                if datetime(date.today().year, self.month, self.day_of_month):
                    return self.day_of_month, self.month
            except ValueError as error:
                if str(error) == 'day is out of range for month':
                    print 'day is out of range for month, day_of_month = *'
                    self.day_of_month = '*'
        return self.day_of_month

    def __check_day_of_the_week(self, day_of_week):
        week_days = {'mon': 1, 'tue': 2, 'wed': 3, 'thu': 4, 'fri': 5, 'sat': 6,
                     'sun': 7}
        for day in week_days:
            if day_of_week == day or day_of_week == week_days.get(day):
                return day_of_week
        day_of_week = '*'
        return day_of_week

    def output(self):
        return str(self.minute) + ' ' + str(self.hour) + ' ' \
               + str(self.__chech_date()) + ' ' + str(self.month) + ' ' \
               + str(self.day_of_week) + ' ' + self.action

    def __check_month(self, month):
        if month in range(1, 13):
            return month
        month = '*'
        return month

    def __check_day_of_month(self, day_of_month):
        if day_of_month in range(1, 32):
            return day_of_month
        day_of_month = '*'
        return day_of_month


example = Task(10, 24, 32, 13, 'tue', 'burn!')
print example.output()

