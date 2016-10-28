import os
# BASEDIR = os.path.abspath(os.path.dirname(__file__))

class DevelopmentConfig(object):
    """Development configuration."""
    DEBUG = True
    db_path = os.path.join(os.path.dirname(__file__), 'application.sqlite')
    db_uri = 'sqlite:///{}'.format(db_path)
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class TestingConfig(object):
    """Testing configuration."""
    db_path = os.path.join(os.path.dirname(__file__), 'tests/testdb.sqlite')
    db_uri = 'sqlite:///{}'.format(db_path)
    TESTING = True
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = True

config_settings = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
