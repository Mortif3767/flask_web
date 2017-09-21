基于Flask的小型微博网站

按照《Flask Web开发》（狗书）自学实践，目前挂载在阿里云http://120.78.85.245 。

微博的主要功能：
<br>
1.用户认证<br>
  包括注册账户token信息认证、账户维护等。<br>
<br> 
2.用户权限<br>
  三个权限：管理员、评论维护员、用户。<br>
<br> 
3.用户资料<br>
  账号拥有个人资料页面，包括gravatar头像、资料编辑器等。<br>
<br> 
4.博客文章<br>
  首页显示即博客文章，支持markdown富文本，可生成博客固定链接，博客修改等功能。<br>
<br> 
5.关注者功能<br>
  支持用户之间关注，首页可选被关注者的微博。<br>
<br> 
6.API服务<br>
  支持客户端获取博客、生成博客、编辑博客功能，并提供账户认证功能，同时可发送json错误信息。<br>
<br> 
PS：注册流程中应有邮箱验证环节，编程中为了测试方便，涉及邮箱验证token信息的流程，被修改为直接跳转到验证页面，不经过email模块发送：）<br>
<br> 

程序结构：<br>
|-flask_web<br>
&emsp;|-app/<br>
&emsp;&emsp;|-main/&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;#主页面蓝本<br>
&emsp;&emsp;&emsp;|-__init__.py<br>
&emsp;&emsp;&emsp;|-views.py<br>
&emsp;&emsp;&emsp;|-forms.py<br>
&emsp;&emsp;&emsp;|-errors.py<br>
&emsp;&emsp;|-auth/&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&ensp;#账户管理页面蓝本<br>
&emsp;&emsp;&emsp;|-__init__.py<br>
&emsp;&emsp;&emsp;|-views.py<br>
&emsp;&emsp;&emsp;|-forms.py<br>
&emsp;&emsp;|-api_1_0/&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;#api服务蓝本<br>
&emsp;&emsp;&emsp;|-__init__.py<br>
&emsp;&emsp;&emsp;|-authentication.py<br>
&emsp;&emsp;&emsp;|-decorators.py<br>
&emsp;&emsp;&emsp;|-errors.py<br>
&emsp;&emsp;&emsp;|-posts.py<br>
&emsp;&emsp;|-templates/&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;#jinja2模版目录 内容略<br>
&emsp;&emsp;|-static/                    &ensp;&ensp; #静态文件<br>
&emsp;&emsp;|-__init__.py&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp;&ensp; #主程序初始化<br>
&emsp;&emsp;|-decorators.py           #装饰器程序<br>
&emsp;&emsp;|-email.py                    #邮件模块<br>
&emsp;&emsp;|-exceptions.py           #自定义错误<br>
&emsp;&emsp;|-models.py                 #数据类型<br>
&emsp;|-manage.py                   #启动脚本<br>
&emsp;|-config.py                        #配置信息<br>
&emsp;|-data-dev.sqlite             #程序建设用数据库<br>
&emsp;|-data-test.sqlite             #程序测试缓冲数据库<br>
&emsp;|-requirements/                #程序运行扩展需求表<br>
&emsp;|-tests/                            #测试程序文件夹<br>
&emsp;|-venv/                            #使用虚拟环境<br>
