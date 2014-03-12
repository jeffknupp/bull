"""Create a free copy of the book for the given version and email address."""
import uuid
import sys

from bull import app
app.config['STRIPE_SECRET_KEY'] = None
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///sqlite3.db'
from bull.models import Product, Purchase, db

NAME_MAP = {'pdf2': 1, 'pdf3': 2, 'epub3': 3, 'epub2': 4, 'bundle': 5}

with app.app_context():
    session = db.session()
    book = session.query(Product).get(NAME_MAP[sys.argv[1]])
    purchase = Purchase(
        uuid=str(uuid.uuid4()),
        email=sys.argv[2],
        product_id=book.id
        )
    session.add(purchase)
    session.commit()
    print 'link is https://buy.jeffknupp.com/{}'.format(purchase.uuid)

#with app.app_context():
#    session = db.session()
#    db.metadata.create_all(db.engine)
#    session.add(pdf2)
#    session.add(pdf3)
#    session.add(epub2)
#    session.add(epub3)
#    session.add(bundle)
#    session.add(purchase)
#    session.commit()
