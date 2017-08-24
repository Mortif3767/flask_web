# -*- coding: utf-8 -*- 
from datetime import datetime
from flask import render_template,session,redirect,url_for

from . import main            #从main／__init__.py中导入蓝本
from .forms import NameForm   #从main／forms导入NameForm类
from .. import db             #从app/__init__.py中导入db=SQLAlchemy（）
from ..models import User     #从app／models导入User数据库表

@main.route('/',methods=['GET','POST'])
def index():
	name=None
	form=NameForm()
	if form.validate_on_submit():
		user=User.query.filter_by(username=form.name.data).first()
		if user is None:
			user=User(username=form.name.data)
			db.session.add(user)
			session['known']=False
			if app.config['FLASKY_ADMIN']:
				send_email(app.config['FLASKY_ADMIN'],'New User',
					       'mail/new_user',user=user)
		else:
			session['known']=True
		session['name']=form.name.data
		form.name.data=''
		return redirect(url_for('main.index'))
	return render_template("index.html",form=form,name=session.get('name'),
		known=session.get('known',False),current_time=datetime.utcnow())