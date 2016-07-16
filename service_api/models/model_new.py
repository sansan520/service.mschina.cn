# # -*- coding: utf-8 -*-
# import datetime
# import os,sys
# #parentdir  父目录
# granddir =os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.insert(0, granddir)
# parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.insert(1, parentdir)
# # print(sys.path)
# from service_api.run import create_app
# from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
#
# app = create_app()
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)
#
# # engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_recycle=7200)
# # db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
#
# # 用户基础表(游客/房东公共部分)
# class UserBase(db.Model):
#
#     __tablename__ = 'userbase'
#
#     user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_account = db.Column(db.String(45), index=True, nullable=False, unique=True)
#     user_password = db.Column(db.String(45), nullable=False)
#     user_mobile = db.Column(db.String(45), nullable=False)
#     user_headimg = db.Column(db.String(100))
#     user_type = db.Column(db.Integer, nullable=False)  # 0房东，1游客
#
#     user_createtime = db.Column(db.DateTime, default=datetime.datetime.now)
#     user_modifytime = db.Column(db.DateTime, default=datetime.datetime.now)
#
#     # houseowner = db.relationship('HouseOwner', backref='userbase', lazy='dynamic')
#
#
#     def to_json(self):
#         return {
#             'user_id': self.user_id,
#             'user_account': self.user_account,
#             'user_mobile': self.user_mobile,
#             'user_headimg': self.user_headimg,
#             'user_type': self.user_type
#         }
#
# # 房东表(用户扩展表,若想成为房东就需要提供更多资料)
# class HouseOwner(db.Model):
#
#     __tablename__ = 'houseowner'
#
#     ho_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('userbase.user_id'))   # 外键
#     ho_name = db.Column(db.String(45), index=True, nullable=False)   # 真实姓名
#     ho_tel = db.Column(db.String(45))    # 家庭电话
#     ho_email = db.Column(db.String(45))   # 邮箱
#     ho_nicard = db.Column(db.String(100), nullable=False)    # 身份证件照
#
#     ho_createtime = db.Column(db.DateTime, default=datetime.datetime.now)
#     ho_modifytime = db.Column(db.DateTime, default=datetime.datetime.now)
#
#     def to_json(self):
#         return {
#             'ho_id': self.ho_id,
#             'ho_name': self.ho_name,
#             'ho_tel': self.ho_tel,
#             'ho_email': self.ho_email,
#             'ho_images': self.ho_images
#         }
#
# # 游客扩展表(以后可能需要预约登记之类的),就可以加扩展表,登记更多用户资料
# # class Visitor(db.Model):
# #     __tablename__ = 'visitor'
# #
# #     vi_id = db.Column('vi_id', Integer, primary_key=True, autoincrement=True)
# #     user_id = db.Column('user_id', Integer, db.ForeignKey('userbase.user_id'))   # 外键
#
#
# #  房源类型表
# class HouseType(db.Model):
#
#     __tablename__ = "housetype"
#
#     ty_id = db.Column(db.Integer, primary_key=True)
#     ty_name = db.Column(db.String(45), nullable=False, unique=True)
#     ty_valume =db.Column(db.Integer, default=0)
#
#     # houseresources = db.relationship('HouseResources', backref='housetype', lazy='dynamic')
#
#     def to_json(self):
#         house_type = {
#             'ty_id': self.ty_id,
#             'ty_name': self.ty_name,
#             'ty_valume': self.ty_valume
#         }
#         return house_type
#
# # 房源表
# class HouseResources(db.Model):
#
#     __tablename__ = "houseresources"
#
#     hs_id = db.Column(db.Integer, primary_key=True)
#     ty_id = db.Column(db.Integer, db.ForeignKey('housetype.ty_id'))
#     ho_id = db.Column(db.Integer, db.ForeignKey('houseowner.ho_id', ondelete='CASCADE'))
#     hs_intro = db.Column(db.String(500))
#     hs_province = db.Column(db.String(50))
#     hs_city = db.Column(db.String(50))
#     hs_country = db.Column(db.String(50))
#     hs_address = db.Column(db.String(50))
#     hs_hitvalume = db.Column(db.String(50))
#     hs_images = db.Column(db.String(500))
#
#     hs_createtime = db.Column(db.DateTime, default=datetime.datetime.now())
#     hs_modifytime = db.Column(db.DateTime, default=datetime.datetime.now())
#
#     def to_json(self):
#         return {
#             'hs_id': self.hs_id,
#             'ty_id': self.ty_id,
#             'ho_id': self.ho_id,
#             'hs_province': self.hs_province,
#             'hs_city': self.hs_city,
#             'hs_country': self.hs_country,
#             'hs_address': self.hs_address,
#             'hs_hitvalume':self.hs_hitvalume,
#             'hs_images': self.hs_images
#         }
#
# # 客房类型表
# # class RoomType(db.Model):
# #
# #     __tablename__ = "roomtype"
# #
# #     rt_id = db.Column('rt_id', Integer, primary_key=True)
# #     rt_name = db.Column('rt_name', String(50), nullable=False)
#
#
#
# class GuestRoom(db.Model):
#
#     __tablename__ = "guestroom"
#
#     gr_id = db.Column(db.Integer, primary_key=True)
#     hs_id = db.Column(db.Integer, db.ForeignKey('houseresources.hs_id', ondelete='CASCADE'))
#     gr_name = db.Column(db.String(100))    # 客房名称
#     gr_price = db.Column(db.DECIMAL(10, 2))
#     gr_describe = db.Column(db.String(500))
#
#     def to_json(self):
#         return {
#             'gt_id': self.gt_id,
#             'hs_id': self.hs_id,
#             'gr_name':self.gr_name,
#             'gt_price': self.gt_price,
#             'gt_describe': self.gt_describe
#         }
#
# if __name__ == '__main__':
#     db.create_all()
#     manager.run()
#
#
# #http://www.cnblogs.com/yueerwanwan0204/p/5327912.html