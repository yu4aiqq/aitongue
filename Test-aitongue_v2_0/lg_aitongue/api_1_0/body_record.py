# @Time  :2021/5/3 15:56
# @Author:Sleet
# @File  :body_record.py


from . import api
from lg_aitongue.models import WechatInfo, Mouth
from flask import jsonify
from lg_aitongue.response_code import RET
import logging


@api.route('/body_record/<wechat_id>', methods=['GET'])
def get_record(wechat_id):
    """
    返回用户的体质记录
    :param wechat_id: 用户微信id
    :return: 用户的体质信息
    """
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
        records = Mouth.query.filter_by(wechat_id=wechat_id).order_by(Mouth.update_time.desc()).all()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='search error')

    # print(records)
    # 体质记录
    record_li = []
    for record in records:
        record_li.append(record.record_to_dict())

    # print(record_li)

    return jsonify(errno=RET.OK, errmsg='OK', data={'records': record_li})
