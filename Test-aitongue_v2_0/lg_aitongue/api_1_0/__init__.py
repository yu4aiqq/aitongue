# @Time  :2021/5/2 16:55
# @Author:Sleet
# @File  :__init__.py.py

from flask import Blueprint

# 创建蓝图，集中保存视图，url_prefix设置前缀
api = Blueprint('api_1_0', __name__, url_prefix='/api/v1.0')
# 导入写好的视图文件，为避免循环导入因此放在文档底部
from . import body_record, result, profile, face, scale, login
from utils.ai_tongue import tongue_diagnosis


# admin_bp = Blueprint('admin_1_0', __name__)
# from . import admin_page
