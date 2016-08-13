# coding:utf-8

from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.models.model import GuestRoom, db_session
from . import api
from sqlalchemy import exc

'''
添加新客房
'''
@api.route("/api/v1.0/gr_insert", methods=["POST"])
def insert_guestroom():

    # hs_id = Column('hs_id', Integer, ForeignKey('houseresources.hs_id', ondelete='CASCADE'))
    # rt_id = Column('rt_id', Integer)
    # gt_price = Column('gt_price', DECIMAL(10, 2))
    # gt_describe = Column('gt_describe', String(500))

    hs_id = request.get_json().get("hs_id")
    if not hs_id:
        return jsonify({"code": 0, "message": "参数错误"})
    # rt_id = request.get_json().get("rt_id")
    # if not rt_id:
    #     return jsonify({"code": 0, "message": "参数错误"})

    gr_price = request.get_json().get("gr_price")
    gr_desc = request.get_json().get("gr_desc")
    gr_name = request.get_json().get("gr_name")
    #gr_status = request.get_json().get("gr_status")
    gr_images = request.get_json().get("gr_images")

    guestroom = GuestRoom()
    guestroom.hs_id = hs_id
    #guestroom.rt_id = rt_id
    guestroom.gr_name = gr_name
    guestroom.gr_price = gr_price
    guestroom.gr_des = gr_desc
    #guestroom.gr_status = gr_status
    guestroom.gr_images = gr_images

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
@api.route("/api/v1.0/gr_update/<int:gr_id>", methods=["PUT"])
def update_guestroom(gr_id):
    if not gr_id:
        return jsonify({"code": 0, "message": "参数错误"})

    hs_id = request.get_json().get("hs_id")
    if not hs_id:
        return jsonify({"code": 0, "message": "参数错误"})
    # rt_id = request.get_json().get("rt_id")
    # if not rt_id:
    #     return jsonify({"code": 0, "message": "参数错误"})

    gr_price = request.get_json().get("gr_price")
    gr_desc = request.get_json().get("gr_desc")
    gr_name = request.get_json().get("gr_name")
    #gr_status = request.get_json().get("gr_status")
    gr_images = request.get_json().get("gr_images")

    try:
        db_session.query(GuestRoom).filter(GuestRoom.gr_id == gr_id).update({
            "hs_id": hs_id,
            #"rt_id": rt_id,
            "gr_price": gr_price,
            "gr_desc": gr_desc,
            "gr_name":gr_name,
            #"gr_status":gr_status,
            "gr_images":gr_images
        })

        db_session.commit()
        return jsonify({"code": 1, "message": "客房更新成功"})
    except exc.IntegrityError:
        db_session.rollback()
    return jsonify({"code": 0, "message": "客房更新失败"})

'''
根据客房主键ID,删除客房
'''
@api.route("/api/v1.0/gr_delete/<int:gr_id>", methods=["DELETE"])
def delete_guestroom(gr_id):

    if not gr_id:
        return jsonify({"code": 0, "message": "参数错误"})
    try:

        db_session.query(GuestRoom).filter(GuestRoom.gr_id == gr_id).delete()
        db_session.commit()
        return jsonify({"code": 1, "message": "客房删除成功"})

    except exc.IntegrityError:
        db_session.rollback()

    return jsonify({"code": 0, "message": "客房删除失败"})


#根据客户主键查询客房
@api.route("/api/v1.0/get_guestroom_by_gr_id/<int:gr_id>",methods=['GET'])
def get_guestroom_by_gr_id(gr_id):
    try:
        entity = db_session.query(GuestRoom).filter(GuestRoom.gr_id == gr_id).first()
        return jsonify({"code":1,"message":[entity.to_json]})
    except:
        return jsonify({"code":0,"message":"查询失败"})
    return jsonify({"code":0,"message":"查询异常"})



# 根据房源类型,查询所有客房列表,返回JSON
@api.route("/api/v1.0/get_guestroom_by_hsId/<int:hs_id>", methods=["GET"])
def get_guestroom_by_hsId(hs_id):
    if not hs_id:
        return jsonify({"code": 0, "message": "参数错误"})

    room_lists = db_session.query(GuestRoom).filter(GuestRoom.hs_id == hs_id).all()

    return jsonify({"code": 1, "message": [guestroom.to_json() for guestroom in room_lists]})

# 根据房间类型,查询所有客房列表,返回JSON
# @api.route("/api/v1.0/get_guestroom_by_rtId/<int:rt_id>", methods=["GET"])
# def get_guestroom_by_rtId(rt_id):
#     if not rt_id:
#         return jsonify({"code": 0, "message": "参数错误"})
#
#     room_lists = db_session.query(GuestRoom).filter(GuestRoom.rt_id == rt_id).all()
#
#     return jsonify({"code": 1, "message": [guestroom.to_json() for guestroom in room_lists]})

# 查询所有客房列表,返回JSON
@api.route("/api/v1.0/get_all_guestroom", methods=["GET"])
def get_all_guestroom():

    try:
        guestroom_all = db_session.query(GuestRoom).all()
        return jsonify({"code": 1, "message": [guestroom.to_json() for guestroom in guestroom_all]})
    except:
        return jsonify({"code":0,"message":"暂无数据"})
    return jsonify({"code":0,"message":"查询异常"})
#根据客房名称搜索
@api.route("/api/v1.0/findbygrname/<string:gr_name>", methods=['GET'])
def findbygrname(gr_name):
    if not gr_name:
        return jsonify({"code": 0, "message": "客房不存在"})
    try:
        entities = db_session.query(GuestRoom).filter_by(GuestRoom.gr_name.like('%'+gr_name+'%')).all()
        return jsonify({"code": 1, "message": [entity.to_json() for entity in entities]})
    except:
        return jsonify({"code":0,"message":"暂无数据"})
    return jsonify({"code":0,"message":"查询异常"})

#根据客房价格搜索

@api.route("/api/v1.0/findbygrprice/<string:gr_price>", methods=['GET'])
def findbygrprice(gr_price):
    if not gr_price:
        return jsonify({"code": 0, "message": "暂无数据"})
    try:
        entities = db_session.query(GuestRoom).filter_by(GuestRoom.gr_price <= gr_price).all()
        return jsonify({"code": 1, "message": [entity.to_json() for entity in entities]})
    except:
        return jsonify({"code": 0, "message": "暂无数据"})
    return jsonify({"code":0,"message":"查询异常"})
