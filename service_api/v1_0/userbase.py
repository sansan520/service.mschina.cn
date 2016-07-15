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
    # user_account = Column('user_account', String(45), index=True, nullable=False)
    # user_password = Column('user_password', String(45), nullable=False)
    # user_mobile = Column('user_mobile', String(45), nullable=False)
    # user_headimg = Column('user_headimg', String(100))
    # user_type = Column('user_type', Integer, nullable=False)  # 0房东，1游客

    user_account = request.json["user_account"]
    if not user_account:
        return jsonify({"code":0,"message":"账号不能为空"})

    user_password = request.json["user_account"]
    if not ho_password:
        return jsonify({"code": 0, "message": "密码不能为空"})

    ho_mobile = request.json["user_account"]
    if not ho_mobile:
        return jsonify({"code": 0, "message": "手机号不能为空"})

    user_type = request.json["user_type"]
    if not user_type:
        return jsonify({"code":0,"message":"用户类型必须是游客或者房东"})

    user_headimg = request.json["user_headimg"]


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