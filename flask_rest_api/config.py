class Development(object):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CSV_REL_FILE_PATH = 'code_challenge_question_dump.csv'


class Testing(object):
    DEBUG = False
    # SQLALCHEMY_ECHO = True

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CSV_REL_FILE_PATH = 'code_challenge_question_dump_testing.csv'


class Production(object):
    DEBUG = False

    SQLALCHEMY_DATABASE_URI = 'NOT PRODUCTION READY'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
