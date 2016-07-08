# coding:utf-8
import hashlib
import time
from functools import wraps
from flask import jsonify, request, g, current_app

from service_api.model import HouseOwner, db_session
from . import api

#redis 需要安装python支持库=>sudo pip install redis

#
# app = Flask(__name__)

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
# redis_store = redis.StrictRedis(host=Conf.REDIS_HOST, port=Conf.REDIS_PORT, db=Conf.REDIS_DB, password=Conf.REDIS_PASSWORD)
#在此之前设置config

def login_check(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get("token")
        if not token:
            return jsonify({"code": 0, "message": "token错误,需要验证"})
        ho_account = current_app.redis.get("token:%s" % token)
        tokenfrmredis = current_app.redis.hget('user:%s' % ho_account.decode('utf8'), 'token')

        if not ho_account or token.encode(encoding="utf8") != tokenfrmredis:
            return jsonify({'code': 2, 'message': '验证信息错误'})
        return func(*args, **kwargs)

    return decorator

@api.before_request
def before_request():
    token = request.headers.get("token")
    if token:
        account = current_app.redis.get("token:%s" % token)
        # print(account)
        if not account:
            account = account.encode("utf8")
        g.current_user = db_session.query(HouseOwner).filter(HouseOwner.ho_account == account).one()
        g.token = token
    return



# @app.route('/api/v1.0/horegister', methods=['POST'])
# def house_owner_register():
#     if not request.json or not 'honame' in request.json:
#         return jsonify({'code': 0,'message':'请填写您的真实姓名'})
#     if not request.json or not 'hoaccount' in request.json:
#         return jsonify({'code': 0, 'message': '请填写您的账号'})
#     if not request.json or not 'homobile' in request.json:
#         return jsonify({'code': 0, 'message': '请填写您的手机号'})
#     if not request.json or not 'honicard' in request.json:
#         return jsonify({'code': 0, 'message': '请提交您的身份证'})
#
#     task={
#         'honame':request.json['honame'],
#         'hoaccount': request.json['hoaccount'],
#         'hotel': request.json['hotel'],
#         'homobile': request.json['homobile'],
#         'hoemail': request.json['hoemail'],
#         'honicard': request.json['honicard'],
#         'hoimage': request.json['hoimage']
#     }
#
#     return jsonify({'code': 1, 'message': '注册成功', "ho_owner": task})

@api.route("/api/v1.0/ho_register",methods = ["POST"])
def ho_register():
    house_owner = {
        "ho_name":request.get_json().get("ho_name"),
        "ho_account":request.get_json().get("ho_account"),
        "ho_password":request.get_json().get("ho_password"),
        "ho_tel":request.get_json().get("ho_tel"),
        "ho_mobile":request.get_json().get("ho_mobile"),
        "ho_nicard":request.get_json().get("ho_nicard"),
        "ho_image":request.get_json().get("ho_image"),
        "ho_email":request.get_json().get("ho_email")
    }
    db_session.add(house_owner)
    db_session.commit()
    return jsonify({"code":1,"message":"恭喜您注册成功"})


@api.route("/api/v1.0/ho_login", methods=["POST"])
def house_owner_login():

    ho_account = request.get_json().get("ho_account")
    ho_password = request.get_json().get("ho_password")

    houseowner = db_session.query(HouseOwner).filter(HouseOwner.ho_account == ho_account).first()
    if not houseowner:
        return jsonify({'code': 0, 'message': '没有此用户'})

    if houseowner.ho_password != ho_password:
        return jsonify({'code': 0, 'message': '密码错误'})

    # m = hashlib.md5()
    # m.update(ho_account.encode("utf8"))
    # m.update(ho_password.encode("utf8"))
    # m.update(str(int(time.time())).encode("utf8"))
    # token = m.hexdigest()


    # redis_store.hmset("user:%s" % ho_account, {"token": token, "online": 1})
    # redis_store.set("token:%s" % token, ho_account)
    # redis_store.expire("token:%s" % token, 3600*5)

    # 为防止传输过程中出错,改用管道
    # pipeline = current_app.redis.pipeline()
    # pipeline.hmset("user:%s" % ho_account, {"token": token, "online": 1})
    # pipeline.set("token:%s" % token, ho_account)
    # pipeline.expire("token:%s" % token, 3600*5)
    # pipeline.execute()

    return jsonify({'code': 1, 'message': '成功登录', 'acount': ho_account, 'token': token})

@api.route("/api/v1.0/get_ho_by_token")
@login_check
def get_house_owner():
    current_user = g.current_user
    # 通过redis中取出的账号查找mysql 数据库,返回该账号其他资料
    entity = db_session.query(HouseOwner).filter(HouseOwner.ho_account == current_user.ho_account).one()
    # print(entity.ho_name)
    db_session.close()

    #return json.dumps(entity.to_json(), ensure_ascii=False)
    return jsonify({'code': 1, 'ho_id': entity.ho_id, 'ho_name': entity.ho_name, 'ho_email': entity.ho_email, 'message': '操作成功', 'token': g.token})

@api.route("/api/v1.0/logout")
@login_check
def logout():

    current_user = g.current_user

    pipeline = current_app.redis.pipeline()
    pipeline.delete("token:%s" % g.token)
    pipeline.hmset("user:%s" % current_user.ho_account, {"online": 0})
    pipeline.execute()
    '''
    127.0.0.1:6379> hget user:jsonwang token
    "61e35e6c30f3b51a2e8e45c4016f98ea"
    127.0.0.1:6379> keys *
    1) "user:jsonwang"
    127.0.0.1:6379> hget user:jsonwang token
    "61e35e6c30f3b51a2e8e45c4016f98ea"
    127.0.0.1:6379> hget user:jsonwang online
    "0"
    '''
    return jsonify({"code": 1, "message": "注销成功"})


@api.teardown_request
def handle_teardown_request(exception):
    db_session.remove()

# if __name__ == "__main__":
#     app.run(host=Conf.SERVICE_HOST, port=Conf.SERVICE_PORT, debug=Conf.DEBUG)