"""Settings for bull installation."""
from os.path import abspath, dirname, join

_cwd = dirname(abspath(__file__))
# Subject of the email sent after purchase 
# MAIL_SUBJECT = 

# Email address for the 'from' field of the generated email
# MAIL_FROM = 

# Email server address
# MAIL_SERVER = 

# Email server username
# MAIL_USERNAME = 

# Email server password
# MAIL_PASSWORD = 

# Email server port
# MAIL_PORT = 

# Use SSL for email? 
# MAIL_USE_SSL = 

# Website address, for use in Stripe purchases and in email
# SITE_ADDRESS = 

# Database URI for SQLAlchmey (Default: 'sqlite+pysqlite3:///sqlite3.db')
# SQLALCHEMY_DATABASE_URI = 'sqlite+pysqlite:///sqlite3.db'

# Stripe secret key to be used to process purchases
STRIPE_SECRET_KEY = 'foo'

# Stripe public key to be used to process purchases
STRIPE_PUBLIC_KEY = 'bar'
