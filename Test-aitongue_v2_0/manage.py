# @Time  :2021/5/2 16:18
# @Author:Sleet
# @File  :manage.py.py

from lg_aitongue import create_app, db, models
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# 调用函数，进行实例化（生产环境）
app = create_app('dev')

# 数据库迁移，将数据库操作对象db和flask实例app进行绑定
manage = Manager(app)
Migrate(app, db)
manage.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manage.run()
