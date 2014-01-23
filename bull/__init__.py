"""Bull library, used for selling digital goods."""

import os
from flask import Flask
from jinja2 import Environment, FileSystemLoader, ChoiceLoader, PackageLoader
import stripe
from .bull import bull, mail
from .models import Product, Purchase, db

app = Flask(__name__)
app.config.from_object('config')
app.jinja_loader = ChoiceLoader([
    FileSystemLoader(os.path.join(os.getcwd(), 'templates')),
    PackageLoader('bull'),
    ])
stripe.api_key = app.config['STRIPE_SECRET_KEY']
db.init_app(app)
mail.init_app(app)
app.register_blueprint(bull)

__version__ = '0.0.1'
