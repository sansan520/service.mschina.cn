# coding:utf-8

from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.models.model import GuestRoom, db_session
from . import api
from sqlalchemy import exc

'''
添加新客房
'''
@api.route("/api/v1.0/gt_insert", methods=["POST"])
def insert_guestroom():

    # hs_id = Column('hs_id', Integer, ForeignKey('houseresources.hs_id', ondelete='CASCADE'))
    # rt_id = Column('rt_id', Integer)
    # gt_price = Column('gt_price', DECIMAL(10, 2))
    # gt_describe = Column('gt_describe', String(500))

    hs_id = request.get_json().get("hs_id")
    if not hs_id:
        return jsonify({"code": 0, "message": "参数错误"})
    rt_id = request.get_json().get("rt_id")
    if not rt_id:
        return jsonify({"code": 0, "message": "参数错误"})

    gt_price = request.get_json().get("gt_price")
    gt_describe = request.get_json().get("gt_describe")

    guestroom = GuestRoom()
    guestroom.hs_id = hs_id
    guestroom.rt_id = rt_id
    guestroom.gt_price = gt_price
    guestroom.gt_describe = gt_describe

    try:
        db_session.add(guestroom)
        db_session.commit()
        return jsonify({"code": 1, "message": "客房添加成功"})
    except exc.IntegrityError:
        db_session.rollback()

    return jsonify({"code": 0, "message": "客房添加失败"})

'''
根据客房主键ID,更新客房
'''
@api.route("/api/v1.0/gt_update/<int:gt_id>", methods=["PUT"])
def update_guestroom(gt_id):
    if not gt_id:
        return jsonify({"code": 0, "message": "参数错误"})

    hs_id = request.get_json().get("hs_id")
    if not hs_id:
        return jsonify({"code": 0, "message": "参数错误"})
    rt_id = request.get_json().get("rt_id")
    if not rt_id:
        return jsonify({"code": 0, "message": "参数错误"})

    gt_price = request.get_json().get("gt_price")
    gt_describe = request.get_json().get("gt_describe")

    try:
        db_session.query(GuestRoom).filter(GuestRoom.gt_id == gt_id).update({
            "hs_id": hs_id,
            "rt_id": rt_id,
            "gt_price": gt_price,
            "gt_describe": gt_describe
        })

        db_session.commit()
        return jsonify({"code": 1, "message": "客房更新成功"})
    except exc.IntegrityError:
        db_session.rollback()
    return jsonify({"code": 0, "message": "客房更新失败"})

'''
根据客房主键ID,删除客房
'''
@api.route("/api/v1.0/gt_delete/<int:gt_id>", methods=["DELETE"])
def delete_guestroom(gt_id):

    if not gt_id:
        return jsonify({"code": 0, "message": "参数错误"})
    try:

        db_session.query(GuestRoom).filter(GuestRoom.gt_id == gt_id).delete()
        db_session.commit()
        return jsonify({"code": 1, "message": "客房删除成功"})

    except exc.IntegrityError:
        db_session.rollback()

    return jsonify({"code": 0, "message": "客房删除失败"})


# 根据房源类型,查询所有客房列表,返回JSON
@api.route("/api/v1.0/get_guestroom_by_hsId/<int:hs_id>", methods=["GET"])
def get_guestroom_by_hsId(hs_id):
    if not hs_id:
        return jsonify({"code": 0, "message": "参数错误"})

    room_lists = db_session.query(GuestRoom).filter(GuestRoom.hs_id == hs_id).all()

    return jsonify({"code": 1, "message": [guestroom.to_json() for guestroom in room_lists]})

# 根据房间类型,查询所有客房列表,返回JSON
@api.route("/api/v1.0/get_guestroom_by_rtId/<int:rt_id>", methods=["GET"])
def get_guestroom_by_rtId(rt_id):
    if not hsrt_id_id:
        return jsonify({"code": 0, "message": "参数错误"})

    room_lists = db_session.query(GuestRoom).filter(GuestRoom.rt_id == rt_id).all()

    return jsonify({"code": 1, "message": [guestroom.to_json() for guestroom in room_lists]})

# 查询所有客房列表,返回JSON
@api.route("/api/v1.0/get_all_guest_room", methods=["GET"])
def getall_guestroom():

    guestroom_all = db_session.query(GuestRoom).all()

    return jsonify({"code": 1, "message": [guestroom.to_json() for guestroom in guestroom_all]})
