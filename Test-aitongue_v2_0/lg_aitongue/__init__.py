# @Time  :2021/5/2 16:21
# @Author:Sleet
# @File  :__init__.py.py


from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_map
from logging.handlers import RotatingFileHandler
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import logging
# import redis


# 将db设为数据库操作对象
db = SQLAlchemy()
# flask后台
admin = Admin(name=u'后台管理系统', url='/sqlalchemy')
# redis_store = None


# 自定义类，重写ModelView中的属性，禁止创建，编辑和删除操作，将可视页面定为50页
class MicroModelView(ModelView):
    can_create = False    # disable model creation
    can_edit = False    # disable model edition
    can_delete = False    # disable model deletion
    page_size = 50    # the number of entries to display on the list view


# 配置日志文件
def setup_log():
    # 设置日志的的登记  DEBUG调试级别
    logging.basicConfig(level=logging.DEBUG)
    # 创建日志记录器，设置日志的保存路径和每个日志的大小和日志的总大小
    file_log_handler = RotatingFileHandler("log/log", maxBytes=1024*1024*100, backupCount=100)
    # 创建日志记录格式，日志等级，输出日志的文件名 行数 日志信息
    formatter = logging.Formatter("%(levelname)s %(filename)s: %(lineno)d %(message)s")
    # 为日志记录器设置记录格式
    file_log_handler.setFormatter(formatter)
    # 为全局的日志工具对象（flaks app使用的）加载日志记录器
    logging.getLogger().addHandler(file_log_handler)


def create_app(config_name):
    # 创建日志
    setup_log()
    # Flask实例化
    app = Flask(__name__)
    # 选择配置对象（生产环境配置或者开发环境配置）
    config_class = config_map.get(config_name)
    # 配置上面所选的配置信息
    app.config.from_object(config_class)

    # 数据操作对象绑定app
    db.init_app(app)
    # 后台绑定app
    admin.init_app(app)

    # 创建后台视图，展示数据库
    # 这里进行导入是为避免循环导入
    from lg_aitongue.models import WechatInfo, UserInfo, Mouth, Face, Scale
    admin.add_view(MicroModelView(WechatInfo, db.session))
    admin.add_view(MicroModelView(UserInfo, db.session))
    admin.add_view(MicroModelView(Mouth, db.session))
    admin.add_view(MicroModelView(Face, db.session))
    admin.add_view(MicroModelView(Scale, db.session))

    # 注册蓝图
    # 这里进行导入是为避免循环导入
    from lg_aitongue.api_1_0 import api
    app.register_blueprint(api)
    # app.register_blueprint(admin_bp)

    return app
