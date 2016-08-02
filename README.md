
已经添加了数据库管理库Flask-migrate

修改 model.py 表结构之后,执行步骤:
1) 在pycharm 编辑器中打开Termial
2) 执行migrate相关命令:生成数据表,更新数据表
  --> 1 python model.py db migrate
  --> 2 python model.py db upgrade

注意:
    如果报如下错误
    Traceback (most recent call last):
  File "model.py", line 14, in <module>
    from service_api.run import create_app
  File "/Users/HuaisanWang/Desktop/service.mschina.cn/service_api/run.py", line 5, in <module>
    from service_api.v1_0 import api as api_1_0_blueprint
  File "/Users/HuaisanWang/Desktop/service.mschina.cn/service_api/v1_0/__init__.py", line 8, in <module>
    from service_api.v1_0 import houseowner
  File "/Users/HuaisanWang/Desktop/service.mschina.cn/service_api/v1_0/houseowner.py", line 6, in <module>
    from service_api.model import HouseOwner, db_session
ImportError: No module named 'service_api.model'

 先将v1.0目录下的__init__.py,部分代码注销:如下
 # from service_api.v1_0 import houseowner
# from service_api.v1_0 import housetype
# from service_api.v1_0 import guestroom
# from service_api.v1_0 import houseresources
# from service_api.v1_0 import roomtype
#
#from service_api.v1_0 import test

待执行数据表更新成功之后,再把注销打开....
