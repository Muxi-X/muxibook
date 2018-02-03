import unittest
import os
from muxibook_app import create_app ,db
from flask import current_app, url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
import random
import json

db=SQLAlchemy()

class BasicTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(os.getenv('FLASK_CONFIG') or 'default')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exist(self):
        self.assertFalse(current_app is None)


    #----------API FILE NAME:/home/shiina/MUXI/muxibook/muxibook_app/api//errors.py-------------------


    #----------API FILE NAME:/home/shiina/MUXI/muxibook/muxibook_app/api//users.py-------------------

    #Test login
    def test_b_login(self):
        response = self.client.post(
            url_for('api.login',_external=True),
            data = json.dumps({
                "username":'shiina',
                "password":'mashiro',
            }),
            content_type = 'application/json')
        s=json.loads(response.data.decode('utf-8'))['token']
        global TOKEN
        TOKEN=s
        self.assertTrue(response.status_code == 200)

    #Test signup
    def test_a_signup(self):
        response = self.client.post(
            url_for('api.signup',_external=True),
            data = json.dumps({
                "realname":'shiina',
                "username":'shiina',
                "password":'mashiro',
            }),
            content_type = 'application/json')
        self.assertTrue(response.status_code == 200)


    #----------API FILE NAME:/home/shiina/MUXI/muxibook/muxibook_app/api//books.py-------------------

    #Test add_book
    def test_c_add_book(self):
        response = self.client.post(
            url_for('api.add_book',_external=True),
            data = json.dumps({
                "kind": 4,
                "book":'algorithm',
                "no":'T0001',
            }),
            content_type = 'application/json')
        self.assertTrue(response.status_code == 200)

    #Test find_book
    def test_d_find_book(self):
        response = self.client.get(
            url_for('api.find_book',kind=4,page=1,_external=True),
            content_type = 'application/json')
        self.assertTrue(response.status_code == 200)

    #Test lend_book
    def test_f_lend_book(self):
        response = self.client.post(
            url_for('api.lend_book',_external=True),
            headers={
                "token":TOKEN ,
            },
            data = json.dumps({
                "book":'algorithm',
                "realname":'shiina',
            }),
            content_type = 'application/json')
        self.assertTrue(response.status_code == 200)

    #Test mybooks
    def test_g_mybooks(self):
        response = self.client.post(
            url_for('api.mybooks',_external=True),
            headers={"token": TOKEN},
            data = json.dumps({
                "username":'shiina',
            }),
            content_type = 'application/json')
        self.assertTrue(response.status_code == 200)

    #Test return_book
    def test_e_return_book(self):
        response = self.client.post(
            url_for('api.return_book',_external=True),
            headers={
                "token" : TOKEN,
            },
            data = json.dumps({
		"no" : 'T0001',
		"username" : 'shiina'
            }),
            content_type = 'application/json')
        self.assertTrue(response.status_code == 200)


    #----------API FILE NAME:/home/shiina/MUXI/muxibook/muxibook_app/api//__init__.py-------------------

