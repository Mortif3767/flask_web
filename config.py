# -*- coding: utf-8 -*- 
import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:                     #基类用于定义通用配置
	SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard to guess string'
	SQLALCHEMY_COMMIT_ON_TEARDOWN = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	FLASKY_MAIL_SUBJECT_PREFIX = '[Flasky]'
	FLASKY_MAIL_SENDER = 'Guo Zhen <garryrich@gmail.com>'
	FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')
	FLASKY_POSTS_PER_PAGE = 20
	FLASKY_FOLLOWERS_PER_PAGE = 50

	@staticmethod                 #不需要self参数，不用实例化，直接类名.程序名引用
	def init_app(app):            #可以执行对当前环境的配置初始化
		pass

class DevelopmentConfig(Config):  #用于专用配置
	DEBUG=True
	MAIL_SERVER = 'smtp.gmail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
	    'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')

class TestingConfig(Config):
	TESTING=True
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
	    'sqlite:///'+os.path.join(basedir,'data-test.sqlite')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	    'sqlite:///'+os.path.join(basedir,'data.sqlite')

config = {
	'development':DevelopmentConfig,
	'testing':TestingConfig,
	'production':ProductionConfig,
	'default':DevelopmentConfig
}