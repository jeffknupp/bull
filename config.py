"""Settings for bull installation."""
from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))

# Directory containing your products
FILE_DIRECTORY = dirname(abspath(__file__)) + '/files'

# Subject of the email sent after purchase 
MAIL_SUBJECT = 'Thanks for the purchase'

# Email address for the 'from' field of the generated email
MAIL_FROM = 'jeff@jeffknupp.com'

# Email server address
MAIL_SERVER = 'smtp.gmail.com'

# Email server username
MAIL_USERNAME = 'jeff@jeffknupp.com'

# Email server password
MAIL_PASSWORD = 'lissrose3'

# Email server port
MAIL_PORT = 465

# Use SSL for email? 
MAIL_USE_SSL = True

# Website name, for use in Stripe purchases
SITE_NAME = 'Foo.com'

# Database URI for SQLAlchmey (Default: 'sqlite+pysqlite3:///sqlite3.db')
SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///sqlite3.db'

# Stripe secret key to be used to process purchases
STRIPE_SECRET_KEY = 'sk_test_VXxFQI4v3Ym2EwnXh79mzDoN'

# Stripe public key to be used to process purchases
STRIPE_PUBLIC_KEY = 'pk_test_w3qNBkDR8A4jkKejBmsMdH34'
