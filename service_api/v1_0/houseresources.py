#coding:utf8
from flask import jsonify,request,g,current_app
from sqlalchemy import exc, desc
from service_api.models.model import db,db_session, HouseResources, HouseType, HouseOwner,HouseResources_Ext
from . import api

@api.route("/api/v1.0/hs_insert",methods = ["POST"])
def insert_houseresources():
    user_id =request.get_json().get("user_id")
    if not user_id:
        return jsonify({"code":0,"message":"请先登录"})
    ty_id = request.get_json().get("ty_id")
    if not ty_id:  # 前段添加房源(非admin),ty_id=1
        return jsonify({"code":0,"message":"房源类型错误"})  #  房东添加房源类型默认为0

    hs_name = request.get_json().get("hs_name")
    hs_intro = request.get_json().get("hs_intro")
    hs_province = request.get_json().get("hs_province")
    hs_city = request.get_json().get("hs_city")
    hs_country = request.get_json().get("hs_country")
    hs_address = request.get_json().get("hs_address")
    hs_images = request.get_json().get("hs_images")
    hs_status = request.get_json().get("hs_status")

    ho_resources = HouseResources()
    ho_resources.user_id = user_id
    ho_resources.ty_id = ty_id  #  初始化为1 ,当然类型表中得存在这个值
    ho_resources.hs_name = hs_name
    ho_resources.hs_intro = hs_intro
    ho_resources.hs_province = hs_province
    ho_resources.hs_city = hs_city
    ho_resources.hs_country = hs_country
    ho_resources.hs_address = hs_address
    ho_resources.hs_images = hs_images
    ho_resources.hs_hitvalume = 0
    ho_resources.hs_status = hs_status

    try:
        db.session.add(ho_resources)
        db.session.commit()
        return jsonify({"code":1,"message":"房源添加成功"})
    except exc.IntegrityError:
        return jsonify({"code":0,"message":"房源添加失败"})

@api.route("/api/v1.0/get_houseresources_by_hs_id/<int:hs_id>",methods=["GET"])
def get_houseresources_by_hs_id(hs_id):
    try:
        entity = db.session.query(HouseResources).filter(HouseResources.hs_id == hs_id).first()
        return jsonify({"code": 1, "message": entity.to_json()})
    except Exception:
      return jsonify({"code": 0, "message": "查询失败"})

#根据主键更新房源
@api.route("/api/v1.0/hs_edit/<int:hs_id>",methods=["PUT"])
def update_houseresources(hs_id):
    if not hs_id:
        return  jsonify({"code":0,"message":"房源不存在"})
    user_id = request.get_json().get("user_id")
    if not user_id:
        return jsonify({"code" : 0,"message":"参数错误"})
    ty_id = request.get_json().get("ty_id") # 前端添加房源(非admin),ty_id=1
    if not ty_id:   # # 前端添加房源(非admin),ty_id=1
        return jsonify({"code" : 0,"message":"参数错误"})
    hs_name = request.get_json().get("hs_name")
    hs_intro = request.get_json().get("hs_intro")
    hs_province = request.get_json().get("hs_province")
    hs_city = request.get_json().get("hs_city")
    hs_country = request.get_json().get("hs_country")
    hs_address = request.get_json().get("hs_address")
    hs_images = request.get_json().get("hs_images")
    #hs_hitvalume = request.get_json().get("hs_hitvalume")
    hs_status = request.get_json().get("hs_status")
    try:
        db.session.query(HouseResources).filter(HouseResources.hs_id == hs_id).update({
            "user_id":user_id,
            "ty_id":ty_id,
            "hs_name":hs_name,
            "hs_intro" : hs_intro,
            "hs_province" : hs_province,
            "hs_city" : hs_city,
            "hs_country" : hs_country,
            "hs_address" : hs_address,
            "hs_images" : hs_images,
            #"hs_hitvalume" : hs_hitvalume
            "hs_status":hs_status
        })
        db.session.commit()
        return jsonify({"code" : 1, "message" : "更新成功"})
    except exc.IntegrityError:
        db_session.rollback()
    return jsonify({"code":0,"message":"更新失败"})


