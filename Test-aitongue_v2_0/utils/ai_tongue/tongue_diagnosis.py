# coding=utf-8
# author:Tang Gaozhi, Sleet
# time: 2021-5-15 11:09

import os
from flask import request, jsonify
from . import runModel3
from . import picSegment
from .constant import value2Dict, type2Dict, weights2Dict
from .constant import imgUrl
import time
from lg_aitongue.api_1_0 import api
from lg_aitongue import db
from config import Config
from lg_aitongue.models import WechatInfo, Mouth
from lg_aitongue.response_code import RET
from utils.commons import create_file_name
import logging


ALLOWED_EXTENSIONS = {'bmp', 'png', 'jpg', 'jpeg', 'gif'}

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = os.getcwd()+'/upload_picture'
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# html = '''
#     <!DOCTYPE html>
#     <title>Upload File</title>
#     <h1>Photo Upload</h1>
#     <form method=post enctype=multipart/form-data>
#          <input type=file name=file>
#          <input type=submit value=upload>
#     </form>
#     '''


# 判断file的格式(是否有‘.’ , 以及是否符合ALLOWED_EXTENSIONS里的格式)
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
# 下载文件路由    
# @api.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'],
#                                filename)


# 上传文件路由
@api.route('/tongue/<wechat_id>', methods=['POST'])
def upload_file(wechat_id):
    """
    获取用户的舌头图片
    :param wechat_id: 用户微信id
    :return: 返回舌诊结果
    """
    # 判断用户是否存在
    try:
        wechat = WechatInfo.query.filter_by(openid=wechat_id).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='search wechat info error')

    if not wechat:
        return jsonify(errno=RET.NOUSER, errmsg='wechat id not exist')

    # 参数获取
    try:
        file = request.files['file']
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.PAPAMERR, errmsg='参数错误')

    # 舌诊逻辑变量
    message = "null"
    predictedTypeRate = 0.0
    tags = []
    result = -1
    maxConfidence = 0.0

    # 下面那几个变量只是为了写入信息，不需要时应该删掉
    typeList = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    weight2Dict = {}

    # 校验文件
    if not file and allowed_file(file.filename):
        return jsonify(errno=RET.PAPAMERR, errmsg='参数错误')

    # 生成文件名
    mouth_img_name = create_file_name(file, wechat_id)
    mouth_img_path = os.path.join(Config.UPLOAD_FOLDER, mouth_img_name)
    mask_mouth_img_path = mouth_img_path.replace(".", "_mask.")
    file.save(mouth_img_path)  # 保存文件

    isTongue = picSegment.pictureProcess(mouth_img_path)

    try:
        tagsString = request.values.get("tags")  # 获取前端的tags的信息
        if tagsString != "":
            tags = tagsString.split(",")  # 分割字符串
    except Exception as e:
        logging.error(e)
        pass

    try:

        if isTongue is True:
            # 这里需要注意，模型2是rec，模型3是mask
            rate = runModel3.getResult(mask_mouth_img_path)
            predictedTypeRate = max(rate)  # 留一手，若无tags传过来，这两个就用上了
            maxConfidence = predictedTypeRate  # 看看纯预测的置信度最高的是多少
            result = rate.index(predictedTypeRate)

            if len(tags) != 0:  # tags有值时执行
                for i in range(0, len(rate)):
                    weight2Dict[i] = 0.4 * rate[i]
                for tag in tags:
                    weight2Dict[int(type2Dict[tag]) - 1] += weights2Dict[tag] * 0.6
                    typeList[int(type2Dict[tag]) - 1] += weights2Dict[tag]
                    if tag == "身体水肿":  # 因为有重叠的，还要算上另一个
                        weight2Dict[6] += weights2Dict["水肿"] * 0.6
                    if tag == "大便稀溏":
                        weight2Dict[3] += weights2Dict["大便稀"] * 0.6
                    if tag == "胸胁疼痛":
                        weight2Dict[2] += 0.3 * 0.6
                    if tag == "乏力":
                        weight2Dict[1] += 0.5 * 0.6

                typeWeight = sorted(weight2Dict.items(), key=lambda item: item[1])

                result = typeWeight[-1][0]  # 预测体质名称下标
                predictedTypeRate = typeWeight[-1][1]  # 置信度
            else:
                for i in range(0, len(rate)):
                    weight2Dict[i] = rate[i]
        else:
            message = "上传照片未检测到舌头，请重新上传!"
            return jsonify(errno=RET.PAPAMERR, errmsg=message)

    except Exception as e:
        message = "服务器异常1,请过几分钟再试!若仍不行,请联系1348040397@qq.com"
        logging.error(e)
        return jsonify(errno=RET.SERVERERR, errmsg=message)

    num = str(0)

    if weight2Dict == {} and isTongue is True:
        message = "服务器已宕机，请联系我们重启程序!"

    if isTongue is True and weight2Dict != {}:

        if weight2Dict[1] > 0.5:
            num = str(1)
        elif maxConfidence < 0.5:
            message = "未知体质，请检查上传图片是否正确!!"
        else:
            num = str(result+1)

    # 删除图片（如果需要查看图片，可注释掉）
    if os.path.exists(mouth_img_path) and os.path.exists(mask_mouth_img_path):
        os.remove(mouth_img_path)
        os.remove(mask_mouth_img_path)

    # 保存变量
    symptoms = ', '.join(tags)
    body_type = value2Dict[num]
    img_url = imgUrl[value2Dict[num]]
    confidence = str(round(predictedTypeRate, 3))
    date = time.strftime("%Y-%m-%d", time.localtime())
    ctime = time.strftime("%H:%M", time.localtime())

    # 要更新的数据和要返回的数据
    diagnosis = {
        'symptoms': symptoms,
        'body_type': body_type,
        'result_img_url': img_url,
        'confidence': confidence,
        'date': date,
        'time': ctime
    }
    # 超过五条记录覆盖最旧的那条
    try:
        mouths_num = Mouth.query.filter_by(wechat_id=wechat_id).count()
        longest_time_reord = Mouth.query.filter_by(wechat_id=wechat_id).order_by(Mouth.update_time).first()
    except Exception as e:
        logging.error(e)
        return jsonify(errno=RET.DBERR, errmsg='search mouth info error')

    if mouths_num == 5:
        longest_time = longest_time_reord.update_time
        # 更新数据
        try:
            Mouth.query.filter(Mouth.wechat_id == wechat_id, Mouth.update_time == longest_time).update(diagnosis)
            db.session.commit()
        except Exception as e:
            # 这里是数据库操作异常后，能够进行回滚，防止错误写入
            db.session.rollback()
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='update mouth info error')
    else:
        # 要写入的数据
        mouth = Mouth(
            wechat_id=wechat_id,
            symptoms=symptoms,
            body_type=body_type,
            result_img_url=img_url,
            confidence=confidence,
            date=date,
            time=ctime
        )
        # 写入数据
        try:
            db.session.add(mouth)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(e)
            return jsonify(errno=RET.DBERR, errmsg='save mouth info error')

    return jsonify(errno=RET.OK, errmsg='OK', data=diagnosis)
