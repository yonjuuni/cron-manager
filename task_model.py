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
        slash = [0, 0]
        if '/' in minute:
            slash = minute.split('/')
            if int(slash[1]) not in range (1, 60):
                print "Wrong using of '/' for minute"
                slash[1] = 0
        else:
            slash[0] = minute    

        if ',' in slash[0]:
            slash[0] = slash[0].split(',')
            separator = ','
        elif '-' in minute:
            slash[0] = slash[0].split('-')
            separator = '-'
        elif slash[0] == '*':
            if slash[1]:
                return minute
            else:
                return '*'
        else:
            if slash[1]:
                print "Wrong using of '/' for minute"
                slash[1] = 0
            separator = None

        if isinstance(slash[0], list):
            for unit in slash[0]:
                if int(unit) not in range(0, 60):
                    print 'minute not in range'
                    if separator == ',':
                        slash[0][slash[0].index(unit)] = '59'
                    elif separator == '-':
                        slash[0][slash[0].index(unit)] = '59'
                        slash[0] = slash[0][:slash[0].index('59') + 1]
                        #slash[0] = separator.join(slash[0])
        else:
            if int(slash[0]) not in range(0, 60):
                print 'minute not in range'
                slash[0] = '59'
        
        if separator == ',':
            slash[0] = sorted(set(slash[0]))
            slash[0] = separator.join(slash[0])
        elif separator == '-':
            slash[0] = separator.join(slash[0])

        if slash[1]:
            minute = '/'.join(slash)
        else:
            minute = slash[0]
        return minute

    def __check_hour(self, hour):
        slash = [0, 0]
        if '/' in hour:
            slash = hour.split('/')
            if int(slash[1]) not in range (1, 24):
                print "Wrong using of '/' for hour"
                slash[1] = 0
        else:
            slash[0] = hour    

        if ',' in slash[0]:
            slash[0] = slash[0].split(',')
            separator = ','
        elif '-' in slash[0]:
            slash[0] = slash[0].split('-')
            separator = '-'
        elif slash[0] == '*':
            if slash[1]:
                return hour
            else:
                return '*'
        else:
            if slash[1]:
                print "Wrong using of '/' for hour"
                slash[1] = 0
            separator = None

        if isinstance(slash[0], list):
            for unit in slash[0]:
                if int(unit) not in range(0, 24):
                    print 'hour not in range'
                    if separator == ',':
                        slash[0][slash[0].index(unit)] = '0'
                    elif separator == '-':
                        slash[0][slash[0].index(unit)] = '0'
                        slash[0] = slash[0][:slash[0].index('0') + 1]
                        #slash[0] = separator.join(slash[0])
        else:
            if int(slash[0]) not in range(0, 24):
                print 'hour not in range'
                slash[0] = '0'

        if separator == ',':
            slash[0] = sorted(set(slash[0]))
            slash[0] = separator.join(slash[0])
        elif separator == '-':
            slash[0] = separator.join(slash[0])
            
        if slash[1]:
            hour = '/'.join(slash)
        else:
            hour = slash[0]
        return hour

    def __check_date(self):
        max_value = []
        slash_day = [0, 0]
        slash_month = [0, 0]

        if '/' in self.day_of_month:
            slash_day = self.day_of_month.split('/')
        else:
            slash_day[0] = self.day_of_month

        if '/' in self.month:
            slash_month = self.month.split('/')
        else:
            slash_month[0] = self.month

        if slash_day[0] != '*' and slash_month[0] != '*':

            if ',' in slash_day[0]:
                all_days_of_month = slash_day[0].split(',')
                max_value.append(all_days_of_month[-1])
                separator = ','
            elif '-' in slash_day[0]:
                day_of_month = slash_day[0].split('-')
                all_days_of_month = range(int(day_of_month[0]),
                                          int(day_of_month[-1]) + 1)
                max_value.append(all_days_of_month[-1])
                separator = '-'
            else:
                all_days_of_month = [slash_day[0]]
                separator = '!'

            if ',' in slash_month[0]:
                all_month = slash_month[0].split(',')
            elif '-' in slash_month[0]:
                month = slash_month[0].split('-')
                all_month = range(int(month[0]), int(month[-1]) + 1)
            else:
                all_month = [slash_month[0]]

            for month in all_month:
                for day in all_days_of_month:
                    try:
                        if datetime(date.today().year, int(month), int(day)):
                            pass
                    except ValueError as error:
                        if str(error) == 'day is out of range for month':
                            print 'day is out of range for month'
                            if 2 in all_month or '2' in all_month:
                                max_value.append(28)
                            else:
                                max_value.append(30)

            if max_value:
                max_value = str(min(max_value))
            else:
                max_value = '31'

            new_day_of_month = []
            if separator == ',':
                for day in all_days_of_month:
                    if day <= max_value:
                        new_day_of_month.append(day)
                new_days = separator.join(new_day_of_month)
            elif separator == '-':
                if day_of_month[0] == max_value:
                    day_of_month = [max_value]
                else:
                    day_of_month[1] = max_value
                new_days = separator.join(day_of_month)
            else:
                if int(all_days_of_month[0]) > int(max_value):
                    new_days =  max_value
                else:
                    new_days = all_days_of_month[0]

            slash_day[0] = new_days       

        if slash_day[1]:
            day_of_month = '/'.join(slash_day)
        else:
            day_of_month = slash_day[0]
        return day_of_month

    def __check_day_of_the_week(self, day_of_week):
        week_days = {'mon': '1', 'tue': '2', 'wed': '3', 'thu': '4',
                     'fri': '5', 'sat': '6', 'sun': '0'}
        slash = [0, 0]
        if '/' in day_of_week:
            slash = day_of_week.split('/')
            if int(slash[1]) not in range (1, 8):
                print "Wrong using of '/' for day_of_week"
                slash[1] = 0
        else:
            slash[0] = day_of_week 

        if ',' in slash[0]:
            slash[0] = slash[0].split(',')
            separator = ','
        elif '-' in slash[0]:
            slash[0] = slash[0].split('-')
            separator = '-'
        elif slash[0] == '*':
            if slash[1]:
                return day_of_week
            else:
                return '*'
        else:
            if slash[1]:
                print "Wrong using of '/' for day_of_week"
                slash[1] = 0
            separator = None        

        if isinstance(slash[0], list):
            for unit in slash[0]:
                if unit not in week_days and unit not in week_days.values():
                    print 'day_of_week not in range'
                    slash[0] = '*'
                    # return day_of_week
        else:
            if slash[0] not in week_days and slash[0] not in week_days.values():
                print 'day_of_week not in range'
                slash[0] = '7'

        if separator == ',':
            slash[0] = sorted(set(slash[0]))
            slash[0] = separator.join(slash[0])
        elif separator == '-':
            slash[0] = separator.join(slash[0])
            
        if slash[1]:
            day_of_week = '/'.join(slash)
        else:
            day_of_week = slash[0]
        return day_of_week

    def output(self):
        if self.reboot:
            return '@reboot ' + self.action
        return str(self.minute) + ' ' + str(self.hour) + ' ' \
               + str(self.__check_date()) + ' ' + str(self.month) + ' ' \
               + str(self.day_of_week) + ' ' + self.action

    def __check_month(self, month):
        slash = [0, 0]
        if '/' in month:
            slash = month.split('/')
            if int(slash[1]) not in range (1, 13):
                print "Wrong using of '/' for month"
                slash[1] = 0
        else:
            slash[0] = month  

        if ',' in slash[0]:
            slash[0] = slash[0].split(',')
            separator = ','
        elif '-' in slash[0]:
            slash[0] = slash[0].split('-')
            separator = '-'
        elif slash[0] == '*':
            if slash[1]:
                return month
            else:
                return '*'
        else:
            if slash[1]:
                print "Wrong using of '/' for month"
                slash[1] = 0
            separator = None

        if isinstance(slash[0], list):
            for unit in slash[0]:
                if int(unit) not in range(1, 13):
                    print 'month not in range'
                    if separator == ',':
                        slash[0][slash[0].index(unit)] = '12'
                    elif separator == '-':
                        slash[0][slash[0].index(unit)] = '12'
                        slash[0] = slash[0][:slash[0].index('12') + 1]
                        #slash[0] = separator.join(slash[0])
        else:
            if int(slash[0]) not in range(1, 13):
                print 'month not in range'
                slash[0] = '0'

        if separator == ',':
            slash[0] = sorted(set(slash[0]))
            slash[0] = separator.join(slash[0])
        elif separator == '-':
            slash[0] = separator.join(slash[0])
            
        if slash[1]:
            month = '/'.join(slash)
        else:
            month = slash[0]
        return month

    def __check_day_of_month(self, day_of_month):
        slash = [0, 0]
        if '/' in day_of_month:
            slash = day_of_month.split('/')
            if int(slash[1]) not in range (1, 16):
                print "Wrong using of '/' for day_of_month"
                slash[1] = 0
        else:
            slash[0] = day_of_month  
        print 'slash =', slash 
        if ',' in slash[0]:
            slash[0] = slash[0].split(',')
            separator = ','
        elif '-' in slash[0]:
            slash[0] = slash[0].split('-')
            separator = '-'
        elif slash[0] == '*':
            if slash[1]:
                return day_of_month
            else:
                return '*'
        else:
            if slash[1]:
                print "Wrong using of '/' for day_of_month"
                slash[1] = 0
            separator = None

        if isinstance(slash[0], list):
            for unit in slash[0]:
                if int(unit) not in range(1, 32):
                    print 'day_of_month not in range'
                    if separator == ',':
                        slash[0][slash[0].index(unit)] = '31'
                    elif separator == '-':
                        slash[0][slash[0].index(unit)] = '31'
                        slash[0] = slash[0][:slash[0].index('31')+1]
                        # day_of_month = separator.join(day_of_month)
        else:
            if int(slash[0]) not in range(1, 32):
                print 'day_of_month not in range'
                slash[0] = '*'

        if separator == ',':
            slash[0] = sorted(set(slash[0]))
            slash[0] = separator.join(slash[0])
        elif separator == '-':
            slash[0] = separator.join(slash[0])
            
        if slash[1]:
            day_of_month = '/'.join(slash)
        else:
            day_of_month = slash[0]
        return day_of_month


example = Task('1', '1', '10,22/2', '1-13', 'mon', 'burn!')
print example.output()

