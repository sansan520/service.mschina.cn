# coding:utf-8

from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.model import HouseType, db_session
from . import api
from sqlalchemy import exc

'''
添加客房类型
'''
@api.route("/api/v1.0/rt_insert", methods=["POST"])
def insert_roomtype():
    # rt_id = Column('rt_id', Integer, primary_key=True)
    # rt_name = Column('rt_name', String(50), nullable=False)

    rt_name = request.get_json().get("rt_name")
    if not rt_name:
        return jsonify({"code": 0, "message": "房间类型不能为空"})

    roomtype = RoomType({"rt_name": rt_name})

    try:
        db_session.add(roomtype)
        db_session.commit()
        return jsonify({"code": 1, "message": "房间类型添加成功"})
    except exc.IntegrityError:
        db_session.rollback()

    return jsonify({"code": 0, "message": "房间类型添加失败"})
