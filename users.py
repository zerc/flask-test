# coding: utf-8
import hashlib
from functools import wraps
import simplejson as json

from flask import render_template, request, url_for, flash
from flask.ext.wtf import Form
from wtforms import TextField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.orm import model_form
from werkzeug.wrappers import BaseResponse

from project import app, db


# Models
class User(db.Model):
    pk = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80))

    def __init__(self, name, password):
        self.name = name
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name


# Forms
# RegisterUserForm = model_form(User, base_class=Form)
class RegisterUserForm(Form):
    name = TextField('name', validators=[DataRequired()])
    password = TextField('password', validators=[DataRequired()])


# Helpers
def user_to_json(user):
    if not isinstance(user, User):
        raise TypeError

    return {f: getattr(user, f) for f in ('name', 'pk')}


def users_as_json(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        ctx = f(*args, **kwargs)

        if request.is_xhr:
            return json.dumps(ctx, default=user_to_json)

        return json.dumps({'message': 'Not ajax'}), 403

    return wrapper


def render_as_html(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            ctx = f(*args, **kwargs) or {}

            if isinstance(ctx, BaseResponse):
                return ctx

            template_name = template or f.__name__ + '.html'
            return render_template(template_name, **ctx)
        return decorated_function
    return decorator


def prepare_user_form_data(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        data = request.form.copy()

        try:
            pswd = data['password']
            if pswd:
                data['password'] = hashlib.sha256(pswd).hexdigest()
        except KeyError:
            pass

        request.form = data

        return f()
    return decorated_function


# Views
@app.route('/', methods=('POST', 'GET'))
@render_as_html()
@prepare_user_form_data
def index():
    form = RegisterUserForm()
    if form.validate_on_submit():
        print form.data
        # user = User(**form.data)
        # db.session.add(user)
        # db.session.commit()
        flash('You registered!')
        form = RegisterUserForm(None)

    return {'form': form}


@app.route('/users/', methods=('GET',))
@users_as_json
def users():
    return User.query.all()
