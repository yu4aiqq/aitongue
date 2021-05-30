# @Time  :2021/5/13 14:52
# @Author:Sleet
# @File  :profile.py

from . import api
from flask import request, jsonify
from lg_aitongue.models import WechatInfo, UserInfo
from lg_aitongue.response_code import RET
from lg_aitongue import db
import logging


@api.route('/user_info', methods=['POST'])
def save_user_info():
    """
    保存用户个人信息
    :param wechat_id: 用户微信id
    :return: json
    """
    # 接收参数
    try:
        user_info_dict = request.get_json()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.PAPAMERR, errmsg='获取参数失败')

    wechat_id = user_info_dict.get('wechat_id')
    gender = user_info_dict.get('gender')
    age = user_info_dict.get('age')
    height = user_info_dict.get('height')
    weight = user_info_dict.get('weight')
    area = user_info_dict.get('area')
    medical_history = user_info_dict.get('medical_history')

    # 校验参数
    if not all(['wechat_id', 'gender', 'age', 'height', 'weight', 'area', 'medical_history']):
        return jsonify(errno=RET.PAPAMERR, errmsg='参数不完整')

    # 判断用户是否存在
    try:
        wechat = WechatInfo.query.filter_by(openid=wechat_id).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='search wechat error')

    if not wechat:
        return jsonify(errno=RET.NOUSER, errmsg='no wechat')

    user = wechat.user
    # 有个人信息时更新，无个人信息时写入
    if user:
        # 要保存的数据
        user_info_update = {
            'gender': gender,
            'age': age,
            'height': height,
            'weight': weight,
            'area': area,
            'medical_history': medical_history
        }

        # 更新用户个人信息
        try:
            UserInfo.query.filter_by(wechat_id=wechat_id).update(user_info_update)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='update user info error')
    if not user:
        # 要写入的数据
        user_info = UserInfo(
            wechat_id=wechat_id,
            gender=gender,
            age=age,
            height=height,
            weight=weight,
            area=area,
            medical_history=medical_history
        )
        # 写入数据
        try:
            db.session.add(user_info)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='save user info error')

    return jsonify(errno=RET.OK, errmsg='save user info success')
