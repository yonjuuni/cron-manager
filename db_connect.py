from config import collection
from bson.objectid import ObjectId
from task_model import Task


def get_cron_list():
    cursor = collection.find()
    if cursor:
        res = []
        for cron in list(cursor):
            if cron.get('action'):
                if cron.get('reboot'):
                    res.append(Task(action=cron['action'],
                                    reboot=True,
                                    _id=cron['_id']))
                else:
                    res.append(Task(cron['minute'],
                                    cron['hour'],
                                    cron['day_of_month'],
                                    cron['month'],
                                    cron['day_of_week'],
                                    cron['action'],
                                    cron['_id']))
        return res


def db_update(cron):
    if cron.reboot:
        data = {'reboot': True,
                'action': cron.action
                }
    else:
        data = {'minute': cron.minute,
                'hour': cron.hour,
                'day_of_month': cron.day_of_month,
                'month': cron.month,
                'day_of_week': cron.day_of_week,
                'action': cron.action
                }

    try:
        collection.update({'_id': cron._id}, data)
    except Exception as e:
        print 'Unable to update DB entry.\nError:', e


def db_add(cron):
    data = {'minute': cron.minute,
            'hour': cron.hour,
            'day_of_month': cron.day_of_month,
            'month': cron.month,
            'day_of_week': cron.day_of_week,
            'action': cron.action
            }

    try:
        collection.insert_one(data)
    except Exception as e:
        print 'Unable to create DB entry.\nError:', e


def db_delete(cron):
    collection.remove({'_id': cron._id})
