# @Time  :2021/5/15 16:24
# @Author:Sleet
# @File  :login.py


from . import api
from flask import request, jsonify
from lg_aitongue.response_code import RET
from lg_aitongue.models import WechatInfo
from lg_aitongue import db
import logging
import requests


@api.route('/login', methods=['POST'])
def login():
    """
    用户登录
    :return: openid 用户唯一凭证
    """
    appid = 'wx6071c183594a411b'    # 小程序的appid
    secret = 'c1b38d99cfe3702ff4f0e1e60c2e2d59'    # 小程序的secretkey
    # 获取参数
    code = request.get_json()['code']
    # 请求地址
    url = f'https://api.weixin.qq.com/sns/jscode2session?appid={appid}&secret={secret}&js_code={code}&grant_type=authorization_code'
    # 获取openid
    try:
        res = requests.get(url)
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.THIRDERR, errsmg='第三方系统异常')
    openid = res.json().get('openid')

    # 查询openid是否已存在
    try:
        wechat = WechatInfo.query.filter_by(openid=openid).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='search wechat info error')

    if not wechat:
        # 要保存的信息
        wechat = WechatInfo(
            openid=openid
        )
        # 写入数据
        try:
            db.session.add(wechat)
            db.session.commit()
        except Exception as e:
            # 这里是数据库操作异常后，能够进行回滚，防止错误写入
            db.session.rollback()
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='save user id error')

    return jsonify(errno=RET.OK, errmsg='OK', data={'openid': openid})
