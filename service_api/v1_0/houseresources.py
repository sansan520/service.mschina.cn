from flask import jsonify,request,g,current_app
from sqlalchemy import exc
from service_api.model import db_session,HouseResources,HouseType,HouseOwner
from . import api
@api.route("/api/v1.0/hs_insert",methods = ["POST"])
def insert_houseresources():

    ho_resources = HouseResources()
    ho_id =request.get_json().get("ho_id")
    if not ho_id:
        return jsonify({"code":0,"message":"请先登录"})
    ty_id = request.get_json().get("ty_id")
    if not ty_id:
        return jsonify({"code":0,"message":"请先添加房源类型"})
    ho_resources.ho_id = HouseOwner.ho_id
    ho_resources.hs_intro = request.get_json().get("hs_intro")
    ho_resources.hs_province = request.get_json().get("hs_province")
    ho_resources.hs_city = request.get_json().get("hs_city")
    ho_resources.hs_country = request.get_json().get("hs_country")
    ho_resources.hs_address = request.get_json().get("hs_address")
    ho_resources.hs_images = request.get_json().get("hs_images")
    ho_resources.hs_hitvalume = 0
    db_session.add(ho_resources)
    db_session.commit()
    return jsonify({"code":1,"message":"房源添加成功"})