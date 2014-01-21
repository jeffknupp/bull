"""Bull is a library used to sell digital products on your website. It's meant
to be run on the same domain as your sales page, making analytics tracking
trivially easy.

"""

import datetime
import sys
import uuid

from jinja2 import Environment, PackageLoader
from flask import (Blueprint, send_from_directory, abort, redirect, request,
                   render_template)
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail, Message
import stripe

from .models import Product, Purchase, db

bull = Blueprint('bull', __name__)
env = Environment(loader=PackageLoader('bull', 'templates'))
mail = Mail()

@bull.route('/<uuid>')
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

@bull.route('/test/<product_id>')
def test(product_id):
    """Return a test page for live testing the "purchase" button."""
    test_product = Product.query.get(product_id)
    return render_template(
            'test.html', 
            test_product=test_product)

if __name__ == '__main__':
    sys.exit(app.run(debug=True))
