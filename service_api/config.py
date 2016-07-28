#   发布环境
class ProductionConfig(object):
    DEBUG = False

    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = ''

    MYSQL_INFO = "mysql+pymysql://root:123@127.0.0.1:3306/mschina?charset=utf8"

#   开发环境
class DevelopmentConfig(object):
    DEBUG = True

    SERVICE_HOST = '127.0.0.1'
    SERVICE_PORT = 8080

    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379
    CACHE_DB = 1
    SESSION_DB = 0
    REDIS_PASSWORD = ''

    MYSQL_INFO = "mysql+pymysql://root:123456@127.0.0.1:3306/mschina?charset=utf8"
    #SQLALCHEMY_TRACK_MODIFICATIONS = True

Conf = DevelopmentConfig