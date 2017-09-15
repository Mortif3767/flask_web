# -*- coding: utf-8 -*-
from flask import g
from ..models import AnonymousUser, User
from flask_httpauth import HTTPBasicAuth
from . import api
from .errors import unauthorized, forbidden

auth = HTTPBasicAuth()           #注意扩展的初始化方式


@auth.verify_password            #httpbasicauth包装（其中不含验证密令方法）
def verify_password(email_or_token, password):    #回调函数定义密码验证方法
    if email_or_token == '':
        g.current_user = AnonymousUser()
        return True
    if password == '':
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    user = User.query.filter_by(email=email).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)
    #程序返回布尔值，另外把已认证用户保存在全局变量g中，可供视图函数使用


@auth.error_handler
def auth_error():
    return unauthorized(u'无效证书')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.is_anonymous and \
            not g.current_user.confirmed:
        return forbidden(u'未认证用户')