# 查询用户名下的房源
@api.route("/api/v1.0/get_resource_by_user_id/<int:user_id>",methods=['GET'])
def get_resource_by_user_id(user_id):
    if not user_id:
        return jsonify({"code":0,"message":"用户不存在"})
    try:
        # entities = db_session.query(HouseOwner.ho_id,HouseResources).join(HouseOwner,HouseResources,HouseOwner.user_id == HouseResources.user_id).all()
        entities = db.session.query(HouseResources).filter(HouseResources.user_id == user_id).all()
        return jsonify({"code":1,"message":[entity.to_json() for entity in entities]})
    except exc.IntegrityError:
        return jsonify({"code":0,"message":"参数错误"})


#根据点击量更新用户的房源类型
@api.route("/api/v1.0/update_ty_id",methods=["PUT"])
def update_ty_id(ty_id):

    if not ty_id:
        return jsonify({"code":0,"message":"房源类型不存在"})
    try:
        db.session.update(HouseResources.ty_id).query(HouseType.ty_id).filter(HouseResources.hs_hitvalume == HouseType.ty_valume)
        db.session.commit()
        return jsonify({"code": 1, "message": "房源类型更新成功"})
    except exc.IntegrityError:
        return jsonify({"code":0,"message":"房源类型更新失败"})

@api.route("/api/v1.0/hs_delete/<int:hs_id>",methods = ["DELETE"])
def delete_houseresources(hs_id):

    if not hs_id:
        return jsonify({"code":0,"message":"参数错误"})
    try:

        db.session.query(HouseResources).filter(HouseResources.hs_id == hs_id).delete()
        db.session.commit()
        return jsonify({"code":1,"message":"删除成功"})
    except exc.IntegrityError:
        db_session.rollback()
        return jsonify({"code": 0, "message": "删除失败"})

@api.route("/api/v1.0/modify_status_by_hs_id/<int:hs_id>", methods=["PUT"])
def modify_status_by_hs_id(hs_id):

    if not hs_id:
        return jsonify({"code": 0, "message": "参数错误hs_id"})
    hs_status = request.get_json().get("hs_status")
    if not hs_status:
        return jsonify({"code": 0, "message": "参数错误hs_status"})
    try:
        db.session.query(HouseResources).filter(HouseResources.hs_id == hs_id).update({
            "hs_status": hs_status
        })
        db.session.commit()
        return jsonify({"code": 1, "message": "删除成功"})
    except exc.IntegrityError:
        db_session.rollback()
        return jsonify({"code": 0, "message": "删除失败"})

#  为首页获取3条热门房源
@api.route("/api/v1.0/get_hot_source4index")
def hot_resources_4_index():
    # ty_id =4 热门房源
    entities = db.session.query(HouseResources).filter(HouseResources.ty_id == 4).order_by(desc(HouseResources.hs_id)).limit(3).all()
    return jsonify({"code": 1, "message": [entity.to_json() for entity in entities]})

#  为首页获取5条特色房源
@api.route("/api/v1.0/get_special_resources4index")
def special_resources_4_index():
    # ty_id = 2
    entities = db.session.query(HouseResources).filter(HouseResources.ty_id == 2).order_by(
        desc(HouseResources.hs_id)).limit(5).all()
    return jsonify({"code": 1, "message": [entity.to_json() for entity in entities]})

#  为首页获取5条金牌房源
@api.route("/api/v1.0/get_goden_resources4index")
def goden_resources_4_index():
    # ty_id = 3
    entities = db.session.query(HouseResources).filter(HouseResources.ty_id == 3).order_by(
        desc(HouseResources.hs_id)).limit(5).all()
    return jsonify({"code": 1, "message": [entity.to_json() for entity in entities]})


#  分页查询 - 用于website (pagesize>10) http://www.cnblogs.com/agmcs/p/4445583.html
@api.route("/api/v1.0/get_res_page/<int:page>")
def get_res_page(page=1):
    pagesize = 6
    pagination = HouseResources.query.order_by(HouseResources.hs_id.desc()).paginate(page, per_page=pagesize, error_out=False)

    entities = pagination.items

    pages = pagination.pages  # 总页数
    total = pagination.total  # 总记录数

    return jsonify({"code": 1, "page": page, "pages": pages, "total": total, "message": [entity.to_json() for entity in entities]})

