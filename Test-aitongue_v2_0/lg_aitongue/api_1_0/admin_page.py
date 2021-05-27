# @Time  :2021/5/21 15:22
# @Author:Sleet
# @File  :admin_page.py
# 该文件用于测试

# from . import admin_bp
# from flask import session, redirect, url_for, render_template, request, jsonify
# from lg_aitongue.response_code import RET
# from lg_aitongue.models import Admin
# import logging
#
#
# @admin_bp.route('/admin')
# def admin_login():
#     # 判断管理员是否登录
#     administrator = session.get('account_name')
#     if administrator is None:
#         return redirect(url_for('login'))
#
#
# @admin_bp.route('/login')
# def login():
#     return render_template('html/login.html')
#
#
# @admin_bp.route('/session', methods=['POST'])
# def session():
#     """
#     管理员登录
#     :return: json
#     """
#     # 获取参数
#     request_dict = request.get_json()
#     account_name = request_dict.get('account_name')
#     password = request_dict.get('password')
#
#     if not all([account_name, password]):
#         return jsonify(errno=RET.PAPAMERR, errmsg='参数不完整')
#
#     try:
#         administrator = Admin.query.filter_by(account=account_name).first()
#     except Exception as e:
#         logging.error(e)
#         return jsonify(errno=RET.DBERR, errmsg='search admin info error')
#
#     if administrator is None:
#         return jsonify(errno=RET.NOUSER, errmsg='login error')
#
#     real_password = administrator.password
#     if password != real_password:
#         return jsonify(errno=RET.LOGINERR, errmsg='login error')
#
#     session['account_name'] = account_name
#     session['password'] = password
#
#     return jsonify(errno=RET.OK, errmsg='login success')
