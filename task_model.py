from datetime import date
from datetime import datetime


class Task(object):

    def __init__(self, minute=None, hour=None, day_of_month=None, month=None,
                 day_of_week=None, action=None, _id=None, reboot=False):

        if not reboot:
            self.minute = self.__check_minute(minute)
            self.hour = self.__check_hour(hour)
            self.day_of_month = self.__check_day_of_month(day_of_month)
            self.month = self.__check_month(month)
            self.day_of_week = self.__check_day_of_the_week(day_of_week)
        self.action = action
        self._id = _id
        self.reboot = reboot

    def __check_minute(self, minute):
        if ',' in minute:
            minute = minute.split(',')
            separator = ','
        elif '-' in minute:
            minute = minute.split('-')
            separator = '-'
        elif minute == '*':
            return minute
        else:
            separator = None

        if isinstance(minute, list):
            for unit in minute:
                if int(unit) not in range(0, 60):
                    print 'minute not in range'
                    if separator == ',':
                        minute[minute.index(unit)] = '59'
                    elif separator == '-':
                        minute[minute.index(unit)] = '59'
                        minute = minute[:minute.index('59') + 1]
                        minute = separator.join(minute)
                        return minute
        else:
            if int(minute) not in range(0, 60):
                print 'minute not in range'
                minute = '59'
                return minute
        
        if separator:
            minute = sorted(set(minute))
            minute = separator.join(minute)
            return minute
        return minute

    def __check_hour(self, hour):
        if ',' in hour:
            hour = hour.split(',')
            separator = ','
        elif '-' in hour:
            hour = hour.split('-')
            separator = '-'
        elif hour == '*':
            return hour
        else:
            separator = None

        if isinstance(hour, list):
            for unit in hour:
                if int(unit) not in range(0, 24):
                    print 'hour not in range'
                    if separator == ',':
                        hour[hour.index(unit)] = '0'
                    elif separator == '-':
                        hour[hour.index(unit)] = '0'
                        hour = hour[:hour.index('0') + 1]
                        hour = separator.join(hour)
                        return hour
        else:
            if int(hour) not in range(0, 24):
                print 'hour not in range'
                hour = '*'
                return hour

        if separator:
            hour = sorted(set(hour))
            hour = separator.join(hour)
            return hour
        return hour

    def __check_date(self):
        if self.day_of_month != '*' and self.month != '*':

            if ',' in self.day_of_month:
                all_days_of_month = self.day_of_month.split(',')
            elif '-' in self.day_of_month:
                day_of_month = self.day_of_month.split('-')
                all_days_of_month = range(int(day_of_month[0]),
                                          int(day_of_month[-1]) + 1)
            else:
                all_days_of_month = self.day_of_month

            if ',' in self.month:
                all_month = self.month.split(',')
            elif '-' in self.month:
                month = self.month.split('-')
                all_month = range(int(month[0]), int(month[-1]) + 1)
            else:
                all_month = self.month

            for month in all_month:
                for day in all_days_of_month:
                    try:
                        if datetime(date.today().year, int(month), int(day)):
                            pass
                    except ValueError as error:
                        if str(error) == 'day is out of range for month':
                            print 'day is out of range for month'
                            self.day_of_month = '*'
                            return self.day_of_month

        return self.day_of_month

    def __check_day_of_the_week(self, day_of_week):
        week_days = {'mon': '1', 'tue': '2', 'wed': '3', 'thu': '4',
                     'fri': '5', 'sat': '6', 'sun': '0'}

        if ',' in day_of_week:
            day_of_week = day_of_week.split(',')
            separator = ','
        elif '-' in day_of_week:
            day_of_week = day_of_week.split('-')
            separator = '-'
        elif day_of_week == '*':
            return day_of_week
        else:
            separator = None

        if isinstance(day_of_week, list):
            for unit in day_of_week:
                if unit not in week_days and unit not in week_days.values():
                    print 'day_of_week not in range'
                    day_of_week = '*'
                    return day_of_week
        else:
            for day in week_days:
                if day_of_week == day or day_of_week == week_days.get(day):
                    return day_of_week
            print 'day_of_week not in range'
            day_of_week = '*'
            return day_of_week

        if separator:
            return separator.join(day_of_week)
        return day_of_week

    def output(self):
        if self.reboot:
            return '@reboot ' + self.action
        return str(self.minute) + ' ' + str(self.hour) + ' ' \
               + str(self.__check_date()) + ' ' + str(self.month) + ' ' \
               + str(self.day_of_week) + ' ' + self.action

    def __check_month(self, month):
        if ',' in month:
            month = month.split(',')
            separator = ','
        elif '-' in month:
            month = month.split('-')
            separator = '-'
        elif month == '*':
            return month
        else:
            separator = None

        if isinstance(month, list):
            for unit in month:
                if int(unit) not in range(1, 13):
                    print 'month not in range'
                    month = '*'
                    return month
        else:
            if int(month) not in range(1, 13):
                print 'month not in range'
                month = '*'
                return month

        if separator:
            return separator.join(month)
        return month

    def __check_day_of_month(self, day_of_month):
        if ',' in day_of_month:
            day_of_month = day_of_month.split(',')
            separator = ','
        elif '-' in day_of_month:
            day_of_month = day_of_month.split('-')
            separator = '-'
        elif day_of_month == '*':
            return day_of_month
        else:
            separator = None

        if isinstance(day_of_month, list):
            for unit in day_of_month:
                if int(unit) not in range(1, 32):
                    print 'day_of_month not in range'
                    if separator == ',':
                        day_of_month[day_of_month.index(unit)] = '30'
                    elif separator == '-':
                        day_of_month[day_of_month.index(unit)] = '30'
                        day_of_month = day_of_month[:day_of_month.index('30')+1]
                        day_of_month = separator.join(day_of_month)
                        return day_of_month
        else:
            if int(day_of_month) not in range(1, 32):
                print 'day_of_month not in range'
                day_of_month = '*'
                return day_of_month

        if separator:
            day_of_month = sorted(set(day_of_month))
            day_of_month = separator.join(day_of_month)
            return day_of_month
        return day_of_month


example = Task('1,2,3,60,70,2,5', '1-60', '20-31', '1-10', '*', 'burn!')
print example.output()
