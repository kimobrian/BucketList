class DevelopmentConfig(object):
    """Development configuration."""
    DEBUG = True
    '''
    Comment out the following 3 lines to switch your application to sqlite
    '''
    # db_path = os.path.join(os.path.dirname(__file__), 'application.sqlite')
    # db_uri = 'sqlite:///{}'.format(db_path)
    # SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_DATABASE_URI = 'postgresql://develop:pass123@' \
        'localhost:5432/bucket_list'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(object):
    """Testing configuration."""
    '''
    Comment out the following 4 lines to switch your application to sqlite
    '''
    # db_path = os.path.join(os.path.dirname(__file__), 'tests/testdb.sqlite')
    # db_uri = 'sqlite:///{}'.format(db_path)
    # TESTING = True
    # SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_DATABASE_URI = 'postgresql://develop:pass123' \
        '@localhost:5432/bucketlist_test'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False


config_settings = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}
