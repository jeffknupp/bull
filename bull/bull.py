"""Bull is a library used to sell digital products on your website. It's meant
to be run on the same domain as your sales page, making analytics tracking
trivially easy.

"""

import datetime
import sys
import uuid

from jinja2 import Environment, PackageLoader
from flask import (Flask, send_from_directory, abort, redirect, request,
                   render_template)
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail, Message
import stripe

from . import app

stripe.api_key = app.config['STRIPE_SECRET_KEY']

db = SQLAlchemy(app)
mail = Mail(app)
env = Environment(loader=PackageLoader('bull', 'templates'))

class Product(db.Model):
    """A digital product for sale on our site.

    :param int id: Unique id for this product
    :param str name: Human-readable name of this product
    :param str file_name: Path to file this digital product represents
    :param str version: Optional version to track updates to products
    :param bool is_active: Used to denote if a product should be considered
                          for-sale
    :param float price: Price of product
    """
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    file_name = db.Column(db.String)
    version = db.Column(db.String, default=None, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=True)
    price = db.Column(db.Float)

    def __str__(self):
        """Return the string representation of a product."""
        return '{} (v{})'.format(self.name, self.version)

class Purchase(db.Model):
    """Contains information about the sale of a product.

    :param str uuid: Unique ID (and URL) generated for the customer unique to
                     this purchase
    :param str email: Customer's email address
    :param int product_id: ID of the product associated with this sale
    :param :class:`SQLAlchemy.relationship` product: The associated product
    :param downloads_left int: Number of downloads remaining using this URL
    """
    __tablename__ = 'purchase'
    uuid = db.Column(db.String, primary_key=True)
    email = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship(Product)
    downloads_left = db.Column(db.Integer, default=5)
    sold_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __str__(self):
        """Return the string representation of the purchase."""
        return '{} bought by {}'.format(self.product.name, self.email)

@app.route('/<uuid>')
def download_file(uuid):
    """Serve the file associated with the purchase whose ID is *uuid*.

    :param str uuid: Primary key of the purchase whose file we need to serve

    """
    purchase = Purchase.query.get(uuid)
    if purchase:
        purchase.downloads_left -= 1
        if purchase.downloads_left <= 0:
            return render_template('downloads_exceeded.html')
        db.session.commit()
        return send_from_directory(directory=app.config['FILE_DIRECTORY'],
                filename=purchase.product.file_name, as_attachment=True)
    else:
        abort(404)
    
@app.route('/buy', methods=['POST'])
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
    except stripe.CardError, e:
        return render_template('charge_error.html')

    app.logger.info(charge)

    purchase = Purchase(uuid=str(uuid.uuid4()),
            email=email,
            product=product)
    db.session.add(purchase)
    db.session.commit()

    mail_template = env.get_template('email.html')
    mail_html = mail_template.render(purchase=purchase, product=product)

    message = Message(
            html=mail_html,
            subject=app.config['MAIL_SUBJECT'],
            sender=app.config['MAIL_FROM'],
            recipients=[email])

    with mail.connect() as conn:
        conn.send(message)

    return render_template('success.html', url=purchase.uuid)

@app.route('/test/<product_id>')
def test(product_id):
    """Return a test page for live testing the "purchase" button."""
    test_product = Product.query.get(product_id)
    return render_template(
            'test.html', 
            test_product=test_product, 
            stripe_key=app.config['STRIPE_PUBLIC_KEY'],
            site_name=app.config['SITE_NAME'])

if __name__ == '__main__':
    sys.exit(app.run(debug=True))
