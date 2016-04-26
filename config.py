import os
from base64 import b64encode

CONNECTION_STRING = "localhost:27017"
TEMP_FILE = '.temp_crontab'


SECRET_KEY = ""
basedir = os.path.abspath(os.path.dirname(__file__))
secret_file = os.path.join(basedir, '.secret')
if os.path.exists(secret_file):
    # Read SECRET_KEY from .secret file
    f = open(secret_file, 'rb')
    SECRET_KEY = b64encode(f.read().strip()).decode()
    f.close()
else:
    # Generate SECRET_KEY & save it away
    temp = os.urandom(24)
    f = open(secret_file, 'wb')
    f.write(temp)
    f.close()
    SECRET_KEY = b64encode(temp).decode()
    # Modify .gitignore to include .secret file
    gitignore_file = os.path.join(basedir, '.gitignore')
    f = open(gitignore_file, 'a+')
    if '.secret' not in f.readlines() and '.secret\n' not in f.readlines():
        f.write('.secret\n')
    f.close()


DEBUG = True  # set it to False on production
