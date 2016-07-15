# coding:utf-8
import hashlib
import time
from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.models.model import HouseOwner, db_session
from sqlalchemy import exc
from . import api

#redis 需要安装python支持库=>sudo pip install redis

#
# app = Flask(__name__)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
# redis_store = redis.StrictRedis(host=Conf.REDIS_HOST, port=Conf.REDIS_PORT, db=Conf.REDIS_DB, password=Conf.REDIS_PASSWORD)
#在此之前设置config

# def login_check(func):
#     @wraps(func)
#     def decorator(*args, **kwargs):
#         token = request.headers.get("token")
#         if not token:
#             return jsonify({"code": 0, "message": "token错误,需要验证"})
#         ho_account = current_app.redis.get("token:%s" % token)
#         tokenfrmredis = current_app.redis.hget('user:%s' % ho_account.decode('utf8'), 'token')
#
#         if not ho_account or token.encode(encoding="utf8") != tokenfrmredis:
#             return jsonify({'code': 2, 'message': '验证信息错误'})
#         return func(*args, **kwargs)
#
#     return decorator
#
# @api.before_request
# def before_request():
#     token = request.headers.get("token")
#     if token:
#         account = current_app.redis.get("token:%s" % token)
#         # print(account)
#         if not account:
#             account = account.encode("utf8")
#         g.current_user = db_session.query(HouseOwner).filter(HouseOwner.ho_account == account).one()
#         g.token = token
#     return


@api.route("/api/v1.0/ho_register", methods=["POST"])
def ho_register():
    ho_name = request.get_json().get("ho_name")
    if not ho_name:
        return jsonify({"code":0,"message":"姓名不能为空"})
    ho_account = request.get_json().get("ho_account")
    if not ho_account:
        return jsonify({"code":0,"message":"账号不能为空"})
    ho_password = request.get_json().get("ho_password")
    if not ho_password:
        return jsonify({"code": 0, "message": "密码不能为空"})
    ho_mobile = request.get_json().get("ho_mobile")
    if not ho_mobile:
        return jsonify({"code": 0, "message": "手机号不能为空"})
    ho_email = request.get_json().get("ho_email")
    if not ho_email:
        return jsonify({"code":0,"message":"邮箱不能为空"})
    ho_nicard = request.get_json().get("ho_nicard")
    if not ho_nicard:
        return jsonify({"code": 0, "message": "证件照不能为空"})

    house_owner = HouseOwner()
    house_owner.ho_name = ho_name
    house_owner.ho_account = ho_account
    house_owner.ho_password = ho_password
    house_owner.ho_tel = request.get_json().get("ho_tel")
    house_owner.ho_mobile = ho_mobile
    house_owner.ho_nicard = ho_nicard
    house_owner.ho_image = request.get_json().get("ho_image")
    house_owner.ho_email = request.get_json().get("ho_email")
    try:
        db_session.add(house_owner)
        db_session.commit()
        return jsonify({"code":1,"message":"恭喜您注册成功"})
    except exc.IntegrityError:
        db_session.rollback();
        return jsonify({"code":0,"message":"注册失败"})


# @api.route("/api/v1.0/ho_login", methods=["POST"])
# def house_owner_login():
#
#     ho_account = request.json["ho_account"]
#     ho_password = request.json["ho_password"]
#
#     houseowner = db_session.query(HouseOwner).filter(HouseOwner.ho_account == ho_account).first()
#     if not houseowner:
#         return jsonify({'code': 0, 'message': '没有此用户'})
#
#     if houseowner.ho_password != ho_password:
#         return jsonify({'code': 0, 'message': '密码错误'})
#
#     # m = hashlib.md5()
#     # m.update(ho_account.encode("utf8"))
#     # m.update(ho_password.encode("utf8"))
#     # m.update(str(int(time.time())).encode("utf8"))
#     # token = m.hexdigest()
#
#
#     # redis_store.hmset("user:%s" % ho_account, {"token": token, "online": 1})
#     # redis_store.set("token:%s" % token, ho_account)
#     # redis_store.expire("token:%s" % token, 3600*5)
#
#     # 为防止传输过程中出错,改用管道
#     # pipeline = current_app.redis.pipeline()
#     # pipeline.hmset("user:%s" % ho_account, {"token": token, "online": 1})
#     # pipeline.set("token:%s" % token, ho_account)
#     # pipeline.expire("token:%s" % token, 3600*5)
#     # pipeline.execute()
#
#     return jsonify({'code': 1, 'message': '成功登录', 'current_user': houseowner.to_json()})

@api.route("/api/v1.0/get_ho_by_token")
# @login_check
def get_house_owner():
    current_user = g.current_user
    # 通过redis中取出的账号查找mysql 数据库,返回该账号其他资料
    entity = db_session.query(HouseOwner).filter(HouseOwner.ho_account == current_user.ho_account).one()
    # print(entity.ho_name)
    db_session.close()

    #return json.dumps(entity.to_json(), ensure_ascii=False)
    return jsonify({'code': 1, 'ho_id': entity.ho_id, 'ho_name': entity.ho_name, 'ho_email': entity.ho_email, 'message': '操作成功', 'token': g.token})
@api.route("/api/v1.0/get_by_ho_mobile")
def getbymobile():
    current_user = g.current_user
    entity = db_session.query(HouseOwner).filter(HouseOwner.ho_mobile == current_user.ho_mobile).one()
    db_session.close()
    return jsonify({'code': 1, 'ho_id': entity.ho_id, 'ho_name': entity.ho_name, 'ho_email': entity.ho_email, 'message': '操作成功','token': g.token})
@api.route("/api/v1.0/get_by_ho_email")
def getbyemail():
    current_user = g.current_user
    entity = db_session.query(HouseOwner).filter(HouseOwner.ho_email == current_user.ho_email).one()
    db_session.close()
    return jsonify({'code': 1, 'ho_id': entity.ho_id, 'ho_name': entity.ho_name, 'ho_email': entity.ho_email, 'message': '操作成功','token': g.token})

# @api.route("/api/v1.0/logout")
# # @login_check
# def logout():
#
#     current_user = g.current_user
#
#     pipeline = current_app.redis.pipeline()
#     pipeline.delete("token:%s" % g.token)
#     pipeline.hmset("user:%s" % current_user.ho_account, {"online": 0})
#     pipeline.execute()
#     '''
#     127.0.0.1:6379> hget user:jsonwang token
#     "61e35e6c30f3b51a2e8e45c4016f98ea"
#     127.0.0.1:6379> keys *
#     1) "user:jsonwang"
#     127.0.0.1:6379> hget user:jsonwang token
#     "61e35e6c30f3b51a2e8e45c4016f98ea"
#     127.0.0.1:6379> hget user:jsonwang online
#     "0"
#     '''
#     return jsonify({"code": 1, "message": "注销成功"})


@api.teardown_request
def handle_teardown_request(exception):
    db_session.remove()

# if __name__ == "__main__":
#     app.run(host=Conf.SERVICE_HOST, port=Conf.SERVICE_PORT, debug=Conf.DEBUG)