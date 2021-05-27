# @Time  :2021/5/14 19:46
# @Author:Sleet
# @File  :commons.py


import random
import time


# 生成舌诊和面诊图片的文件名
def create_file_name(file, wechat_id):
    old_name = file.filename
    suffix = old_name[old_name.rfind("."):]
    upload_time = time.strftime('%Y_%m_%d-%H_%M_%S', time.localtime())
    rnum = random.randint(10, 99)
    file_name = f'{wechat_id}-{rnum}@{upload_time}{suffix}'
    return file_name
