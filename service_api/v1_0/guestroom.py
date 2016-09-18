# coding:utf-8

from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.models.model import db,GuestRoom, db_session
from . import api
from sqlalchemy import exc

'''
添加新客房
'''
@api.route("/api/v1.0/gr_insert", methods=["POST"])
def insert_guestroom():

    hs_id = request.get_json().get("hs_id")
    if not hs_id:
        return jsonify({"code": 0, "message": "参数错误"})

    gr_price = request.get_json().get("gr_price")
    gr_desc = request.get_json().get("gr_desc")
    gr_name = request.get_json().get("gr_name")
    gr_status = request.get_json().get("gr_status")
    gr_images = request.get_json().get("gr_images")

    guestroom = GuestRoom()
    guestroom.hs_id = hs_id
    guestroom.gr_name = gr_name
    guestroom.gr_price = gr_price
    guestroom.gr_desc = gr_desc
    guestroom.gr_status = gr_status
    guestroom.gr_images = gr_images
    # 添加详细信息
    guestroom.gr_room_type = request.get_json().get("gr_room_type")
    guestroom.gr_room_area=request.get_json().get("gr_room_area")
    guestroom.gr_bed_type = request.get_json().get("gr_bed_type")
    guestroom.gr_bed_count = request.get_json().get("gr_bed_count")
    guestroom.gr_settings = request.get_json().get("gr_settings")

    try:
        db.session.add(guestroom)
        db.session.commit()
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

    gr_price = request.get_json().get("gr_price")
    gr_desc = request.get_json().get("gr_desc")
    gr_name = request.get_json().get("gr_name")
    gr_status = request.get_json().get("gr_status")
    gr_images = request.get_json().get("gr_images")
    gr_windows =request.get_json().get("gr_windows")
    gr_breakfast = request.get_json().get("gr_breakfast")
    gr_settings = request.get_json().get("gr_settings")
    gr_room_type = request.get_json().get("gr_room_type")
    gr_room_area = request.get_json().get("gr_room_area")
    gr_bed_type = request.get_json().get("gr_bed_type")
    gr_bed_count = request.get_json().get("gr_bed_count")

    try:
        db.session.query(GuestRoom).filter(GuestRoom.gr_id == gr_id).update({
            "hs_id": hs_id,
            "gr_price": gr_price,
            "gr_desc": gr_desc,
            "gr_name":gr_name,
            "gr_status":gr_status,
            "gr_images":gr_images,
            "gr_room_type":gr_room_type,
            "gr_room_area":gr_room_area,
            "gr_bed_type":gr_bed_type,
            "gr_bed_count":gr_bed_count,
            "gr_windows":gr_windows,
            "gr_breakfast":gr_breakfast,
            "gr_settings":gr_settings
        })

        db.session.commit()
        return jsonify({"code": 1, "message": "客房更新成功"})
    except exc.IntegrityError:
        db.session.rollback()
    return jsonify({"code": 0, "message": "客房更新失败"})

'''
根据客房主键ID,删除客房
'''
@api.route("/api/v1.0/gr_delete/<int:gr_id>", methods=["DELETE"])
def delete_guestroom(gr_id):

    if not gr_id:
        return jsonify({"code": 0, "message": "参数错误"})
    try:

        db.session.query(GuestRoom).filter(GuestRoom.gr_id == gr_id).delete()
        db.session.commit()
        return jsonify({"code": 1, "message": "客房删除成功"})

    except exc.IntegrityError:
        db.session.rollback()

    return jsonify({"code": 0, "message": "客房删除失败"})


#根据客户主键查询客房
@api.route("/api/v1.0/get_guestroom_by_gr_id/<int:gr_id>",methods=['GET'])
def get_guestroom_by_gr_id(gr_id):
    try:
        entity = db.session.query(GuestRoom).filter(GuestRoom.gr_id == gr_id).first()
        return jsonify({"code":1,"message":entity.to_json()})
    except:
        return jsonify({"code":0,"message":"查询失败"})
    return jsonify({"code":0,"message":"查询异常"})



# 根据房源类型,查询所有客房列表,返回JSON
@api.route("/api/v1.0/get_guestroom_by_hsId/<int:hs_id>", methods=["GET"])
def get_guestroom_by_hsId(hs_id):
    if not hs_id:
        return jsonify({"code": 0, "message": "参数错误"})

    room_lists = db.session.query(GuestRoom).filter(GuestRoom.hs_id == hs_id).all()

    return jsonify({"code": 1, "message": [entity.to_json() for entity in room_lists]})

@api.route("/api/v1.0/change_status_by_gr_id/<int:gr_id>", methods=["PUT"])
def change_status_by_gr_id(gr_id):
    if not gr_id:
        return jsonify({"code": 0, "message": "参数错误hs_id"})
    gr_status = request.get_json().get("gr_status")
    if int(gr_status)>2:
        return jsonify({"code": 0, "message": "gr_status"})
    try:
        db.session.query(GuestRoom).filter(GuestRoom.gr_id == gr_id).update({
            "gr_status": gr_status
        })
        db.session.commit()
        return jsonify({"code": 1, "message": "状态更新成功"})
    except exc.IntegrityError:
        db_session.rollback()
        return jsonify({"code": 0, "message": "状态更新失败"})

# 根据房间类型,查询所有客房列表,返回JSON
# @api.route("/api/v1.0/get_guestroom_by_rtId/<int:rt_id>", methods=["GET"])
# def get_guestroom_by_rtId(rt_id):
#     if not rt_id:
#         return jsonify({"code": 0, "message": "参数错误"})
#
#     room_lists = db_session.query(GuestRoom).filter(GuestRoom.rt_id == rt_id).all()
#
#     return jsonify({"code": 1, "message": [guestroom.to_json() for guestroom in room_lists]})


@api.route("/api/v1.0/get_all_rooms_by_hs_id/<int:hs_id>/<int:page>")
def get_all_rooms_by_hs_id(hs_id,page):
    if not hs_id:
        return jsonify({"code": 0, "message": "参数错误"})
    pagesize = 10
    try:
        pagination = GuestRoom.query.filter(GuestRoom.hs_id==hs_id).order_by(GuestRoom.gr_id.desc()).\
            paginate(page, per_page=pagesize,error_out=False)
        pages = pagination.pages  # 总页数
        total = pagination.total  # 总记录数
        entities = pagination.items
        return jsonify({"code": 1, "page": page, "pages": pages, "total": total,
                        "message": [entity.to_json() for entity in entities]})
    except:
        return jsonify({"code": 0, "message": "查询失败"})

#查询该房源下的所有客房的个数
#@api.route("api/v1.0/get_count_by_hs_id",methods=['GET'])

#根据客房名称搜索
@api.route("/api/v1.0/findbygrname/<string:gr_name>", methods=['GET'])
def findbygrname(gr_name):
    if not gr_name:
        return jsonify({"code": 0, "message": "客房不存在"})
    try:
        entities = db.session.query(GuestRoom).filter_by(GuestRoom.gr_name.like('%'+gr_name+'%')).all()
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
        entities = db.session.query(GuestRoom).filter_by(GuestRoom.gr_price <= gr_price).all()
        return jsonify({"code": 1, "message": [entity.to_json() for entity in entities]})
    except:
        return jsonify({"code": 0, "message": "暂无数据"})
    return jsonify({"code":0,"message":"查询异常"})
