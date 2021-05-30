# @Time  :2021/5/8 10:37
# @Author:Sleet
# @File  :face.py

from . import api
from flask import request, jsonify
from lg_aitongue.response_code import RET
from lg_aitongue.models import WechatInfo, Face
from lg_aitongue import db
# from libs.tencent_cloud（腾讯云对象存储）.image_operate import storage, delete
from utils.commons import create_file_name
from config import Config
import logging
import os


@api.route('/face', methods=['POST'])
def save_face():
    """
    保存用户的面部图片
    :param wechat_id: 用户微信id， face_img: 用户面部图片
    :return: 保存成功或错误信息
    """
    # 获取参数
    try:
        face_img = request.files['face_img']
        wechat_id = request.form.get('wechat_id')
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.PAPAMERR, errmsg='参数错误')

    if not all([face_img, wechat_id]):
        return jsonify(errno=RET.PAPAMERR, errmsg='参数错误')

    # 判断用户是否存在
    try:
        wechat = WechatInfo.query.filter_by(openid=wechat_id).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='search wechat error')

    if not wechat:
        return jsonify(errno=RET.NOUSER, errmsg='wechat id not exist')

    # 上传图片到腾讯云
    # filename = face_img.filename
    # suffix = filename[filename.rfind("."):]
    # upload_time = time.strftime('%Y_%m_%d-%H_%M_%S', time.localtime())
    # rnum = str(random.randint(10, 99))
    # face_img_name = wechat_id + '-' + rnum + '@' + upload_time + suffix
    # face_img_data = face_img.read()
    # try:
    #     face_img_url = storage(face_img_data, face_img_name)
    # except Exception as e:
    #     logging.error(e)
    #     return jsonify(errno=RET.THIRDERR, errmsg='第三方系统异常')

    # 生成文件名
    face_img_name = create_file_name(face_img, wechat_id)
    # 保存图片到本地文件夹
    face_img.save(os.path.join(Config.SAVE_FACE_IMG_FOLDER, face_img_name))

    # 保存图片
    # if not all([user.gender, user.age, user.height, user.weight, user.area, user.medical_history]):
    #     return jsonify(errno=RET.NOUSER, errmsg='个人信息不完整')

    # 超过五个后覆盖最旧的那个
    try:
        # 获取数据记录量
        faces_num = Face.query.filter_by(wechat_id=wechat_id).count()
        # 获取最新记录
        longest_time_face = Face.query.filter_by(wechat_id=wechat_id).order_by(Face.update_time).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='search face info error')

    # 删除腾讯云被覆盖了的图片
    # try:
    #     delete(longest_time_img_name)
    # except Exception as e:
    #     logging.error(e)
    #     return jsonify(errno=RET.THIRDERR, errmsg='第三方系统出错')

    if faces_num == 5:
        # 删除文件夹被覆盖了的图片
        longest_time_img_name = longest_time_face.face_img_url
        longest_time_img_path = os.path.join(Config.SAVE_FACE_IMG_FOLDER, longest_time_img_name)
        if os.path.exists(longest_time_img_path):
            os.remove(longest_time_img_path)
        try:
            longest_time_face.face_img_url = face_img_name
            db.session.commit()
        except Exception as e:
            # 这里是数据库操作异常后，能够进行回滚，防止错误写入
            db.session.rollback()
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='update face info error')
    else:
        # 要写入的数据
        face = Face(
            wechat_id=wechat_id,
            face_img_url=face_img_name
        )
        # 写入数据
        try:
            db.session.add(face)
            db.session.commit()
        except Exception as e:
            # 这里是数据库操作异常后，能够进行回滚，防止错误写入
            db.session.rollback()
            # 记录错误信息
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='保存异常')

    return jsonify(errno=RET.OK, errmsg='save face info success')
