"""Tests for the Bull digital goods sales application."""

import datetime
import unittest
import uuid
import os

from flask import current_app
from flask.ext.login import LoginManager, login_required, login_user

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
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['FILE_DIRECTORY'] = os.path.abspath(os.path.join(os.path.split(os.path.abspath(__file__))[0], 'files'))
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
                    uuid=self.purchase_uuid,
                    sold_at=datetime.datetime(2014, 1, 1, 12, 12, 12))
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
        """Can we retrieve the User instance created in setUp?"""
        with app.app_context():
            user = User.query.get('admin@foo.com')
            assert bcrypt.check_password_hash(user.password, 'password')

    def test_get_product(self):
        """Can we retrieve the Product instance created in setUp?"""
        with app.app_context():
            product = Product.query.get(1)
            assert product is not None
            assert product.name == 'Test Product'

    def test_get_purchase(self):
        """Can we retrieve the Purchase instance created in setUp?"""
        with app.app_context():
            purchase = Purchase.query.get(self.purchase_uuid)
            assert purchase is not None
            assert purchase.product.price == 5.01
            assert purchase.email == 'foo@bar.com'

    def test_download_file(self):
        """Given an exisitng purchase, does visiting the purchase's url allow us
        to download the file?."""
        purchase_url = '/' + self.purchase_uuid
        response = self.app.get(purchase_url)
        assert response.data == 'Test content\n'
        assert response.status_code == 200

    def test_product_no_version_as_string(self):
        """Is the string representation of the Product model what we expect?"""
        with app.app_context():
            product = Product.query.get(1)
            assert str(product) == 'Test Product'

    def test_product_with_version_as_string(self):
        """Is the string representation of the Product model what we expect?"""
        with app.app_context():
            product = Product.query.get(1)
            product.version = '1.0'
            assert str(product) == 'Test Product (v1.0)'

    def test_get_purchase_date(self):
        """Can we retrieve the date of the Purchase instance created in setUp?"""
        with app.app_context():
            purchase = Purchase.query.get(self.purchase_uuid)
            assert purchase.sell_date() == datetime.datetime(2014, 1, 1).date()

    def test_get_purchase_string(self):
        """Is the string representation of the Purchase model what we expect?"""
        with app.app_context():
            purchase = Purchase.query.get(self.purchase_uuid)
            assert str(purchase) == 'Test Product bought by foo@bar.com'

    def login(self, username, password):
        """Login user."""
        return self.app.post(
                '/login', 
                data={'email': username, 'password': password},
                follow_redirects=True
                )

    def test_user_authentication(self):
        """Do the authencation methods for the User model work as expected?"""
        with app.app_context():
            user = User.query.get('admin@foo.com')
            response = self.app.get('/reports')
            assert response.status_code == 401
            assert self.login(user.email, 'password').status_code == 200
            response = self.app.get('/reports')
            assert response.status_code == 200
            assert 'drawSalesChart' in response.data
            response = self.app.get('/logout')
            assert response.status_code == 200
            response = self.app.get('/reports')
            assert response.status_code == 401
