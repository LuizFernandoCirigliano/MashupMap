import os

basedir = os.path.abspath(os.path.dirname(__file__))

SECRET_KEY = os.getenv('FLASK_SECRET', 'VERY_ASASD')

SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    'sqlite:///' + os.path.join(basedir, 'app.db')
)

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

PRODUCTION = os.getenv('PRODUCTION', False)
