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
	FLASKY_COMMENTS_PER_PAGE = 5

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
	WTF_CSRF_ENABLED = False
	SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
	    'sqlite:///'+os.path.join(basedir,'data-test.sqlite')

class ProductionConfig(Config):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	    'sqlite:///'+os.path.join(basedir,'data.sqlite')

	@classmethod
	def init_app(cls, app):
		Config.init_app(app)    #继承Config方法的内容

		import logging
		from logging.handlers import SMTPHandler
		credentials = None
		secure = None
		if getattr(cls, 'MAIL_USERNAME', None) is not None:  #getattr(x,'y') is equal to x.y
			credentials = (cls.MAIL_USERNAME, cls.MAIL_PASSWORD)
			if getattr(cls, 'MAIL_USE_TLS', None):
				secure = ()
		mail_handler = SMTPHandler(
			mailhost=(cls.MAIL_SERVER, cls.MAIL_PORT),
			fromaddr=cls.FLASKY_MAIL_SENDER,
			toaddrs=[cls.FLASKY_ADMIN],
			subject=cls.FLASKY_MAIL_SUBJECT_PREFIX + 'Application Error',
			credentials=credentials,
			secure=secure)
		mail_handler.setLevel(logging.ERROR)
		app.logger.addHandler(mail_handler)



config = {
	'development':DevelopmentConfig,
	'testing':TestingConfig,
	'production':ProductionConfig,
	'default':DevelopmentConfig
}