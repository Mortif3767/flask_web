# -*- coding: utf-8 -*-
from flask import Blueprint

main = Blueprint('main',__name__)

from . import views,errors

@main.app_context_processor              #把Permission类加入模板上下文
def inject_permissions():
    return dict(Permission=Permission)