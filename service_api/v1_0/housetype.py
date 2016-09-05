# coding:utf-8

from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.models.model import HouseType, db_session,db
from . import api
from sqlalchemy import exc


@api.route("/api/v1.0/ht_insert", methods=["POST"])
def insert_housetype():
    ty_name = request.get_json().get("ty_name")
    if not ty_name:
        return jsonify({"code": 0, "message": "类型不能为空"})
    ty_valume = request.get_json().get("ty_valume")
    if not ty_valume:
        return jsonify({"code": 0, "message": "类型不能为空"})
    house_type = HouseType()
    house_type.ty_name = ty_name
    house_type.ty_valume = ty_valume

    try:
        db.session.add(house_type)
        db.session.commit()
        # db_session.add(house_type)
        # db_session.commit()
        return jsonify({"code": 1, "message": "类型添加成功"})
    except exc.IntegrityError:
        db_session.rollback()

    return jsonify({"code": 0, "message": "类型添加失败"})

#  分页查询 - 用户admin
@api.route("/api/v1.0/get_all_hs_type/<int:page>")
def get_all_hs_type(page=1):
    pagesize = 10
    pagination = HouseType.query.order_by(HouseType.ty_id.desc()).paginate(page, per_page=pagesize, error_out=False)

    entities = pagination.items

    pages = pagination.pages  # 总页数
    total = pagination.total  # 总记录数

    return jsonify({"code": 1, "page": page, "pages": pages, "total": total, "message": [entity.to_json() for entity in entities]})

@api.route("/api/v1.0/ht_update/<int:ty_id>", methods=["PUT"])
def update_housetype(ty_id):
    if not ty_id:
        return jsonify({"code": 0, "message": "参数错误"})

    ty_name = request.get_json().get("ty_name")
    if not ty_name:
        return jsonify({"code": 0, "message": "参数错误"})
    ty_valume = request.get_json().get("ty_valume")
    if not ty_valume:
        return jsonify({"code": 0, "message": "参数错误"})
    try:
        db.session.query(HouseType).filter(HouseType.ty_id == ty_id).update({
            "ty_name": ty_name,
            "ty_valume":ty_valume
        })

        db.session.commit()
        return jsonify({"code": 1, "message": "类型更新成功"})
    except exc.IntegrityError:
        db_session.rollback()
    return jsonify({"code": 0, "message": "类型更新失败"})


@api.route("/api/v1.0/ht_delete/<int:ty_id>", methods=["DELETE"])
def ht_delete(ty_id):

    if not ty_id:
        return jsonify({"code": 0, "message": "参数错误"})
    try:
        db.session.query(HouseType).filter(HouseType.ty_id == ty_id).delete()
        db.session.commit()
        return jsonify({"code": 1, "message": "类型删除成功"})

    except exc.IntegrityError:
        db_session.rollback()

    return jsonify({"code": 0, "message": "类型删除失败"})

