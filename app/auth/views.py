# -*- coding: utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm,\
    PasswordResetForm
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

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
	form = ChangePasswordForm()
	if form.validate_on_submit():
		if current_user.verify_password(form.old_password.data):
			current_user.password = form.password.data
			db.session.add(current_user)
			flash(u'密码已更改')
			return redirect(url_for('main.index'))
		else:
			flash(u'密码错误')
	return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
	if not current_user.is_anonymous:            #研究下这个anonymous
		redirect(url_for('main.index'))
	form = PasswordResetRequestForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user:
			token = user.generate_reset_token()
			flash(u'成功受理')
			return render_template('auth/save.html', token=token, user=user)
			# redirect reset page
	return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
	if not current_user.is_anonymous:
		redirect(url_for('main.index'))
	form = PasswordResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			flash(u'无效邮箱')
		elif user.reset_password(token, form.password.data):
			flash(u'密码修改成功')
			return redirect(url_for('auth.login'))
		else:
			flash(u'修改链接错误')
			return redirect(url_for('main.index'))
	return render_template('auth/reset_password.html', form=form)





