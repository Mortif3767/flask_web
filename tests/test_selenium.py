# -*- coding: utf-8 -*-
import unittest
import re
import threading
import time
from selenium import webdriver
from app import db, create_app
from app.models import Role, User, Post


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        try:
            cls.client = webdriver.Safari()
        except:
            pass
        if cls.client:
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel('ERROR')

            db.drop_all()
            db.create_all()
            Role.insert_roles()
            User.generate_fake(10)
            Post.generate_fake(10)

            admin_role = Role.query.filter_by(permissions=0xff).first()
            admin = User(email='test1@test.com', password='biu',
                         username='biubiu1', confirmed=True, role=admin_role)
            db.session.add(admin)
            db.session.commit()

            threading.Thread(target=cls.app.run).start()

            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            db.drop_all()
            db.session.remove()

            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('web browser not avaliablee')

    def tearDown(self):
        pass

    def test_admin_home_page(self):
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search(u'你好,\s+欢迎登陆', self.client.page_source))

        self.client.find_element_by_link_text('Sign In').click()
        self.assertTrue('<h1>Login</h1>' in self.client.page_source)

        self.client.find_element_by_name('email').send_keys('test1@test.com')
        self.client.find_element_by_name('password').send_keys('biu')
        self.client.find_element_by_name('submit').click()
        self.assertTrue(re.search(u'你好,\s+biubiu', self.client.page_source))

        self.client.find_element_by_link_text('Profile').click()
        self.assertTrue('<h1>biubiu1</h1>' in self.client.page_source)