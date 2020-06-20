

class Config(object):
    '''Common configurations'''
    pass


class DevelopmentConfig(object):
    '''Development configurations'''
    DEBUG = True
    # To log errors
    SQLALCHEMY_ECHO = True
    

class ProductionConfig(object):
    '''Production configurations'''
    DEBUG = False



app_config = {
    'development' : DevelopmentConfig,
    'production' : ProductionConfig
}
