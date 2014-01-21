"""Bull library, used for selling digital goods."""

from flask import Flask
import stripe
from .bull import bull, mail
from .models import Product, Purchase, db

app = Flask(__name__)
app.config.from_object('config')
stripe.api_key = app.config['STRIPE_SECRET_KEY']
db.init_app(app)
mail.init_app(app)
app.register_blueprint(bull)

__version__ = '0.0.1'
