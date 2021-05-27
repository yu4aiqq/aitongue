# @Time  :2021/5/13 20:47
# @Author:Sleet
# @File  :scale.py


from . import api
from flask import request, jsonify
from lg_aitongue.response_code import RET
from lg_aitongue.models import WechatInfo, Scale
from lg_aitongue import db
import logging


@api.route('/save_scale_info/<wechat_id>', methods=['POST'])
def save_scale_info(wechat_id):
    """
    保存用户的量表信息
    :param wechat_id: 用户微信id
    :return: json
    """
    # 获取参数
    try:
        scale_dict = request.get_json()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.PAPAMERR, errmsg='获取参数失败')

    body = scale_dict.get('body')
    sweat = scale_dict.get('sweat')
    pain = scale_dict.get('pain')
    excretion = scale_dict.get('excretion')
    spirit = scale_dict.get('spirit')
    skin = scale_dict.get('skin')
    mouth = scale_dict.get('mouth')
    immune = scale_dict.get('immune')
    breath = scale_dict.get('breath')
    others = scale_dict.get('others')

    # 校验参数
    if not all(['body', 'sweat', 'pain', 'excretion', 'spirit', 'skin', 'mouth', 'immune', 'breath', 'others']):
        return jsonify(errno=RET.PAPAMERR, errmsg='参数错误')

    # 查询用户是否存在
    try:
        wechat = WechatInfo.query.filter_by(openid=wechat_id).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='search wechat error')

    if not wechat:
        return jsonify(errno=RET.NOUSER, errmsg='wechat id not exist')

    # 保存图片信息
    # 超过五条记录就进行覆盖
    try:
        scale_num = Scale.query.filter_by(wechat_id=wechat_id).count()
        longest_time_scale = Scale.query.filter_by(wechat_id=wechat_id).order_by(Scale.update_time).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='search scale info error')

    if scale_num == 5:
        # 要更新的数据
        scale_update = {
            'body': body,
            'sweat': sweat,
            'pain': pain,
            'excretion': excretion,
            'spirit': spirit,
            'skin': skin,
            'mouth': mouth,
            'immune': immune,
            'breath': breath,
            'others': others
        }
        longest_time = longest_time_scale.update_time
        # 更新数据
        try:
            Scale.query.filter(Scale.wechat_id == wechat_id, Scale.update_time == longest_time).update(scale_update)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='update scale info error')
    else:
        # 要写入的数据
        scale = Scale(
            wechat_id=wechat_id,
            body=body,
            sweat=sweat,
            pain=pain,
            excretion=excretion,
            spirit=spirit,
            skin=skin,
            mouth=mouth,
            immune=immune,
            breath=breath,
            others=others
        )
        # 写入数据
        try:
            db.session.add(scale)
            db.session.commit()
        except Exception as e:
            # 这里是数据库操作异常后，能够进行回滚，防止错误写入
            db.session.rollback()
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='save scale info error')

    return jsonify(errno=RET.OK, errmsg='save scale info success')


# @api.route('/get_scale_info/<user_id>', methods=['GET'])
# def get_scale_info(user_id):
#     """
#     获取用户的量表信息
#     :param user_id: 用户微信id
#     :return: 用户的量表信息
#     """
#     # 判断用户是否存在
#     try:
#         user = UserInfo.query.filter_by(openid=user_id).first()
#     except Exception as e:
#         logging.error(e)
#         return jsonify(errno=RET.DBERR, errmsg='search error')
#
#     if not user:
#         return jsonify(errno=RET.NOUSER, errmsg='用户不存在')
#
#     if not all([user.gender, user.age, user.height, user.weight, user.area, user.medical_history]):
#         return jsonify(errno=RET.NODATA, errmsg='用户个人信息不完整')
#
#     scales = user.scales
#     if not scales:
#         return jsonify(errno=RET.NODATA, errmsg='未填写量表信息')
#
#     try:
#         scale = Scale.query.filter_by(user_id=user_id).order_by(Scale.update_time.desc()).first()
#     except Exception as e:
#         logging.error(e)
#         return jsonify(errno=RET.DBERR, errmsg='search scale info error')
#     # print(scale)
#     # print(scale.scale_to_dict())
#     # print(scale.body)
#
#     return jsonify(errno=RET.OK, errmsg='search scale info success', data=scale.scale_to_dict())
