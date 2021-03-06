# -*- coding: utf-8 -*-
import unittest
import json
from base64 import b64encode
from app import create_app, db
from app.models import Role, User, Post
from flask import url_for


class APITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, username, password):
        return {
            'Authorization':
                'Basic '+b64encode(
                    (username + ':' + password).encode('utf-8')).decode('utf-8'),
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def test_no_auth(self):
        response = self.client.get(url_for('api.get_posts'),
                                           content_type='application/json')
        self.assertTrue(response.status_code == 200)

    def test_posts(self):    #创建用户
        r = Role.query.filter_by(name='User').first()
        self.assertIsNotNone(r)
        u = User(email='test@test.com', password='biu', confirmed=True, role=r)
        db.session.add(u)
        db.session.commit()

        #发布一篇日志
        response = self.client.post(
            url_for('api.new_post'),
            headers=self.get_api_headers('test@test.com', 'biu'),
            data=json.dumps({'body': 'blablabla'}))
        self.assertTrue(response.status_code == 201)
        url = response.headers.get('Location')
        self.assertIsNotNone(url)

        #获取刚刚发布的文章
        response = self.client.get(
            url,
            headers=self.get_api_headers('test@test.com', 'biu'))
        self.assertTrue(response.status_code == 200)
        json_response = json.loads(response.data.decode('utf-8'))
        self.assertTrue(json_response['url'] == url)
        self.assertTrue(json_response['body'] == 'blablabla')
