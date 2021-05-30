# @Time  :2021/5/15 16:24
# @Author:Sleet
# @File  :login.py


from . import api
from flask import request, jsonify
from lg_aitongue.response_code import RET
from lg_aitongue.models import WechatInfo, Mouth, Face, UserInfo, Scale
from lg_aitongue import db
import logging
import requests


@api.route('/login', methods=['POST'])
def login():
    """
    用户登录
    :return: openid 用户唯一凭证
    """
    appid = 'your appid'    # 小程序的appid
    secret = 'you secretkey'    # 小程序的secretkey
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


@api.route('/logoff', methods=['DELETE'])
def logoff():
    """
    注销用户
    :return: JSON信息
    """

    # 获取参数
    wechat_id = request.get_json()['wechat_id']
    print(wechat_id)
    # 校验参数
    if not wechat_id:
        return jsonify(errno=RET.PAPAMERR, errmsg='参数错误')

    # 删除数据
    try:
        Mouth.query.filter_by(wechat_id=wechat_id).delete()
        Face.query.filter_by(wechat_id=wechat_id).delete()
        Scale.query.filter_by(wechat_id=wechat_id).delete()
        UserInfo.query.filter_by(wechat_id=wechat_id).delete()
        WechatInfo.query.filter_by(openid=wechat_id).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='delete error')

    # print(wechat)
    #
    # return "OK"

    return jsonify(errno=RET.OK, errmsg='OK')
