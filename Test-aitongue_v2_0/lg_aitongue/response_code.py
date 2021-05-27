# @Time  :2021/5/2 17:05
# @Author:Sleet
# @File  :response_code.py


class RET:
    OK = '0'
    DBERR = '4001'
    NODATA = '4002'
    DATAEXIST = '4003'
    NOUSER = '4101'
    LOGINERR = '4102'
    PAPAMERR = '4103'
    REQERR = '4201'
    THIRDERR = '4301'
    SERVERERR = '4500'
    OTHERERR = '4501'
    UNKNOWNERR = '4502'


error_map = {
    RET.OK: '成功',
    RET.DBERR: '数据库异常',
    RET.NODATA: '无数据',
    RET.DATAEXIST: '数据已存在',
    RET.NOUSER: '用户未登录',
    RET.LOGINERR: '用户登录失败',
    RET.PAPAMERR: '参数错误',
    RET.REQERR: '非法请求',
    RET.THIRDERR: '第三方系统错误',
    RET.SERVERERR: '内部错误',
    RET.OTHERERR: '其它错误',
    RET.UNKNOWNERR: '未知错误'
}
