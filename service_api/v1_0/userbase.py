# coding:utf-8

import hashlib
import time
from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.models.model import UserBase, db_session
from sqlalchemy import exc
from . import api

@api.route("/api/v1.0/user_login", methods=["POST"])
def user_login():

    user_account = request.json["user_account"]
    user_password = request.json["user_password"]

    userbase = db_session.query(UserBase).filter(UserBase.user_account == user_account).first()
    if not userbase:
        return jsonify({'code': 0, 'message': '没有此用户'})

    if userbase.user_password != user_password:
        return jsonify({'code': 0, 'message': '密码错误'})

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
    userbase.user_id = user_type
    userbase.user_headimg = user_headimg

    try:
        db_session.add(userbase)
        db_session.commit()
        return jsonify({"code":1,"message":"恭喜您注册成功"})
    except exc.IntegrityError:
        db_session.rollback();
        return jsonify({"code":0,"message":"注册失败"})