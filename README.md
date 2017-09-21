基于Flask的小型微博网站

按照《Flask Web开发》（狗书）自学实践，目前挂载在阿里云http://120.78.85.245 。

微博的主要功能：

1、用户认证
  包括注册账户token信息认证、账户维护等。
  
2、用户权限
  三个权限：管理员、评论维护员、用户。
  
3、用户资料
  账号拥有个人资料页面，包括gravatar头像、资料编辑器等。
  
4、博客文章
  首页显示即博客文章，支持markdown富文本，可生成博客固定链接，博客修改等功能。
  
5、关注者功能
  支持用户之间关注，首页可选被关注者的微博。
  
6、API服务
  支持客户端获取博客、生成博客、编辑博客功能，并提供账户认证功能，同时可发送json错误信息。
  
PS：注册流程中应有邮箱验证环节，编程中为了测试方便，涉及邮箱验证token信息的流程，被修改为直接跳转到验证页面，不经过email模块发送：）
  

程序结构：
|-flask_web
  |-app/
    |-main/                       #主页面蓝本
      |-__init__.py
      |-views.py
      |-forms.py
      |-errors.py
    |-auth/                       #账户管理页面蓝本
      |-__init__.py
      |-views.py
      |-forms.py
    |-api_1_0/                    #api服务蓝本
      |-__init__.py
      |-authentication.py
      |-decorators.py
      |-errors.py
      |-posts.py
    |-templates/                  #jinja2模版目录 内容略
    |-static/                     #静态文件
    |-__init__.py                 #主程序初始化
    |-decorators.py               #装饰器程序
    |-email.py                    #邮件模块
    |-exceptions.py               #自定义错误
    |-models.py                   #数据类型
  |-manage.py                     #启动脚本
  |-config.py                     #配置信息
  |-data-dev.sqlite               #程序建设用数据库
  |-data-test.sqlite              #程序测试缓冲数据库
  |-requirements/                 #程序运行扩展需求表
  |-tests/                        #测试程序文件夹
  |-venv/                         #使用虚拟环境
