"""Bull is a library used to sell digital products on your website. It's meant
to be run on the same domain as your sales page, making analytics tracking
trivially easy.

"""

import logging
import sys
import uuid

from flask import (Blueprint, send_from_directory, abort, request,
                   render_template, current_app, render_template, redirect,
                   url_for)
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_required, login_user
from flask.ext.mail import Mail, Message
from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired
import stripe

from .models import Product, Purchase, User, db

logger = logging.getLogger(__name__)
bull = Blueprint('bull', __name__)
mail = Mail()
login_manager = LoginManager()

class LoginForm(Form):
    email = TextField('name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()]) 

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return User.query.get(user_id)

@bull.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.get(form.email.data)
        login_user(user, remember=True)
        
        return redirect(url_for("bull.reports"))
    return render_template("login.html", form=form)

@bull.route('/<purchase_uuid>')
def download_file(purchase_uuid):
    """Serve the file associated with the purchase whose ID is *purchase_uuid*.

    :param str purchase_uuid: Primary key of the purchase whose file we need
                              to serve

    """
    purchase = Purchase.query.get(purchase_uuid)
    if purchase:
        purchase.downloads_left -= 1
        if purchase.downloads_left <= 0:
            return render_template('downloads_exceeded.html')
        db.session.commit()
        return send_from_directory(
                directory=current_app.config['FILE_DIRECTORY'],
                filename=purchase.product.file_name,
                as_attachment=True)
    else:
        abort(404)


@bull.route('/buy', methods=['POST'])
def buy():
    """Facilitate the purchase of a product."""

    stripe_token = request.form['stripeToken']
    email = request.form['stripeEmail']
    product_id = request.form['product_id']

    product = Product.query.get(product_id)
    try:
        charge = stripe.Charge.create(
                amount=int(product.price * 100),
                currency='usd',
                card=stripe_token,
                description=email)
    except stripe.CardError:
        return render_template('charge_error.html')

    current_app.logger.info(charge)

    purchase = Purchase(uuid=str(uuid.uuid4()),
            email=email,
            product=product)
    db.session.add(purchase)
    db.session.commit()

    mail_html = render_template(
            'email.html',
            url=purchase.uuid,
            )

    message = Message(
            html=mail_html,
            subject=current_app.config['MAIL_SUBJECT'],
            sender=current_app.config['MAIL_FROM'],
            recipients=[email])

    with mail.connect() as conn:
        conn.send(message)

    return render_template('success.html', url=str(purchase.uuid))

@bull.route('/reports')
@login_required
def reports():
    """Run and display various analytics reports."""
    products = Product.query.all()
    purchases = Purchase.query.all()
    purchases_by_day = dict()
    for purchase in purchases:
        purchase_date = purchase.sold_at.date().strftime('%m-%d')
        if purchase_date not in purchases_by_day:
            purchases_by_day[purchase_date] = {'units': 0, 'sales': 0.0}
        purchases_by_day[purchase_date]['units'] += 1
        purchases_by_day[purchase_date]['sales'] += purchase.product.price
    purchase_days = sorted(purchases_by_day.keys())
    units = len(purchases)
    total_sales = sum([p.product.price for p in purchases])

    return render_template(
            'reports.html',
            products=products,
            purchase_days=purchase_days,
            purchases=purchases,
            purchases_by_day=purchases_by_day,
            units=units,
            total_sales=total_sales)

@bull.route('/test/<product_id>')
def test(product_id):
    """Return a test page for live testing the "purchase" button."""
    test_product = Product.query.get(product_id)
    return render_template(
            'test.html',
            test_product=test_product)
