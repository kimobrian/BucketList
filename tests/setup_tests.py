from manage import app, db
from flask_testing import TestCase
from app.models import User, BucketList, BucketListItem
from datetime import datetime
from config import config_settings
import os
import json
from flask import url_for

class BaseTestSetup(TestCase):

    def create_app(self):
        """Test Configuration"""
        app.config.from_object(config_settings['testing'])
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        db.create_all()

        user = User(
            email="brian_kim@gmail.com",
            password="complex_pass"
        )

        db.session.add(user)
        db.session.commit()

        bucketlist = BucketList(
            name="Todo List",
            date_created=datetime.now(),
            date_modified=datetime.now(),
            created_by=user.id
        )

        db.session.add(bucketlist)
        db.session.commit()

        bucketlist_item = BucketListItem(
            name='Todo A',
            bucketlist_id=bucketlist.id
        )

        db.session.add(bucketlist_item)
        db.session.commit()
        self.auth_token = ''

        # reg_details = {'email': 'unique@gmail.com', 'password': 'password123'}
        # response = self.app.post('/auth/register/', data=reg_details, content_type="application/json")
        # self.auth_token = ''
        # login_details = {'email': 'unique@gmail.com', 'password': 'password123'}
        # response = self.app.post('/auth/login/', data=json.dumps(login_details), content_type="application/json")
        # response_data = response.json
        # self.auth_token = {'Authorization': response_data['token']}


    def tearDown(self):
        """Clearing all DB contents"""
        db.session.remove()
        db.drop_all()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.remove(dir_path+'/testdb.sqlite')
