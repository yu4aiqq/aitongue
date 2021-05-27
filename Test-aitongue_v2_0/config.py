# @Time  :2021/5/2 16:22
# @Author:Sleet
# @File  :config.py

import os
import redis


class Config(object):
    """配置信息"""
    # 数据库配置
    HOSTNAME = '127.0.0.1'
    DATABASE = 'aitongue'
    PORT = 3306
    USERNAME = 'root'
    PASSWORD = 'root'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 启用flask后台需要
    SECRET_KEY = os.urandom(12)

    # 舌头图片文件夹的路径
    UPLOAD_FOLDER = os.getcwd() + '/utils/ai_tongue/upload_picture'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # 面部图片文件夹的路径
    SAVE_FACE_IMG_FOLDER = os.getcwd() + '/face_img'


class DevConfig(Config):
    """开发环境"""
    DEBUG = True


class ProConfig(Config):
    """生产环境"""


# 配置选择面板
config_map = {
    'dev': DevConfig,
    'pro': ProConfig
}
