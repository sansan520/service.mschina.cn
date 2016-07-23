# coding:utf-8

import hashlib
import time
from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.models.model import UserBase, db_session
from sqlalchemy import exc
from . import api

#http://www.cnblogs.com/melonjiang/p/5342505.html
# http://redis.readthedocs.io/en/2.4/hash.html
# http://blog.csdn.net/u012894975/article/details/51333535  #python操作redis


@api.route("/api/v1.0/user_login", methods=["POST"])
def user_login():

    user_account = request.json["user_account"]
    user_password = request.json["user_password"]

    userbase = db_session.query(UserBase).filter(UserBase.user_account == user_account).first()
    if not userbase:
        return jsonify({'code': 0, 'message': '没有此用户'})

    if userbase.user_password != user_password:
        return jsonify({'code': 0, 'message': '密码错误'})

    m = hashlib.md5()
    m.update(user_account.encode("utf8"))
    m.update(user_password.encode("utf8"))
    # m.update(str(int(time.time())).encode("utf8"))
    user_account = m.hexdigest()   # 2dd99d263ecc5ebf25b91d2532b46080

    # 将该用户消息保存到redis中redis.Redis(host='127.0.0.1', port=6379, db=0)
    pipeline = current_app.session_redis.pipeline()
    # user_json = userbase.to_json()  # => test ok like hmDict = {'field': 'foo', 'field1': 'bar'}
    pipeline.hmset("user:%s" % user_account, {"current_user": userbase.to_json()})
    pipeline.expire("user:%s" % user_account, 60*5)  # 秒单位
    pipeline.execute()
    # test ok ,return  bytes like b'sansan',b'1',[b'1']
    # result = current_app.session_redis.hmget('user:%s' % user_account, ['user_id', 'user_account'])
    # result_01 = current_app.session_redis.hmget('user:%s' % user_account, 'user_id')
    # result_02 = current_app.session_redis.hget('user:%s' % user_account, 'user_id')
    # print(result)
    # print(result_01)
    # print(result_02)
    # 简单类型存取
    # pipeline.set("username:%s" % user_account, userbase.user_mobile)
    # pipeline.expire("username:%s" % user_account, 60 * 2)  # 秒单位
    # username = current_app.redis.get("username:%s" % user_account)  # bytes name,mobile
    # print(type(username))
    # username_new = username.decode()   # bytes to str
    # print(type(username_new))
    # 简单类型存取结束

    return jsonify({'code': 1, 'message': '成功登录', 'current_user': userbase.to_json()})

@api.route("/api/v1.0/user_register", methods=["POST"])
def user_register():

    user_account = request.json["user_account"]
    if not user_account:
        return jsonify({"code":0,"message":"账号不能为空"})

    user_password = request.json["user_password"]
    if not user_password:
        return jsonify({"code": 0, "message": "密码不能为空"})

    user_mobile = request.json["user_mobile"]
    if not user_mobile:
        return jsonify({"code": 0, "message": "手机号不能为空"})

    user_type = request.json["user_type"]       # 0房东，1游客
    if not user_type:
        return jsonify({"code":0,"message":"用户类型必须是游客或者房东"})

    user_headimg = request.json["user_headimg"]

    userbase = UserBase()
    userbase.user_account = user_account
    userbase.user_password = user_password
    userbase.user_mobile = user_mobile
    userbase.user_type = user_type
    userbase.user_headimg = user_headimg

    try:
        db_session.add(userbase)
        db_session.commit()
        return jsonify({"code":1,"message":"恭喜您注册成功"})
    except exc.IntegrityError:
        db_session.rollback();
        return jsonify({"code":0,"message":"注册失败"})
#查询手机号是否存在
@api.route("/api/v1.0/get_by_mobile/<string:user_mobile>",methods=["GET"])
def getbymobile(user_mobile):
    #current_user = g.current_user
    entity = db_session.query(UserBase).filter(UserBase.ho_mobile == user_mobile).one()
    return jsonify({'code': 0, "message":[entity.to_json()]})

#查询账号是否存在
@api.route("/api/v1.0/get_by_account/<string:user_account>",methods=["GET"])
def getbyaccount(user_account):
    entity = db_session.query(UserBase).filter(UserBase.user_account == user_account).one()
    return jsonify({"code":0,"message":[entity.to_json()]})
