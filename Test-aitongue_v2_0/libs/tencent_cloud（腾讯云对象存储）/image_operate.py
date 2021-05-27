# @Time  :2021/5/3 20:34
# @Author:Sleet
# @File  :image_operate.py


# 1. 设置用户配置, 包括 secretId，secretKey 以及 Region
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
# from lg_aitongue import constants
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
secret_id = 'AKIDC9QRJxTRH0fSxK82MKK4b5JJ8hpImVFh'  # 替换为用户的 secretId
secret_key = 'kEQL1RfZwsZw2rwlMfiV6R6IFxPdGdlg'  # 替换为用户的 secretKey
region = 'ap-shanghai'  # 替换为用户的 Region
token = None  # 使用临时密钥需要传入 Token，默认为空，可不填
scheme = 'https'  # 指定使用 http/https 协议来访问 COS，默认为 https，可不填
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token, Scheme=scheme)

# 2. 获取客户端对象
client = CosS3Client(config)


def storage(filedata, filename):

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
    # file = '../../upload_picture/picture.jpg'

    # with open(file, 'rb') as fp:
    response = client.put_object(
        Bucket='face-img-1305581802',
        Body=filedata,
        Key=filename,
        StorageClass='STANDARD',
        EnableMD5=False
    )
    # print(response['ETag'])
    true_response = response['ETag']
    if true_response:
        return filename
    else:
        raise Exception


def delete(filename):
    # 删除object
    # deleteObject
    response = client.delete_object(
        Bucket='face-img-1305581802',
        Key=filename
    )
    if not response:
        raise Exception
