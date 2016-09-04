# coding:utf-8
import hashlib
import time
from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.models.model import UserBase,HouseOwner,UserBase_Ext, db_session
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

@api.route("/api/v1.0/get_hs/<string:ho_name>",methods=["GET"])
# @login_check
def get_house_owner(ho_name):
    try:
        # 通过redis中取出的账号查找mysql 数据库,返回该账号其他资料
        entity = db_session.query(HouseOwner).filter(HouseOwner.ho_name == ho_name).one()
        # print(entity.ho_name)
        return jsonify({'code': 1, 'message':[entity.to_json()]})
    except:
        return jsonify({"code":0,"message":"该用户不存在"})
    return jsonify({"code":0,"message":"查询异常"})

@api.route("/api/v1.0/get_hs_by_Id/<int:ho_id>", methods=["GET"])
def get_hs_by_userId(ho_id):
    if not ho_id:
        return jsonify({"code": 0, "message": "参数错误"})
    try:
        entity = HouseOwner.query.filter(HouseOwner.ho_id == ho_id).one()
        return jsonify({"code": 1, "message": [entity.to_json()]})
    except:
        return jsonify({"code": 0, "message": "查询失败"})

# 获取所有普通会员用户分页列表
@api.route("/api/v1.0/get_all_hs_owner/<int:page>")
def get_all_hs_owner(page=1):
    pagesize = 10
    #try:
    querylist = UserBase.query.join(HouseOwner,UserBase.user_id == HouseOwner.user_id).\
        add_columns(UserBase.user_id,UserBase.user_account,UserBase.user_createtime,UserBase.user_headimg,UserBase.user_mobile,
                    UserBase.user_headimg,UserBase.user_password,UserBase.user_status,UserBase.user_type,UserBase.user_modifytime,HouseOwner.ho_id).\
        filter(UserBase.user_type == 0).order_by(HouseOwner.user_id.desc()).paginate(page, per_page=pagesize)
    newEntities = []
    newItem = UserBase_Ext()
    entities = querylist.items
    for entity in entities:
        newItem.user_account = entity.user_account
        newItem.ho_id=entity.ho_id
        newItem.user_type=entity.user_type
        newItem.user_status=entity.user_status
        newItem.user_headimg=entity.user_headimg
        newItem.user_id=entity.user_id
        newItem.user_createtime=entity.user_createtime
        newItem.user_modifytime=entity.user_modifytime
        newItem.user_mobile=entity.user_mobile
        newItem.user_password=entity.user_password
        newEntities.append(newItem)
    pages = querylist.pages  # 总页数
    total = querylist.total  # 总记录数
    return jsonify({"code": 1, "page": page, "pages": pages, "total": total,"message": [newItem.to_json() for newItem in newEntities]})
    # except:
    #     return jsonify({"code": 0, "message": "查询异常"})


#
# @api.route("/api/v1.0/get_by_ho_mobile")
# def getbymobile():
#     current_user = g.current_user
#     entity = db_session.query(HouseOwner).filter(HouseOwner.ho_mobile == current_user.ho_mobile).one()
#     db_session.close()
#     return jsonify({'code': 1, 'ho_id': entity.ho_id, 'ho_name': entity.ho_name, 'ho_email': entity.ho_email, 'message': '操作成功','token': g.token})
# @api.route("/api/v1.0/get_by_ho_email")
# def getbyemail():
#     current_user = g.current_user
#     entity = db_session.query(HouseOwner).filter(HouseOwner.ho_email == current_user.ho_email).one()
#     db_session.close()
#     return jsonify({'code': 1, 'ho_id': entity.ho_id, 'ho_name': entity.ho_name, 'ho_email': entity.ho_email, 'message': '操作成功','token': g.token})

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