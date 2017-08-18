from flask import Flask
app=Flask(__name__)      #创建程序实例

@app.route('/')          #路由：处理URL和函数之间的关系
def index():             #视图函数
    return '<h1>NIHAO!</h1>'

if __name__=='__main__': #启动服务器
    app.run(debug=True)