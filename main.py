import subprocess
import sys
import os
import socket
from db_connect import get_cron_list, db_add
from task_model import Task
from config import TEMP_FILE
from pprint import pprint


def run_command(cmd):
    """Runs the console command and returns a list of resulting lines from
     STDOUT.
    """
    stdout = []
    try:
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
    except Exception as e:
        print 'Error executing "{}".\nDetails: {}'.format(cmd, e)
    else:
        while True:
            line = p.stdout.readline().strip()
            if line:
                stdout.append(line)
            if line == '' and p.poll() is not None:
                break
    return stdout


def text_to_cron_object(text):

    if text.startswith('@yearly') or text.startswith('@annually'):
        text = text.replace('@yearly', '0 0 1 1 *', 1)
        text = text.replace('@annually', '0 0 1 1 *', 1)

    elif text.startswith('@monthly'):
        text = text.replace('@monthly', '0 0 1 * *', 1)

    elif text.startswith('@weekly'):
        text = text.replace('@weekly', '0 0 * * 0', 1)

    elif text.startswith('@daily') or text.startswith('@midnight'):
        text = text.replace('@daily', '0 0 * * *', 1)
        text = text.replace('@midnight', '0 0 * * *', 1)

    elif text.startswith('@hourly'):
        text = text.replace('@hourly', '0 * * * *', 1)

    cron = text.split()
    if cron[0] == '@reboot':
        t = Task(action=' '.join(cron[1:]), reboot=True)
    else:
        try:
            t = Task(minute=cron[0],
                     hour=cron[1],
                     day_of_month=cron[2],
                     month=cron[3],
                     day_of_week=cron[4],
                     action=' '.join(cron[5:]))
        except Exception as e:
            print "{} is not a valid cron entry.\nDetails: {}".format(text, e)
            return e

    return t


def read_crontab(from_file=False):
    if from_file:
        cron_list = [l.strip() for l in open(TEMP_FILE, 'rb').readlines()]
    else:
        cron_list = run_command('crontab -l')

    if cron_list:
        cron_list = [c for c in cron_list if not c.startswith('#')]
        res = []
        for line in cron_list:
            cron = text_to_cron_object(line)
            res.append(cron)

        return res


def create_crontab_file():
    cron_list = [cron.output() for cron in get_cron_list()]
    f = open(TEMP_FILE, 'wb+')
    for line in cron_list:
        f.write(line + '\n')
    f.close()


def write_crontab(file=TEMP_FILE):
    try:
        run_command('crontab {}'.format(file))
    except Exception as e:
        print 'An error occurred while updating crontab.\nDetails: ', e
    else:
        print 'Crontab has been successfully updated.'


def get_sys_info():
    host = socket.gethostname()
    user = os.getlogin()
    sys_info = os.uname()
    return ("{} {} ({})</br>{}".format(sys_info[0], sys_info[4], sys_info[2], sys_info[3]),
            "{}@{}".format(user, host))


def main():
    """This is an ugly temporary function until the web UI is in place.
    """

    print "\nSelect option:\n1 - Read crontab\n2 - Add new cron to DB and temp" \
          "file\n3 - Update system crontab from temp file"
    ans = raw_input('Enter your choice: ')

    if ans == '1':
        cron_list = read_crontab()
        cron_db_list = get_cron_list()
        cron_file_list = read_crontab(from_file=True)

        if cron_list:
            print "\nSystem crontab contents:"
            for cron in cron_list:
                print cron.output()
        else:
            print "\nSystem crontab is empty"

        if cron_db_list:
            print "DB contents:"
            for cron in cron_db_list:
                print cron.output()
        else:
            print 'DB is empty'

        if cron_file_list:
            print "Temp file contents:"
            for cron in cron_file_list:
                print cron.output()
        else:
            print 'Temp file is empty'

    elif ans == '2':
        raw_cron = raw_input("Enter a proper cron (there's no validation): ")
        cron = text_to_cron_object(raw_cron)
        if cron:
            print 'Cron seems fine.'
            db_add(cron)
            create_crontab_file()
            out = run_command('cat {}'.format(TEMP_FILE))
            print 'Updated crontab file:\n', '\n'.join(out)

    elif ans == '3':
        write_crontab()

    elif ans.lower() == 'q':
        print 'Bye.'
        sys.exit(0)


if __name__ == '__main__':
    main()
