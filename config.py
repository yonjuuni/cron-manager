import pymongo

CONNECTION_STRING = "localhost:27017"


def get_connection():
    return pymongo.MongoClient(CONNECTION_STRING)


def get_db(conn, db_name):
    return conn[db_name]


def get_collection(db, collection_name):
    return db[collection_name]

db = get_db(get_connection(), 'test')
collection = get_collection(db, 'cron-manager')
