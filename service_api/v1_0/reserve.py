# coding:utf-8

from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.models.model import Reserve, db_session
from . import api
from sqlalchemy import exc

# 预订客房
@api.route("/api/v1.0/insert_reserve", methods=["POST"])
def insert_reserve():
    gr_id = request.get_json().get("gr_id")
    if not gr_id:
        return jsonify({"code": 0, "message": "请选择客房"})
    user_id = request.get_json().get("user_id")
    if not user_id:
        return jsonify({"code": 0, "message": "请先登录"})

    start_time = request.get_json().get("start_time")
    end_time = request.get_json().get("end_time")
    status = request.get_json().get("status")

    reserve = Reserve()
    reserve.user_id = user_id
    reserve.gr_id = gr_id
    reserve.start_time = start_time
    reserve.end_time = end_time
    reserve.status = status
    try:
        db_session.add(reserve)
        db_session.commit()
        return jsonify({"code": 1, "message": "预订成功"})
    except exc.IntegrityError:
        db_session.rollback()

    return jsonify({"code": 0, "message": "预订失败"})

# 更新预订状态
@api.route("/api/v1.0/update_reserve/<int:id>", methods=["PUT"])
def update_reserve(id):
    start_time = request.get_json().get("start_time")
    end_time = request.get_json().get("end_time")
    status = request.get_json().get("status")
    try:
        db_session.query(Reserve).filter(Reserve.id == id).update({
            "start_time": start_time,
            "end_time": end_time,
            "status": status,
            "modify_time":datetime.now()
        })

        db_session.commit()
        return jsonify({"code": 1, "message": "预定状态修改成功"})
    except exc.IntegrityError:
        db_session.rollback()
    return jsonify({"code": 0, "message": "预订修改失败"})

# 退订客房
@api.route("/api/v1.0/del_reserve/<int:id>", methods=["PUT"])
def del_reserve(id):
    if not id:
        return jsonify({"code": 0, "message": "退订客房id不能为空"})
    try:
        db_session.query(Reserve).filter(Reserve.id == id).update({
            "status": 0,
            "modify_time": datetime.now()
        })

        db_session.commit()
        return jsonify({"code": 1, "message": "客房退订成功"})
    except exc.IntegrityError:
        db_session.rollback()
    return jsonify({"code": 0, "message": "预订修改失败"})

@api.route("/api/v1.0/get_reserve_by_user_id/<int:user_id>", methods=["GET"])
def get_reserve_by_user_id(user_id):
    try:
        entitys = db_session.query(Reserve).filter(Reserve.user_id == user_id).all()
        return jsonify({"code": 1, "message": [entity.to_json() for entity in entitys]})
    except:
        return jsonify({"code": 0, "message": "查询失败"})
    return jsonify({"code": 0, "message": "获取预订信息失败"})

@api.route("/api/v1.0/get_reserve_by_id/<int:id>", methods=["GET"])
def get_reserve_by_id(id):
    try:
        entity = db_session.query(Reserve).filter(Reserve.id == id).first()
        return jsonify({"code": 1, "message": entity.to_json()})
    except:
        return jsonify({"code": 0, "message": "查询失败"})
    return jsonify({"code": 0, "message": "获取预订信息失败"})

@api.route("/api/v1.0/get_reserve_by_grid/<int:gr_id>", methods=["GET"])
def get_reserve_by_gr_id(gr_id):
    try:
        entity = db_session.query(Reserve).filter(Reserve.gr_id == gr_id).first()
        return jsonify({"code": 1, "message": entity.to_json()})
    except:
        return jsonify({"code": 0, "message": "查询失败"})
    return jsonify({"code": 0, "message": "获取预订信息失败"})