#  分页查询 - 用户admin
@api.route("/api/v1.0/get_all_houses/<int:page>")
def get_all_houses(page=1):
    pagesize = 10
    try:
        #pagination = HouseResources.query.order_by(HouseResources.hs_id.desc()).paginate(page, per_page=pagesize, error_out=False)
        querylist = HouseResources.query.join(HouseType, HouseResources.user_id == HouseType.ty_id). \
            join(HouseOwner, HouseResources.user_id == HouseOwner.user_id). \
            add_columns(HouseResources.hs_id, HouseResources.ty_id, HouseResources.hs_intro, HouseResources.hs_province,
                        HouseResources.hs_city, HouseResources.hs_country, HouseResources.hs_address,
                        HouseResources.hs_hitvalume,HouseResources.hs_name,HouseResources.hs_status,
                        HouseResources.hs_images, HouseResources.hs_createtime,HouseResources.user_id,
                        HouseResources.hs_modifytime, HouseOwner.ho_name, HouseType.ty_name). \
            order_by(HouseResources.hs_id.desc())

        pagination = querylist.paginate(page, per_page=pagesize,error_out=False)
        newEntities = []
        newItem = HouseResources_Ext()
        entities = pagination.items
        for entity in entities:
            newItem.hs_id = entity.hs_id
            newItem.ty_name = entity.ty_name
            newItem.ho_name = entity.ho_name
            newItem.hs_modifytime = entity.hs_modifytime
            newItem.ty_id = entity.ty_id
            newItem.hs_hitvalume = entity.hs_hitvalume
            newItem.hs_createtime = entity.hs_createtime
            newItem.hs_intro = entity.hs_intro
            newItem.hs_province = entity.hs_province
            newItem.hs_city = entity.hs_city
            newItem.hs_country = entity.hs_country
            newItem.hs_images = entity.hs_images
            newItem.hs_address = entity.hs_address
            newItem.hs_name = entity.hs_name
            newItem.hs_status = entity.hs_status
            newEntities.append(newItem)
        pages = pagination.pages  # 总页数
        total = pagination.total  # 总记录数

        return jsonify({"code": 1, "page": page, "pages": pages, "total": total,
                        "message": [entity.to_json() for entity in newEntities]})
    except:
        return jsonify({"code": 0, "message": "查询失败"})

#按省来查询
@api.route("/api/v1.0/findbyprovince/<string:hs_province>",methods=['GET'])
def findbyprovince(hs_province):
    if not hs_province:
        return jsonify({"code": 0, "message": "对不起，您搜索的省不存在"})
    try:
        entities = db.session.query(HouseResources).filter_by(HouseResources.hs_province == hs_province).all()
        return jsonify({"code": 1, "message":[entity.to_json() for entity in entities]})
    except:
        return jsonify({"code": 0, "message": "暂无数据"})
    return jsonify({"code": 0, "message": "查询异常"})

#按市来查询
@api.route("/api/v1.0/findbycity/<string:hs_city>", methods=['GET'])
def findbycity(hs_city):
    if not hs_city:
        return jsonify({"code": 0, "message": "对不起，您搜索的市不存在"})
    try:
        entities = db.session.query(HouseResources).filter_by(HouseResources.hs_city == hs_city).all()
        return jsonify({"code": 1, "message": [entity.to_json() for entity in entities]})
    except:
        return jsonify({"code": 0, "message": "暂无数据"})
    return jsonify({"code": 0, "message": "查询异常"})

#按区来查询
@api.route("/api/v1.0/findbycountry/<string:hs_country>", methods=['GET'])
def findbycountry(hs_country):
    if not hs_country:
        return jsonify({"code": 0, "message": "对不起，您搜索的市不存在"})
    try:
        entities = db.session.query(HouseResources).filter_by(HouseResources.hs_country == hs_country).all()
        return jsonify({"code": 1, "message": [entity.to_json() for entity in entities]})
    except:
        return jsonify({"code": 0, "message": "暂无数据"})
    return jsonify({"code": 0, "message": "查询异常"})







