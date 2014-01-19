"""Bull library, used for selling digital goods."""

from flask import Flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///sqlite3.db'
app.config['FILE_DIRECTORY'] = 'files'

__version__ = '0.0.1'
