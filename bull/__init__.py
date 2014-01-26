"""Bull library, used for selling digital goods."""

import os

from flask import Flask
from flaskext.bcrypt import Bcrypt
from jinja2 import Environment, FileSystemLoader, ChoiceLoader, PackageLoader
import stripe

from .bull import bull, mail, login_manager
from .models import Product, Purchase, db


app = Flask(__name__)
app.config['SECRET_KEY'] = 'foo'
app.config['WTF_CSRF_KEY'] = 'foo'
app.config.from_object('config')
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(os.getcwd(), 'templates')),
    PackageLoader('bull'),
    ])
stripe.api_key = app.config['STRIPE_SECRET_KEY']
db.init_app(app)
mail.init_app(app)
bcrypt = Bcrypt(app)
login_manager.init_app(app)
app.register_blueprint(bull)

__version__ = '0.2.0'
