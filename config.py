import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP="app.py"
    FLASK_DEBUG=1
    FLASK_ENV='development'
    SECRET_KEY='secret_key'
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND")
    DATABASE_URL = os.environ.get("DATABASE_URL")