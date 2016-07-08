# coding:utf-8
from flask import Flask
import redis
from service_api.config import Conf
from service_api.v1_0 import api as api_1_0_blueprint

def create_app():

    app = Flask(__name__)
    app.config.from_object(Conf)

    # print(app.config['REDIS_HOST'])

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    # redis_store = redis.StrictRedis(host=Conf.REDIS_HOST, port=Conf.REDIS_PORT, db=Conf.REDIS_DB,
    #                                 password=Conf.REDIS_PASSWORD)
    # app.secret_key = app.config['SECRET_KEY']
    app.redis = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'],
                            db=app.config['REDIS_DB'], password=app.config['REDIS_PASSWORD'])

    # app.q = Auth(access_key=app.config['QINIU_ACCESS_KEY'], secret_key=app.config['QINIU_SECRET_KEY'])
    # app.bucket_name = app.config['BUCKET_NAME']
    app.debug = app.config['DEBUG']

    # from service_api.v1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=Conf.DEBUG, host=Conf.SERVICE_HOST, port=Conf.SERVICE_PORT)