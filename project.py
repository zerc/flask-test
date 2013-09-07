#!venv/bin/python
# coding: utf-8
import os
import hashlib
from flask import Flask, Request
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import cached_property


DIRNAME = os.path.dirname(__name__)

sqlite_db_path = os.path.join(DIRNAME, 'flask-test.db')

app = Flask(__name__)

app.config.update({
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///%s' % sqlite_db_path,
    'SECRET_KEY': '2dasd2dd44fas',
})

db = SQLAlchemy(app)
