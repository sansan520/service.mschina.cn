# coding:utf-8
import datetime
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String, DateTime, \
    DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from service_api.config import Conf

engine = create_engine(Conf.MYSQL_INFO, pool_recycle=7200)

Base = declarative_base()

db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False, bind=engine))

#Base.query = db_session.query_property()

# 创建数据表
class HouseOwner(Base):

    __tablename__ = 'houseowner'

    ho_id = Column('ho_id', Integer, primary_key=True)
    ho_name = Column('ho_name', String(45), index=True, nullable=False)
    ho_account = Column('ho_account', String(45), index=True, nullable=False)
    ho_password = Column('ho_password', String(45), nullable=False)
    ho_tel = Column('ho_tel', String(45))
    ho_mobile = Column('ho_mobile', String(45), nullable=False)
    ho_email = Column('ho_email', String(45))
    ho_nicard = Column('ho_nicard', String(100), nullable=False)
    ho_images = Column('ho_images', String(100))

    ho_createtime = Column('ho_createtime', DateTime, default=datetime.datetime.now)
    ho_modifytime = Column('ho_modifytime', DateTime, default=datetime.datetime.now)

    def to_json(self):
        return {
            'ho_id': self.ho_id,
            'ho_name': self.ho_name,
            'ho_password':self.ho_password,
            'ho_tel': self.ho_tel,
            'ho_mobile':self.ho_mobile
        }

class HouseType(Base):

    __tablename__ = "housetype"

    ty_id = Column('ty_id', Integer, primary_key=True)
    ty_name = Column('ty_name', String(45), nullable=False)
    ty_valume =Column('ty_valume', Integer, default=0)

# 房源表
class HouseResources(Base):

    __tablename__ = "houseresources"

    hs_id = Column('hs_id', Integer, primary_key=True)
    ty_id = Column('ty_id', Integer, ForeignKey('housetype.ty_id'))
    ho_id = Column('ho_id', Integer, ForeignKey('houseowner.ho_id', ondelete='CASCADE'))
    hs_intro = Column('hs_intro', String(500))
    hs_province = Column('hs_province', String(50))
    hs_city = Column('hs_city', String(50))
    hs_country = Column('hs_country', String(50))
    hs_address = Column('hs_address', String(50))
    hs_hitvalume = Column('hs_hitvalume', String(50))
    hs_images = Column('hs_images', String(500))


class RoomType(Base):

    __tablename__ = "roomtype"

    rt_id = Column('rt_id', Integer, primary_key=True)
    rt_name = Column('rt_name', String(50), nullable=False)


class GuestRoom(Base):

    __tablename__ = "guestroom"

    gt_id = Column('gt_id', Integer, primary_key=True)
    hs_id = Column('hs_id', Integer, ForeignKey('houseresources.hs_id', ondelete='CASCADE'))
    rt_id = Column('rt_id', Integer)
    gt_price = Column('gt_price', DECIMAL(10, 2))
    gt_describe = Column('gt_describe', String(500))

if __name__ == '__main__':
    Base.metadata.create_all(engine)


#http://www.cnblogs.com/yueerwanwan0204/p/5327912.html