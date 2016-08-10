from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.models.model import GuestRoom, db_session
from . import api
from sqlalchemy import exc


#   添加删除图片
@api.route("/api/v1.0/save_delete_image", methods=["POST"])
def save_delete_image():
    image = request.json.get("image")
    del_image = DeleteImages()
    del_image.image = image
    try:
        db_session.add(del_image)
        db_session.commit()
        return jsonify({"code": 1, "message": "添加成功"})
    except exc.IntegrityError:
        db_session.rollback()

    return jsonify({"code": 0, "message": "添加失败"})
