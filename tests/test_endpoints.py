from setup_tests import BaseTestSetup
from flask import g
from app.models import User


class EndpointTests(BaseTestSetup):
    '''Tests for API endpoints'''

    def test_homepage(self):
        '''Test the Response from the Homepage'''
        response = self.app.get('/')
        response_data = response.json
        self.assertEquals(
            response_data, {
                'message': 'Welcome to BucketList API'})

    def test_login_with_valid_details(self):
        '''Test User Login with valid details'''
        login_response = self.app.post(
            '/auth/login/', data=self.reg_data)  # Login User
        login_response_message = login_response.json
        res_message = login_response_message['message']
        self.assertEquals(res_message, 'Logged In', msg='Login Failed')
        self.assert200(login_response, message='Login Failed')

    def test_login_with_invalid_details(self):
        '''
        Test User Login with invalid details
        Not Available in DB
        '''
        data = {'email': 'wrong@gmail.com', 'password': 'wrong_pass'}
        response = self.app.post('/auth/login/', data=data)
        self.assertEqual(
            response.json, {
                'message': 'Invalid email, password combination'})
        self.assert401(response, message='Login Failed')

    def test_login_without_details(self):
        '''Test user login without providing login details'''
        login_data = {'email': '', 'password': ''}
        response = self.app.post('/auth/login/', data=login_data)
        self.assertEqual(
            response.json, {
                'message': 'Provide both username and password'})
        self.assert400(response)

    def test_user_register_with_details(self):
        '''Test user registration when email and password are provided'''
        current_users_count = User.query.count()  # Count before reg
        data = {'email': 'kevin123@gmail.com', 'password': 'password123'}
        response = self.app.post('/auth/register/', data=data)
        after_registration_count = User.query.count()  # Count after reg
        self.assertEqual(after_registration_count - current_users_count, 1)
        self.assertEqual(response.json, {'message': 'Registered Successfully'})

    def test_user_register_without_details(self):
        '''Test user registration when email or password are not provided'''
        data = {'email': '', 'password': ''}
        response = self.app.post('/auth/register/', data=data)
        self.assertEqual(
            response.json, {
                'message': 'Provide both email and password'})
        self.assert400(response)

    def test_registration_for_unique_email(self):
        '''Test for unique registration email'''
        responseB = self.app.post(
            '/auth/register/',
            data=self.reg_data)  # Registration with same email address
        responseB_data = responseB.json
        self.assertEqual(
            responseB_data, {
                'message': 'Email address already in use'})
        self.assert400(
            responseB,
            message='Email is not in use(Valid Registration)')

    def test_bucket_lists_result_with_non_existent_id(self):
        '''
        Test bucketlists result when the id provided is
        not available(Single Bucketlist)
        '''
        response = self.app.get(
            '/bucketlists/43/',
            headers=self.header_content_token)
        self.assertEquals(
            response.json, {
                'message': 'No Bucket List with that ID'})
        self.assert200(response)

    def test_bucket_lists_result_with_existing_id(self):
        '''
        Test bucketlists result when the
        id provided is available(Single Bucketlist)
        '''
        response = self.app.get(
            '/bucketlists/1/',
            headers=self.header_content_token)
        self.assertIn('Bucket List', response.json)
        self.assert200(response)

    def test_bucket_list_results_when_none_exist(self):
        '''
        Test for bucketlist results when
        user has not created any bucket lists
        '''
        # Delete all bucketlists by user first
        self.BL.query.filter_by(created_by=g.user_id).delete()
        self.database.session.commit()
        response = self.app.get(
            '/bucketlists/',
            headers=self.header_content_token)
        self.assertEquals(
            response.json, {
                'message': 'No Bucket Lists Created'})
        self.assert200(response)

    def test_bucket_list_result_when_they_have_been_created(self):
        '''Test bucketlist results when some have been created'''
        response = self.app.get(
            '/bucketlists/',
            headers=self.header_content_token)
        self.assertIn('info', response.json)
        self.assert200(response)

    def test_bucket_lists_when_not_authenticated(self):
        '''Test bucketlists result when no authorization header is provided'''
        responseB = self.app.get('/bucketlists/')
        self.assert401(responseB, message='Missing Authentication Token')

    def test_creation_of_bucket_list_with_no_name(self):
        '''Test for creation of bucket list with no name'''
        data = {'name': ''}
        response = self.app.post(
            '/bucketlists/',
            data=data,
            headers=self.header_content_token)
        self.assertEqual(
            response.json, {
                'message': 'Please provide name for your bucketlist'})
        self.assert400(response)

    def test_creation_of_bucket_list_with_name_that_exists(self):
        '''
        Test for creating a bucketlist with name
        that already exists on user list
        '''
        response = self.app.post(
            '/bucketlists/',
            data=self.bucket_list_form,
            headers=self.header_content_token)
        self.assertEqual(
            response.json, {
                'message': 'Bucketlist name already exists'})
        self.assert400(response)

    def test_successful_creation_of_bucket_list(self):
        '''Test for creation of new bucket list with valid data'''
        data = {'name': 'BucketList By Brian'}
        response = self.app.post(
            '/bucketlists/',
            data=data,
            headers=self.header_content_token)
        self.assertEqual(
            response.json, {
                'message': 'Bucketlist Created Successfully'})
        self.assert200(response)

    def test_update_of_bucket_list_with_no_new_data(self):
        '''Test for update of existing bucket list proving empty data'''
        data = {'name': ''}
        response = self.app.put(
            '/bucketlists/1/',
            data=data,
            headers=self.header_content_token)
        self.assertEqual(
            response.json, {
                'message': 'Please provide new Bucket List Name'})
        self.assert200(response)

    def test_update_of_bucket_list_with_name_that_exists(self):
        '''
        Test for update of existing bucket list
        providing name that is already in use
        '''
        # Create a new bucket list to test duplicate names
        data = {'name': 'My New Bucketlist'}
        self.app.post(
            '/bucketlists/', data=data, headers=self.header_content_token)
        response = self.app.put(
            '/bucketlists/1/',
            data=data,
            headers=self.header_content_token)
        self.assertEqual(response.json, {'message': 'Name already in use'})
        self.assert200(response)

    def test_update_of_bucket_list_with_non_existent_id(self):
        '''
        Test for update of non existent bucketlist
        (No Bucket list with given ID)
        '''
        data = {'name': 'My New Bucketlist'}
        response = self.app.put(
            '/bucketlists/23/',
            data=data,
            headers=self.header_content_token)
        self.assertEqual(
            response.json, {
                'message': 'No bucketlist with that ID'})
        self.assert200(response)

    def test_update_of_bucket_that_exists(self):
        '''Test for successful update of bucket list'''
        data = {'name': 'My New Bucketlist'}
        response = self.app.put(
            '/bucketlists/1/',
            data=data,
            headers=self.header_content_token)
        self.assertEqual(
            response.json, {
                'message': 'Bucket List updated Successfully'})
        self.assert200(response)

    def test_deletion_of_bucket_list_for_non_existent_id(self):
        '''Test deletion of bucket list with non existent id'''
        response = self.app.delete(
            '/bucketlists/405/',
            headers=self.header_content_token)
        self.assertEqual(
            response.json, {
                'message': 'No Bucket List with that ID'})
        self.assert200(response)

    def test_deletion_of_bucket_list_for_existing_id(self):
        '''Test deletion of bucket list with existing id'''
        response = self.app.delete(
            '/bucketlists/1/',
            headers=self.header_content_token)
        self.assertEqual(
            response.json, {
                'message': 'BucketList Deleted Successfully'})
        self.assert200(response)

    def test_retrieve_bucket_list_items(self):
        '''Test for creation of a new item in a bucket list'''
        response = self.app.post(
            '/bucketlists/id/items/',
            headers=self.header_content_token)
        self.assert200(response, message='Failed to create bucket list item')

    def test_create_token(self):
        '''Test if a token was created for logged in user'''
        login_response = self.app.post(
            '/auth/login/', data=self.reg_data)  # Login User
        self.assertIn(
            'token',
            login_response.json,
            msg='Token was not created')

    def test_retrieve_bucketlist_by_existing_name(self):
        '''Retrieve bucketlist by name that exists'''
        bucket_list_form = {'name': 'Bucketlist one'}
        self.app.post(
            '/bucketlists/',
            data=bucket_list_form,
            headers=self.header_content_token)
        response = self.app.get(
            '/bucketlists/?q=one',
            headers=self.header_content_token)
        self.assertIn('info', response.json)
        self.assert200(response)

    def test_retrieve_bucketlist_with_nonexisting_name(self):
        '''Retrieve bucketlist by name that does not exists'''
        response = self.app.get(
            '/bucketlists/?q=BucketlistMissing',
            headers=self.header_content_token)
        self.assertEqual(
            {'message': 'No Bucket Lists Containing that word'}, response.json)
        self.assert200(response)

    def test_if_bucketlist_limit_is_invalid(self):
        '''Test if number of records to be returned is not a number'''
        response = self.app.get(
            '/bucketlists/?limit=invalid',
            headers=self.header_content_token)
        self.assertEqual(
            {'message': 'Limit of records must be a number'}, response.json)
        self.assert200(response)

    def test_update_of_bucketlist_without_id(self):
        '''Test for editting a bucketlist without providing id'''
        response = self.app.put(
            '/bucketlists/', headers=self.header_content_token)
        self.assertEqual(
            response.json, {'message': 'Provide Id of Bucketlist to Edit'})

    def test_deletion_of_bucketlist_without_id(self):
        '''Try to delete bucketlist withour providing an Id'''
        response = self.app.delete(
            '/bucketlists/', headers=self.header_content_token)
        self.assertEqual(
            {'message': 'Provide Id of bucket list to delete'}, response.json)

    def test_creation_of_bucketlist_with_id(self):
        '''Test creation of bucketlist with an Id provided'''
        response = self.app.post(
            '/bucketlists/1/', headers=self.header_content_token)
        self.assertEqual(
            {'message': 'New bucketlist creation does not require an ID'},
            response.json)
