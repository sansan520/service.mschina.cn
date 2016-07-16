# # coding:utf-8
# from . import api
# from service_api.models.model_new import HouseType, db, HouseResources
# from functools import wraps
# from flask import jsonify,request
# from sqlalchemy import exc
#
# @api.route("/api/v2.0/get_all_ht")
# def get_all_housetype():
#
#     housetypes = HouseType.query.all()
#
#     return jsonify({"code": 1, "message": [housetype.to_json() for housetype in housetypes]})
#
#
# @api.route("/api/v2.0/ht_insert", methods=["POST"])
# def insert_housetype2():
#
#     t_name = request.json["ty_name"]
#     if not t_name:
#         return jsonify({"code": 0, "message": "类型不能为空"})
#
#     house_type = HouseType()
#     house_type.ty_name = t_name
#     house_type.ty_valume = 0
#
#     try:
#         db.session.add(house_type)
#         db.session.commit()
#         return jsonify({"code": 1, "message": "类型添加成功"})
#     except exc.IntegrityError:
#         db.session.rollback()
#
#     return jsonify({"code": 0, "message": "类型添加失败"})
#
# @api.route("/api/v2.0/ht_delete/<int:ty_id>", methods=["DELETE"])
# def delete_housetype2(ty_id):
#
#     if not ty_id:
#         return jsonify({"code": 0, "message": "参数错误"})
#     try:
#         house_type = HouseType.query.get(ty_id)
#         db.session.delete(house_type)
#         db.session.commit()
#
#         return jsonify({"code": 1, "message": "类型删除成功"})
#
#     except exc.IntegrityError:
#         db.session.rollback()
#
#     return jsonify({"code": 0, "message": "类型删除失败"})
#
#
# @api.route("/api/v2.0/ht_update/<int:ty_id>", methods=["PUT"])
# def update_housetype2(ty_id):
#
#     if not ty_id:
#         return jsonify({"code": 0, "message": "参数错误"})
#
#     ty_name = request.json["ty_name"]
#     if not ty_name:
#         return jsonify({"code": 0, "message": "参数错误"})
#
#     try:
#         # db_session.query(HouseType).filter(HouseType.ty_id == ty_id).update({
#         #     "ty_name": ty_name
#         # })
#         # HouseType.query.get(ty_id).update({"ty_name": ty_name})
#         db.session.query(HouseType).filter(HouseType.ty_id == ty_id).update({
#             "ty_name": ty_name
#         })
#         db.session.commit()
#         return jsonify({"code": 1, "message": "类型更新成功"})
#     except exc.IntegrityError:
#         db_session.rollback()
#     return jsonify({"code": 0, "message": "类型更新失败"})
#
# #  分页查询  http://www.cnblogs.com/agmcs/p/4445583.html
# @api.route("/api/v2.0/get_res_page")
# @api.route("/api/v2.0/get_res_page/<int:page>")
# def get_page_resources(page=1):
#
#     pagination = HouseResources.query.order_by(HouseResources.hs_id.desc()).paginate(page, per_page=6, error_out=False)
#
#     entities = pagination.items
#     totalpages = pagination.pages  # 总页数
#     sums = pagination.total  # 总记录数
#     return jsonify({"code": 1, "totalPages": totalpages, "sums":sums, "message": [entity.to_json() for entity in entities]})