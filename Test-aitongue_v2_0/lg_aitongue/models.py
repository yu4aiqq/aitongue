# @Time  :2021/5/2 17:40
# @Author:Sleet
# @File  :models.py

from . import db
from datetime import datetime


class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间"""
    create_time = db.Column(db.DateTime, default=datetime.now)    # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)    # 记录的更新时间


class WechatInfo(BaseModel, db.Model):
    """微信用户信息"""

    __tablename__ = 'wechat_info'

    openid = db.Column(db.String(50), primary_key=True)    # 微信用户的openid
    user = db.relationship('UserInfo', backref='wechat', uselist=False)
    mouths = db.relationship('Mouth', backref='wechat')
    faces = db.relationship('Face', backref='wechat')
    scales = db.relationship('Scale', backref='wechat')


class UserInfo(BaseModel, db.Model):
    """用户自行填写的信息"""

    __tablename__ = 'user_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    # 记录编号
    wechat_id = db.Column(db.String(50), db.ForeignKey('wechat_info.openid'), nullable=False)    # 用户微信id
    gender = db.Column(db.Enum('男', '女'), nullable=False)    # 用户的性别
    age = db.Column(db.Integer, nullable=False)    # 用户年龄
    height = db.Column(db.Integer, nullable=False)    # 用户身高
    weight = db.Column(db.Integer, nullable=False)    # 用户体重
    area = db.Column(db.String(20), nullable=False)    # 用户常住区域
    medical_history = db.Column(db.TEXT)    # 用户病史


class Mouth(BaseModel, db.Model):
    """用户的舌诊信息"""

    __tablename__ = 'mouth_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    # 记录编号
    wechat_id = db.Column(db.String(50), db.ForeignKey('wechat_info.openid'), nullable=False)    # 用户id
    symptoms = db.Column(db.TEXT)    # 用户的症状
    body_type = db.Column(db.String(10))    # 用户体质
    result_img_url = db.Column(db.String(128))    # 诊断结果图片地址
    confidence = db.Column(db.String(10))    # 置信度
    date = db.Column(db.String(20))    # 诊断日期
    time = db.Column(db.String(10))    # 诊断时间

    def record_to_dict(self):
        """用字典呈现体质记录"""
        mouth_dict = {
            'body': self.body_type,
            'date': self.date,
            'time': self.time
        }
        return mouth_dict


class Face(BaseModel, db.Model):
    """用户的面诊信息"""

    __tablename__ = 'face_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    # 记录编号
    wechat_id = db.Column(db.String(50), db.ForeignKey('wechat_info.openid'), nullable=False)    # 用户id
    face_img_url = db.Column(db.String(128))    # 用户面部图片地址
    test = db.Column(db.Integer, default=0)    # 测试状态（0为测试数据，1为正式数据）


class Scale(BaseModel, db.Model):
    """用户的填写的量表信息"""

    __tablename__ = 'scale_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)    # 记录编号
    wechat_id = db.Column(db.String(50), db.ForeignKey('wechat_info.openid'), nullable=False)    # 用户id
    body = db.Column(db.TEXT)    # 用户近期身体冷热情况
    sweat = db.Column(db.TEXT)    # 用户近期出汗、油脂分泌情况
    pain = db.Column(db.TEXT)    # 用户近期身体疼痛、眩晕情况
    excretion = db.Column(db.TEXT)    # 用户近期排泄情况
    spirit = db.Column(db.TEXT)    # 用户近期精神状态
    skin = db.Column(db.TEXT)    # 用户近期皮肤状况
    mouth = db.Column(db.TEXT)    # 用户近期口腔、干渴情况
    immune = db.Column(db.TEXT)    # 用户近期身体免疫情况
    breath = db.Column(db.TEXT)    # 用户近期呼吸状况
    others = db.Column(db.TEXT)    # 用户近期其他状况
    test = db.Column(db.Integer, default=0)    # 测试状态（0为测试数据，1为正式数据）

    def scale_to_dict(self):
        """用字典呈现量表信息"""
        scale_dict = {
            'body': self.body,
            'sweat': self.sweat,
            'pain': self.pain,
            'excretion': self.excretion,
            'spirit': self.spirit,
            'skin': self.skin,
            'mouth': self.mouth,
            'immune': self.immune,
            'breath': self.breath,
            'others': self.others
        }
        return scale_dict


# class Admin(BaseModel, db.Model):
#     """管理员信息"""
#
#     __tablename__ = 'admin_info'
#
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)    # 记录编号
#     account = db.Column(db.String(50), nullable=False)    # 用户账号
#     password = db.Column(db.String(11), nullable=False)    # 用户密码
