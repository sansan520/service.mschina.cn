# # coding:utf-8
# from . import api
# from service_api.models.model_new import RoomType, db_session
# from functools import wraps
# from flask import jsonify, request, g, current_app
#
# from sqlalchemy import exc
# @api.route("/api/v1.0/test", methods=["GET"])
# def json_test():
#     return "hello world"
#
# @api.route("/api/v2.0/rt_insert", methods=["POST"])
# def insert_roomtype():
#     # rt_id = Column('rt_id', Integer, primary_key=True)
#     # rt_name = Column('rt_name', String(50), nullable=False)
#
#     rt_name = request.json["rt_name"]
#     if not rt_name:
#         return jsonify({"code": 0, "message": "房间类型不能为空"})
#
#     roomtype = RoomType()
#     roomtype.rt_name = rt_name
#
#     try:
#         db_session.add(roomtype)
#         db_session.commit()
#         return jsonify({"code": 1, "message": "房间类型添加成功"})
#     except exc.IntegrityError:
#         db_session.rollback()
#
#     return jsonify({"code": 0, "message": "房间类型添加失败"})
