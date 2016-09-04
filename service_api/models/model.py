# -*- coding: utf-8 -*-
import datetime
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime, \
    DECIMAL
from sqlalchemy.orm import sessionmaker, scoped_session
import os,sys
#parentdir  父目录
granddir =os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, granddir)
parentdir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, parentdir)

# print(sys.path)
from service_api.run import create_app
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app()
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], pool_recycle=7200)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=True, bind=engine))

# 会员基础表(游客/房东公共部分)
class UserBase(db.Model):

    __tablename__ = 'userbase'

    user_id = Column('user_id', Integer, primary_key=True, autoincrement=True)
    user_account = Column('user_account', String(45), index=True, nullable=False)
    user_password = Column('user_password', String(45), nullable=False)
    user_mobile = Column('user_mobile', String(45), nullable=False)
    user_headimg = Column('user_headimg', String(100))
    user_type = Column('user_type', Integer, nullable=False)  # 0房东，1游客
    user_status = Column('user_status', Integer, nullable=False) # 默认1:正常,0 被管理员禁止(删除)

    user_createtime = Column('user_createtime', DateTime, default=datetime.datetime.now)
    user_modifytime = Column('user_modifytime', DateTime, default=datetime.datetime.now)

    houseowner = db.relationship('HouseOwner', backref='userbase', lazy='dynamic')


    def to_json(self):
        return {
            'user_id': self.user_id,
            'user_account': self.user_account,
            'user_password':self.user_password,
            'user_mobile': self.user_mobile,
            'user_headimg': self.user_headimg,
            'user_type': self.user_type,
            'user_status':self.user_status,
            'user_createtime':self.user_createtime.strftime('%Y-%m-%d %H:%M:%S'),
            'user_modifytime':self.user_modifytime.strftime('%Y-%m-%d %H:%M:%S')
        }

class UserBase_Ext(UserBase):
    ho_id = Column('ho_id', Integer)
    def to_json(self):
        return {
            'user_id': self.user_id,
            'user_account': self.user_account,
            'user_password': self.user_password,
            'user_mobile': self.user_mobile,
            'user_headimg': self.user_headimg,
            'user_type': self.user_type,
            'user_status': self.user_status,
            'user_createtime': self.user_createtime.strftime('%Y-%m-%d %H:%M:%S'),
            'user_modifytime': self.user_modifytime.strftime('%Y-%m-%d %H:%M:%S'),
            'ho_id':self.ho_id
        }

# 房东表(用户扩展表,若想成为房东就需要提供更多资料)
class HouseOwner(db.Model):

    __tablename__ = 'houseowner'

    ho_id = Column('ho_id', Integer, primary_key=True, autoincrement=True)
    user_id = Column('user_id', Integer, ForeignKey('userbase.user_id'))   # 外键,唯一键unique=true
    ho_name = Column('ho_name', String(45), index=True, nullable=False)   # 真实姓名
    ho_tel = Column('ho_tel', String(45))    # 家庭电话
    ho_email = Column('ho_email', String(45))   # 邮箱
    ho_nicard = Column('ho_nicard', String(100), nullable=False)    # 身份证件照

    ho_createtime = Column('ho_createtime', DateTime, default=datetime.datetime.now)
    ho_modifytime = Column('ho_modifytime', DateTime, default=datetime.datetime.now)

    def to_json(self):
        return {
            'ho_id': self.ho_id,
            'user_id':self.user_id,
            'ho_name': self.ho_name,
            'ho_tel': self.ho_tel,
            'ho_email': self.ho_email,
            'ho_nicard': self.ho_nicard
        }

# 游客扩展表(以后可能需要预约登记之类的),就可以加扩展表,登记更多用户资料
# class Visitor(db.Model):
#     __tablename__ = 'visitor'
#
#     vi_id = Column('vi_id', Integer, primary_key=True, autoincrement=True)
#     user_id = Column('user_id', Integer, ForeignKey('userbase.user_id'))   # 外键


#  房源类型表
class HouseType(db.Model):

    __tablename__ = "housetype"

    ty_id = Column('ty_id', Integer, primary_key=True, autoincrement=True)
    ty_name = Column('ty_name', String(45), nullable=False)
    ty_valume =Column('ty_valume', Integer, default=0)


    def to_json(self):
        house_type = {
            'ty_id': self.ty_id,
            'ty_name': self.ty_name,
            'ty_valume': self.ty_valume
        }
        return house_type

