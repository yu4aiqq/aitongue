# @Time  :2021/5/3 17:48
# @Author:Sleet
# @File  :result.py


from . import api
from lg_aitongue.models import WechatInfo, Mouth
from flask import jsonify, request
from lg_aitongue.response_code import RET
import logging


@api.route('/result', methods=['GET'])
def mouth_result():
    """
    返回用户的个人信息
    :param wechat_id: 用户微信id
    :return: 用户的个人信息
    """
    # 获取参数
    wechat_id = request.get_json()['wechat_id']
    
    # 校验参数
    if not wechat_id:
        return jsonify(errno=RET.PAPAMERR, errmsg='参数错误')

    # 查询用户是否存在
    try:
        wechat = WechatInfo.query.filter_by(openid=wechat_id).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='search wechat error')

    if not wechat:
        return jsonify(errno=RET.NOUSER, errmsg='wechat id not exist')

    # 查询数据库
    try:
        mouth = Mouth.query.filter_by(wechat_id=wechat_id).order_by(Mouth.update_time.desc()).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='search error')

    user_dict = dict(body=mouth.body_type)

    return jsonify(errno=RET.OK, errmsg='OK', data=user_dict)
