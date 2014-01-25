"""Tests for the Bull digital goods sales application."""

import unittest
import uuid

from flask import current_app

from bull import app, mail, bcrypt
from bull.models import db, User, Product, Purchase
class BullTestCase(unittest.TestCase):
    """Main test cases for Bull."""

    def setUp(self):
        """Pre-test activities."""
        app.testing = True
        app.config['STRIPE_SECRET_KEY'] = 'foo'
        app.config['STRIPE_PUBLIC_KEY'] = 'bar'
        app.config['SITE_NAME'] = 'www.foo.com'
        app.config['STRIPE_SECRET_KEY'] = 'foo'
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with app.app_context():
            db.init_app(current_app)
            db.metadata.create_all(db.engine)
            mail.init_app(current_app)
            bcrypt.init_app(current_app)
            self.db = db
            self.app = app.test_client()
            self.purchase_uuid = str(uuid.uuid4())
            product = Product(
                name='Test Product',
                file_name='test.txt',
                price=5.01)
            purchase = Purchase(product=product,
                    email='foo@bar.com',
                    uuid=self.purchase_uuid)
            user = User(email='admin@foo.com',
                    password=bcrypt.generate_password_hash('password'))
            db.session.add(product)
            db.session.add(purchase)
            db.session.add(user)
            db.session.commit()


    def test_get_test(self):
        """Does hitting the /test endpoint return the proper HTTP code?"""
        response = self.app.get('/test/1')
        assert response.status_code == 200
        assert app.config['STRIPE_PUBLIC_KEY'] in response.data

    def test_get_user(self):
        with app.app_context():
            user = User.query.get('admin@foo.com')
            assert bcrypt.check_password_hash(user.password, 'password')

    def test_get_product(self):
        with app.app_context():
            product = Product.query.get(1)
            assert product is not None
            assert product.name == 'Test Product'

    def test_get_purchase(self):
        with app.app_context():
            purchase = Purchase.query.get(self.purchase_uuid)
            assert purchase is not None
            assert purchase.product.price == 5.01
            assert purchase.email == 'foo@bar.com'
