# -*- coding: utf-8 -*- 

from flask import Flask
from flask_script import Manager

app=Flask(__name__)      #创建程序实例

manager=Manager(app)

@app.route('/')          #路由：处理URL和函数之间的关系
def index():             #视图函数
    return '<h1>NIHAO!</h1>'

@app.route('/user/<name>')
def user(name):
	return "<h1>NiHao,%s</h1>" % name

if __name__=='__main__': #启动服务器
    manager.run()