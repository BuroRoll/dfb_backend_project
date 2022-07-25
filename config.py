class Config(object):
    DEBUG = False
    # TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'b\'\xc5>`\xe3C\x19\x13\xdc\xeaV\xefT\x9d\xa4x\xae\''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '3jkewh2jhfblj23*657lb3@$2#$$!241ae$'


# class ProductionConfig(Config):
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevelopmentConfig(Config):
    # FLASK_ENV=development
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql://danilkonkov:22012011@localhost:5432/dfb_db"