# 房源表
class HouseResources(db.Model):

    __tablename__ = "houseresources"

    hs_id = Column('hs_id', Integer, primary_key=True, autoincrement=True)
    ty_id = Column('ty_id', Integer, ForeignKey('housetype.ty_id'))
    user_id = Column('user_id', Integer, ForeignKey('userbase.user_id', ondelete='CASCADE'))
    hs_name = Column('hs_name', String(20))   # 房源名称
    hs_intro = Column('hs_intro', String(500))
    hs_province = Column('hs_province', String(20))
    hs_city = Column('hs_city', String(20))
    hs_country = Column('hs_country', String(20))
    hs_address = Column('hs_address', String(50))
    hs_hitvalume = Column('hs_hitvalume', Integer)    # 点击量
    hs_images = Column('hs_images', String(500))
    hs_status = Column('hs_status',Integer)  #  房源状态, 0 表示暂停营业,1 表示正常营业
    hs_createtime = Column('hs_createtime', DateTime, default=datetime.datetime.now())
    hs_modifytime = Column('hs_modifytime', DateTime, default=datetime.datetime.now())

    def to_json(self):
        return {
            'hs_id': self.hs_id,
            'ty_id': self.ty_id,
            'user_id': self.user_id,
            'hs_name':self.hs_name,
            'hs_province': self.hs_province,
            'hs_city': self.hs_city,
            'hs_country': self.hs_country,
            'hs_address': self.hs_address,
            'hs_hitvalume':self.hs_hitvalume,
            'hs_images': self.hs_images,
            'hs_status':self.hs_status,
            'hs_intro':self.hs_intro
        }

# 客房类型表
# class RoomType(db.Model):
#
#     __tablename__ = "roomtype"
#
#     rt_id = Column('rt_id', Integer, primary_key=True)
#     rt_name = Column('rt_name', String(50), nullable=False)


# 客房表
class GuestRoom(db.Model):

    __tablename__ = "guestroom"

    # 客房基本信息
    gr_id = Column('gr_id', Integer, primary_key=True, autoincrement=True)
    hs_id = Column('hs_id', Integer, ForeignKey('houseresources.hs_id', ondelete='CASCADE'))

    gr_name = Column('gr_name', String(100))    # 客房名称
    gr_price = Column('gr_price', DECIMAL(10, 2))
    gr_desc = Column('gr_desc', String(500))   # 简单描述
    gr_images = Column('gr_images', String(500))
    gr_status = Column('gr_status', Integer)    #admin:0表示审核中,1 正常(审核通过),2 房东停止发布
    gr_createtime = Column('gr_createtime',DateTime,default=datetime.datetime.now())
    gr_modifytime = Column('gr_modifytiem',DateTime,default=datetime.datetime.now())

    # 详细信息
    gr_room_type = Column('gr_room_type', Integer)  # 1,2,...6 人间
    gr_room_area = Column('gr_room_area', Integer)  # 面积:30 (平方米)
    gr_bed_type = Column('gr_bed_type', String(50)) # 单人床
    gr_bed_count = Column('gr_bed_count', Integer)
    gr_windows = Column('gr_windows', Integer)
    gr_breakfast = Column('gr_breakfast', Integer)
    gr_settings = Column('gr_settings', String(500))


    def to_json(self):
        return {
            'gr_id': self.gr_id,
            'hs_id': self.hs_id,
            'gr_name':self.gr_name,
            'gr_price': float(self.gr_price),
            'gr_modifytime':self.gr_modifytime.strftime('%Y-%m-%d %H:%M:%S'),
            'gr_desc': self.gr_desc,
            'gr_images':self.gr_images,
            'gr_room_type':self.gr_room_type,
            'gr_room_area': self.gr_room_area,
            'gr_bed_type': self.gr_bed_type,
            'gr_bed_count': self.gr_bed_count,
            'gr_windows': self.gr_windows,
            'gr_breakfast': self.gr_breakfast,
            'gr_settings': self.gr_settings
        }


# 客房预订表
class Reserve(db.Model):

    __tablename__ = "reserve"

    id = Column('id',Integer,primary_key=True,autoincrement=True)
    gr_id = Column('gr_id',Integer,ForeignKey('guestroom.gr_id'),nullable=False)
    user_id = Column('user_id',Integer,ForeignKey('userbase.user_id'),nullable=False)
    start_time = Column('start_time',DateTime)
    end_time = Column('end_time',DateTime)
    status = Column('status',Integer,nullable=False)  # 订单状态 0 已取消(退订) 1 预订 2 房东确认
    create_time = Column('create_time', DateTime,default=datetime.datetime.now())
    modify_time = Column('modify_time',DateTime,default=datetime.datetime.now())

    def to_json(self):
        return {
            'id': self.id,
            'gr_id': self.gr_id,
            'user_id': self.user_id,
            'start_time': self.start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'end_time': self.end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'status': self.status,
            'create_time': self.gr_images.strftime('%Y-%m-%d %H:%M:%S'),
            'modify_time':self.modify_time.strftime('%Y-%m-%d %H:%M:%S')
        }

class DeleteImages(db.Model):

    __tablename__ = "deleteimages"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    image = Column('image', String(100))


if __name__ == '__main__':
    db.create_all()
    manager.run()


#http://www.cnblogs.com/yueerwanwan0204/p/5327912.html