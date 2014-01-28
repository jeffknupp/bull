import uuid

from bull import app
app.config['STRIPE_SECRET_KEY'] = None
from bull.models import Product, Purchase, db

pdf2 = Product(
    id=1,
    name='Writing Idiomatic Python 2.7 PDF',
    file_name='writing_idiomatic_python_2.pdf',
    version='1.5',
    is_active=True,
    price=9.99)

pdf3 = Product(
    id=2,
    name='Writing Idiomatic Python 3 PDF',
    file_name='writing_idiomatic_python_3.pdf',
    version='1.5',
    is_active=True,
    price=9.99)

epub2 = Product(
    id=3,
    name='Writing Idiomatic Python 2.7 ePub',
    file_name='writing_idiomatic_python_2.epub',
    version='1.5',
    is_active=True,
    price=9.99)

epub3 = Product(
    id=4,
    name='Writing Idiomatic Python 2.7 ePub',
    file_name='writing_idiomatic_python_3.epub',
    version='1.5',
    is_active=True,
    price=9.99)

bundle = Product(
    id=5,
    name='Writing Idiomatic Python Bundle',
    file_name='writing_idiomatic_python.zip',
    version='1.5',
    is_active=True,
    price=14.99)

purchase = Purchase(
    uuid=str(uuid.uuid4()),
    email="jeff@jeffknupp.com",
    product_id=pdf3.id,
    )

with app.app_context():
    session = db.session()
    db.metadata.create_all(db.engine)
    session.add(pdf2)
    session.add(pdf3)
    session.add(epub2)
    session.add(epub3)
    session.add(bundle)
    session.add(purchase)
    session.commit()
