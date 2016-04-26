from config import CONNECTION_STRING
import pymongo
from bson.objectid import ObjectId
from task_model import Task


def get_connection(conn_string):
    return pymongo.MongoClient(conn_string)


def get_db(conn, db_name):
    return conn[db_name]


def get_collection(db, collection_name):
    return db[collection_name]


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
        collection.insert_one(data)
    except Exception as e:
        print 'Unable to create DB entry.\nError:', e


def db_delete(_id):
    collection.remove({'_id': ObjectId(_id)})


db = get_db(get_connection(CONNECTION_STRING), 'test')
collection = get_collection(db, 'cron-manager')
