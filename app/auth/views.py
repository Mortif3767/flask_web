# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm
from .. import db
from ..email import send_email

@auth.before_app_request
def before_request():
	if current_user.is_authenticated \
	        and not current_user.confirmed \
	        and request.endpoint[:5] != 'auth.' \
	        and request.endpoint != 'static':
		return redirect(url_for('auth.unconfirmed'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('main.index'))  #第一项是登陆前页面
		flash(u'错误用户名或密码!')
	return render_template('auth/login.html',form=form)


@auth.route('/logout')
@login_required   #only authenticated user are allowed
def logout():
	logout_user()
	flash(u"你已经退出。")
	return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	token = None
	if form.validate_on_submit():
		user = User(email=form.email.data,
			        username=form.username.data,
			        password=form.password.data)
		db.session.add(user)
		db.session.commit()
		token = user.generate_confirmation_token()
		flash(u'注意点击确认链接')
		return render_template('auth/unconfirmed.html', token = token)
	return render_template('auth/register.html', form=form, token = token)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
	if current_user.confirmed:
		return redirect(url_for('main.index'))
	if current_user.confirm(token):
		flash(u'你已经成功激活你的账户')
	else:
		flash(u'链接已经失效，请重试')
	return redirect(url_for('main.index'))

@auth.route('/unconfirmed')
def unconfirmed():
	if current_user.is_anonymous or current_user.confirmed:
		return redirect(url_for('main.index'))
	token = current_user.generate_confirmation_token()
	return render_template('auth/unconfirmed.html', token=token)
