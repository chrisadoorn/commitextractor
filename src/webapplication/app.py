import os

from flask import Flask

POSTGRESQL = 'postgresql'
CONFIGFILE = 'config.ini'
APP_DIR = os.path.dirname(os.path.realpath(__file__))


app = Flask(__name__)
app.config.from_object(__name__)


# Here I would set up the cache, a task queue, etc.
