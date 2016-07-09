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
    house_type.ty_name = t_name
    house_type.ty_valume = 0

    try:
        db_session.add(house_type)
        db_session.commit()
        return jsonify({"code": 1, "message": "类型添加成功"})
    except exc.IntegrityError:
        db_session.rollback()

    return jsonify({"code": 0, "message": "类型添加失败"})


@api.route("/api/v1.0/ht_update/<int:ty_id>", methods=["PUT"])
def update_housetype(ty_id):
    if not ty_id:
        return jsonify({"code": 0, "message": "参数错误"})

    ty_name = request.get_json().get("ty_name")
    if not ty_name:
        return jsonify({"code": 0, "message": "参数错误"})

    try:
        db_session.query(HouseType).filter(HouseType.ty_id == ty_id).update({
            "ty_name": ty_name
        })

        db_session.commit()
        return jsonify({"code": 1, "message": "类型更新成功"})
    except exc.IntegrityError:
        db_session.rollback()
    return jsonify({"code": 0, "message": "类型更新失败"})


@api.route("/api/v1.0/ht_delete/<int:ty_id>", methods=["DELETE"])
def delete_housetype(ty_id):

    if not ty_id:
        return jsonify({"code": 0, "message": "参数错误"})
    try:

        db_session.query(HouseType).filter(HouseType.ty_id == ty_id).delete()
        db_session.commit()
        return jsonify({"code": 1, "message": "类型删除成功"})

    except exc.IntegrityError:
        db_session.rollback()

    return jsonify({"code": 0, "message": "类型删除失败"})

@api.route("/api/v1.0/get_all_house_type", methods=["GET"])
def getall_housetype():

    housetype_all = db_session.query(HouseType).all()

    return jsonify({"code": 1, "message": [housetype.to_json() for housetype in housetype_all]})
