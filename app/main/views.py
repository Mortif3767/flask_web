# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, url_for, abort, request,\
    current_app
from . import main
from ..models import User, Role, Permission, Post
from flask_login import login_required, current_user
from .forms import EditProfileForm, EditProfileAdminForm, PostForm
from .. import db
from ..decorators import admin_required, permission_required


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data, author=current_user._get_current_object())
        #current_user是Flask-login提供的轻度包装User对象，真正的对象需要调用_get_current_object()
        db.session.add(post)
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)     #dict.get(key, default=None, type=None)
    #默认页面是第一页
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)                             #返回第page页，每页*个记录
    posts = pagination.items                         #留意pagination对象是什么？items是该对象的属性
    return render_template('index.html', form=form, posts=posts, pagination=pagination)


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    posts = user.posts.order_by(Post.timestamp.desc()).all()
    return render_template('user.html', user=user, posts=posts)


@main.route('/post/<int:id>')
def post(id):
    post = Post.query.get_or_404(id)
    return render_template('post.html',posts=[post])


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash(u'个人信息更新成功')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit-profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash(u'信息更新成功')
        return redirect(url_for('main.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit-profile.html', form=form, user=user)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    post = Post.query.get_or_404(id)
    if current_user != post.author and \
        not current_user.is_administrator():
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.body = form.body.data
        db.session.add(post)
        flash(u'日志修改成功')
        return redirect(url_for("main.post", id=id))
    form.body.data = post.body
    return render_template('edit_post.html', form=form)


@main.route('/follow/<username>')
@login_required
@permission_required(Permission.FOLLOW)
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'无效用户')
        return redirect(url_for('main.index'))
    if current_user.is_following(user):
        flash(u'已经关注此用户')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    flash(u'你现在正在关注：%s' % username)
    return redirect(url_for('main.user', username=username))


@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'无效用户')
        return redirect(url_for('main.index'))
    if not current_user.is_following(user):
        flash(u'没有关注此用户')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    flash(u'你不再关注 %s' % username)
    return redirect(url_for('main.user', username=username))


@main.route('/followers/<username>')
def followers(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'无效用户')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followers.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user':item.follower, 'timestamp':item.timestamp} 
        for item in pagination.items]
    return render_template('followers.html', user=user, title=u"的粉丝",
                           endpoint='main.followers', pagination=pagination, follows=follows)


@main.route('/followed/<username>')
def followed(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(u'无效用户')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    pagination = user.followed.paginate(
        page, per_page=current_app.config['FLASKY_FOLLOWERS_PER_PAGE'],
        error_out=False)
    follows = [{'user':item.followed, 'timestamp':item.timestamp}
        for item in pagination.items]
    return render_template('followed.html', user=user, title=u'的关注者',
                            endpoint='main.followed', pagination=pagination, follows=follows)
