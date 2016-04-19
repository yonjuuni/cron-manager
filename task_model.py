class Task(object):

    def __init__(self, minute, hour, day_of_month, month, day_of_week, action):
        
        self.minute = minute
        self.hour = hour
        self.day_of_month = day_of_month
        self.month = month
        self.day_of_week = day_of_week
        self.action = action
        self._id = None
        

    def output(self):

        if self.minute in range(0, 60) or self.minute == '*':
            if self.hour in range(0, 24) or self.hour == '*':
                if self.day_of_month in range(1, 32) or self.day_of_month == '*':
                    if self.month in range(1, 13) or self.month == '*':
                        if self.day_of_week in range(1, 8) or self.day_of_week == '*':
                            if self.action:  
                                command = str(self.minute) + ' ' + str(self.hour) + ' ' \
                                    + str(self.day_of_month) + ' ' + str(self.month) + ' ' \
                                    + str(self.day_of_week) + ' ' + self.action
                                return command
                            else:
                                print 'write action'
                        else:
                            print 'wrong day of week'
                    else:
                        print 'wrong month'
                else:
                    print 'wrong day of month'
            else:
                print 'wrong hour'
        else:
            print 'wrong minute'


example = Task(10, '*', 30, 12, 7, 'burn!')
print example.output()







