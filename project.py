#!venv/bin/python
# coding: utf-8
import os
import hashlib
from flask import Flask, Request
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.datastructures import ImmutableMultiDict
from werkzeug.utils import cached_property


class CustomRequest(Request):
    """
    We like are hard ways :D
    """
    @cached_property
    def form(self):
        data = dict(super(Request, self).form)
        try:
            pswd = data['password'].pop()
            if pswd:
                data['password'] = hashlib.sha256(pswd).hexdigest()
        except KeyError:
            pass
        return ImmutableMultiDict(data)


DIRNAME = os.path.dirname(__name__)

sqlite_db_path = os.path.join(DIRNAME, 'flask-test.db')

app = Flask(__name__)
app.request_class = CustomRequest

app.config.update({
    'DEBUG': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite:///%s' % sqlite_db_path,
    'SECRET_KEY': '2dasd2dd44fas',
})

db = SQLAlchemy(app)
