# coding:utf-8

from functools import wraps
from flask import jsonify, request, g, current_app
from service_api.model import HouseType, db_session
from . import api
from sqlalchemy import exc


@api.route("/api/v1.0/ht_insert", methods=["POST"])
def insert_housetype():

    t_name = request.get_json().get("ty_name")
    if not t_name:
        return jsonify({"code": 0, "message": "类型不能为空"})

    house_type = HouseType()
    house_type.ho_account = request.get_json().get("ho_account")
    house_type.ty_valume = 0

    try:
        db_session.add(house_type)
        db_session.commit()
        return jsonify({"code": 1, "message": "类型添加成功"})
    except exc.IntegrityError:
        db_session.rollback()

    return jsonify({"code": 0, "message": "类型添加失败"})

#
# @api.route("/api/v1.0/ht_update", methods=["PUT"])
# def update_housetype():

# @api.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
# def update_task(task_id):
#     task = filter(lambda t: t['id'] == task_id, tasks)
#     if len(task) == 0: abort(404)
#     if not request.json: abort(400)
#     if 'title' in request.json and type(request.json['title']) != unicode: abort(400)
#     if 'description' in request.json and type(request.json['description']) is not unicode: abort(400)
#     if 'done' in request.json and type(request.json['done']) is not bool: abort(400)
#     task[0]['title'] = request.json.get('title', task[0]['title'])
#     task[0]['description'] = request.json.get('description', task[0]['description'])
#     task[0]['done'] = request.json.get('done', task[0]['done'])
#     return jsonify({'task': task[0]})
#
# @api.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
# def delete_task(task_id):
#     task = filter(lambda t: t['id'] == task_id, tasks)
#     if len(task) == 0: abort(404)
#     tasks.remove(task[0])
#     return jsonify({'result': True})