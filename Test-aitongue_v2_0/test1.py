# @Time  :2021/5/3 22:13
# @Author:Sleet
# @File  :test1.py
# 通用测试文件（测试一些功能的实现）


# import os
#
# # print(os.getcwd())
#
# import time
#
# # print(time.strftime('%Y_%m_%d-%H_%M_%S', time.localtime()))
# # print(time.strftime('%Y-%m-%d', time.localtime()))
#
# # import random
# #
# # # print(random.randint(10, 100))
# #
# # num = random.randint(10, 100)
# # now = time.strftime('%Y_%m_%d-%H_%M_%S', time.localtime())
# # print('picture' + num + '-' + now + '.png')
#
# import hashlib
# # 导入time模块
# import time
# import requests
# import json
# '''
# 调用北京贝叶斯科技AI舌诊接口成功示例。
# 详细使用教程请访问网址：http://www.bayescience.com/bes-project/login.html
# '''
#
#
# def Md5(res):
#     print(res)
#     md = hashlib.md5()  # 构造一个md5
#     md.update(res.encode(encoding='utf-8'))
#     # 加密
#     print(md.hexdigest().upper())
#     return md.hexdigest().upper()
#
#
# def testapi():
#     tures = {}
#     restime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
#     # restime="20190829114035"
#     # 传入参数
#     tures['timestamp'] = restime
#     tures['app_id'] = "a4a5afd0b1994048"
#     tures['version'] = '1.0'
#     tures['method'] = 'jiuti'
#     tures['imgpath'] = 'https://bys-tonguepicture.oss-cn-beijing.aliyuncs.com/1563412989396.jpg'
#     tures['sign'] = Md5(Md5(restime) + "0a2a94839f9c4d48a88cb74c2cdf335e")
#     url = "http://www.bayescience.com/api/analysis"
#     response = requests.post(url, params=tures)
#     print(response.text)
#     print(type(response.text))
#     load = json.loads(response.text)
#     print(load)
# testapi()


# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
# from lg_aitongue import constants
import sys
import logging
#
#
# logging.basicConfig(level=logging.INFO, stream=sys.stdout)
# secret_id = 'AKIDC9QRJxTRH0fSxK82MKK4b5JJ8hpImVFh'      # 替换为用户的 secretId
# secret_key = 'kEQL1RfZwsZw2rwlMfiV6R6IFxPdGdlg'      # 替换为用户的 secretKey
# region = 'ap-shanghai'     # 替换为用户的 Region
# token = None                # 使用临时密钥需要传入 Token，默认为空，可不填
# scheme = 'https'            # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
# config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)
#
# # 2. 获取客户端对象
# client = CosS3Client(config)

# # 根据文件大小自动选择简单上传或分块上传，分块上传具备断点续传功能。
# response = client.upload_file(
#    Bucket='aitongue-1305581802',
#    LocalFilePath='local.txt',
#    Key='picture.jpg',
#    PartSize=1,
#    MAXThread=10,
#    EnableMD5=False
# )
# print(response['ETag'])

# 文件流简单上传（不支持超过5G的文件，推荐使用下方高级上传接口）
# 强烈建议您以二进制模式(binary mode)打开文件,否则可能会导致错误
# file = 'utils/ai_tongue/upload_picture/picture.jpg'
#
# with open(file, 'rb') as fp:
#     response = client.put_object(
#         Bucket='face-img-1305581802',
#         Body=fp,
#         Key='picture.jpg',
#         StorageClass='STANDARD',
#         EnableMD5=False
#     )
# print(response['ETag'])
# true_response = response['ETag']
# if true_response:
#     return constants.TONGUE_IMG_PREFIX + filename
# else:
#     raise Exception
#
# result = []
# if not result:
#     print(1)


# tags = ['sadca', 'sadcasd', 'asdcad']
# symptoms = ', '.join(tags)
# print(symptoms)
