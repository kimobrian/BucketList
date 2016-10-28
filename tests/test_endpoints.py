from app.resources import Login, Register, BucketListsAction, BucketListItemAction
from setup_tests import BaseTestSetup
from flask import jsonify, url_for
import json


class EndpointTests(BaseTestSetup):
    '''Tests for API endpoints'''

    def test_homepage(self):
        response = self.app.get('/')
        self.assert200(response, message='Request failed with status:'+str(response.status_code))

    def test_login(self):
        '''Test User Login'''
        data = {'email': 'wrong@gmail.com', 'password': 'wrong_pass'}
        response = self.app.post('/auth/login/', data=data)
        self.assert401(response, message='Login Failed')

    def test_user_register_A(self):
        '''Test user registration when email and password are provided'''
        data = {'email': 'kevin123@gmail.com', 'password': 'password123'}
        response = self.app.post('/auth/register/', data=json.dumps(data), content_type='application/json')
        self.assert200(response, message='Registration Failed'+str(response.status_code))

    def test_user_register_B(self):
        '''Test user registration when email or password are not provided'''
        data = {'email': '', 'password': ''}
        response = self.app.post('/auth/register/', data=data)
        self.assert400(response, message='No Registration details provided')

    def test_registration_for_unique_email(self):
        data = {'email': 'brian@gmail.com', 'password': 'password123'}
        response = self.app.post('/auth/register/', data=data)
        self.assert400(response, message='Email already in use')

    def test_bucket_lists_A(self):
        """Test bucketlists result when authorization header is provided"""
        response = self.app.get('/bucketlists/', headers=self.auth_token)
        self.assert200(response, message='Failed to collect bucketlists')

    def test_bucket_lists_B(self):
        """Test bucketlists result when no authorization header is provided"""
        responseB = self.app.get('/bucketlists/')
        self.assert401(responseB, message='Missing Authentication Token')

    def test_creation_of_bucket_list(self):
        '''Test for creation of new bucket list'''
        data = {'name': 'BucketList 1', 'created_by': '1'}
        response = self.app.post('/bucketlists/', headers=self.auth_token)
        assert200(response, message='Failed to create bucket list')

    def test_creation_of_bucket_list(self):
        '''Test for creation of new bucket list'''
        data = {'name': 'BucketList One Changed'}
        response = self.app.put('/bucketlists/1/', headers=self.auth_token)
        self.assert200(response, message='Failed to Update bucket list')

    def test_for_missing_bucket_list_id(self):
        """Test for retrieval of a bucket list with non-existent id"""
        response = self.app.get('/bucketlists/134/', headers=self.auth_token)
        self.assert400(response, message='Missing bucket list Id')

    def test_deletion_of_bucket_list(self):
        '''Test if bucket list has been deleted'''
        response = self.app.delete('/bucketlists/id/', headers=self.auth_token)
        self.assert200(response, message='Failed to delete bucket list')

    def test_get_bucket_list_with_id(self):
        '''Test for retrieval of a bucket list id that exists'''
        response = self.app.get('/bucketlists/1/', headers=self.auth_token)
        self.assert200(response, message='Failed to retrieve bucketlist')

    def test_retrieve_bucket_list_items(self):
        '''Test for creation of a new item in a bucket list'''
        response = self.app.post('/bucketlists/id/items/', headers=self.auth_token)
        self.assert200(response, message='Failed to create bucket list item')

    def test_update_of_bucket_list_item(self):
        '''Test if bucketlist item was created'''
        response = self.app.put('/bucketlists/id/items/item_id/', headers=self.auth_token)
        self.assert200(response, message='Failed to update bucket list item')

    def test_deletion_of_bucket_list_item(self):
        '''Test if bucketlist item was deleted'''
        response = self.app.put('/bucketlists/id/items/item_id/', headers=self.auth_token)
        self.assert200(response, message='Failed to update bucket list item')
