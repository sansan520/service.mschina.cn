# coding:utf-8

from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.model import HouseType, db_session
from . import api
from sqlalchemy import exc


@api.route("/api/v1.0/ht_insert", methods=["POST"])
def insert_housetype():

    t_name = request.get_json().get("ty_name")
    if not t_name:
        return jsonify({"code": 0, "message": "类型不能为空"})

    house_type = HouseType()
    house_type.ho_account = request.get_json().get("ho_account")
    house_type.ty_valume = 0

    try:
        db_session.add(house_type)
        db_session.commit()
        return jsonify({"code": 1, "message": "类型添加成功"})
    except exc.IntegrityError:
        db_session.rollback()

    return jsonify({"code": 0, "message": "类型添加失败"})

#
# @api.route("/api/v1.0/ht_update", methods=["PUT"])
# def update_housetype():
