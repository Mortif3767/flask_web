
# -*- coding: utf-8 -*-
import unittest
from app import create_app, db
from app.models import User, Role

class FlaskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True) #flask测试客户端对象

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue(u'欢迎登陆' in response.get_data(as_text=True))

    def test_register_and_login(self):    #注册新用户
        response = self.client.post(url_for('auth.register'), data={
            'email': 'test@test.com'
            'username': 'biubiu'
            'password': 'biu'
            'password2': 'biu'
            })
        self.assertTrue(response.status_code == 302)

        #测试登陆
        response = self.client.post(url_for('auth.login'),data={
            'email': 'test@test.com'
            'password': 'biu'
            }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(re.search(u'你好,\s+biubiu', data))

        #发送确认令牌
        user = User.query.filter_by(email='test@test.com').first()
        token = user.generate_confirmation_token()
        response = self.client.get(url_for('auth.confirm', token=token), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(u'你已经成功激活你的账户' in data)

        #退出
        response = self.client.get(url_for('auth.logout'),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue(u'你已经退出' in data)