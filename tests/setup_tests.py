from manage import app, db
from flask_testing import TestCase
from app.models import BucketList
from config import config_settings
# import os


class BaseTestSetup(TestCase):

    def create_app(self):
        """Test Configuration"""
        app.config.from_object(config_settings['testing'])
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        self.database = db
        self.b_list = BucketList
        db.create_all()

        # Register Test Users
        self.reg_data = {'email': 'brian@gmail.com', 'password': 'password123'}
        self.reg_response = self.app.post(
            '/v1/auth/register/',
            data=self.reg_data)  # Response when user Registers

        # Generate token to be used for testing routes that require login
        login_response = self.app.post(
            '/v1/auth/login/', data=self.reg_data)  # Login User
        login_response_message = login_response.json
        self.header_content_token = {
            'Authorization': login_response_message['token']}

        # Create bucketlist to be used for tests
        self.bucket_list_form = {'name': 'My Bucketlist'}
        self.bucket_list_response = self.app.post(
            '/v1/bucketlists/',
            data=self.bucket_list_form,
            headers=self.header_content_token)

    def tearDown(self):
        """Clearing all DB contents"""
        db.session.remove()
        db.drop_all()
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # os.remove(dir_path + '/testdb.sqlite')
