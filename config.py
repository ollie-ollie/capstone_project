import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(32)


class Production(Config):
    ENV = 'production'
    DEBUG = False
    TESTING = False


class Development(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = False


class Testing(Config):
    # the testing config is supposed to run locally
    ENV = 'testing'
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    TEST_DB_NAME = os.getenv('TEST_DB_NAME')
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.\
        format(DB_USER, DB_PASSWORD, DB_HOST, TEST_DB_NAME)
    DEBUG = True
    TESTING = True
