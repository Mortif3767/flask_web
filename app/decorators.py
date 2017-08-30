# -*- coding: utf-8 -*-
from functools import wraps
from flask import abort
from flask_login import current_user
from .models import Permission

def permission_required(permission):            #permission为装饰函数功能的参数，所以要多套用一层。
    def decorator(f):                           #f为被装饰函数wrapped
        @wraps(f)                               #用于使用装饰器函数，可以正确显示__name__,__doc__
        def decorator_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)                      #为运行f这个函数添加条件，不满足条件即abort跳出错误
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER).(f)