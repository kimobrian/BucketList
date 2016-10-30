from setup_tests import BaseTestSetup


class TestItemsEndpoints(BaseTestSetup):
    '''Tests for bucketlits items endpoints'''

    def test_creation_of_empty_item(self):
        '''Test creation of bucket list item with empty data'''
        data = {'name': ''}
        response = self.app.post(
            '/bucketlists/1/items/',
            data=data,
            headers=self.header_content_token)
        self.assertEquals(
            response.json, {
                'message': 'Please provide bucketlist item data'})

    def test_creation_of_empty_item_in_a_missing_bucket_list(self):
        '''
        Test creation of bucket list item in a
        bucketlist that does not exist
        '''
        data = {'name': 'My Bucketlist Item'}
        response = self.app.post(
            '/bucketlists/20/items/',
            data=data,
            headers=self.header_content_token)
        self.assertEquals(response.json, {'message': 'Missing bucketlist ID'})

    def test_successful_creation_of_bucket_list_item(self):
        '''Test for successful creation of item'''
        data = {'name': 'My Bucketlist Item'}
        response = self.app.post(
            '/bucketlists/1/items/',
            data=data,
            headers=self.header_content_token)
        self.assertEquals(
            response.json, {
                'message': 'Bucket List Item Saved Successfully'})

    def test_creation_of_duplicate_item_name(self):
        '''Test creation of duplicate item in the same bucket list'''
        data = {'name': 'My Bucketlist Item'}
        self.app.post(
            '/bucketlists/1/items/',
            data=data,
            headers=self.header_content_token)
        response2 = self.app.post(
            '/bucketlists/1/items/',
            data=data,
            headers=self.header_content_token)
        self.assertEqual(
            response2.json, {
                'message': 'Bucket List Item with that description exists'})

    def test_update_item_with_empty_information(self):
        '''Test update of item with no data provided'''
        data = {'name': ''}
        response = self.app.put(
            '/bucketlists/1/items/1/',
            data=data,
            headers=self.header_content_token)
        self.assertEqual(
            response.json, {
                'message': 'Please provide update info'})

    def test_update_of_duplicate_item(self):
        '''Test updating an item with a description that is already in use'''
        data = {'name': 'Be a professional programmer'}
        self.app.post(
            '/bucketlists/1/items/',
            data=data,
            headers=self.header_content_token)  # Create new item
        responseB = self.app.put(
            '/bucketlists/1/items/1/',
            data=data,
            headers=self.header_content_token)
        self.assertEqual(
            responseB.json, {
                'message': 'Bucket List Item with that description exists'})

    def test_update_item_in_non_existent_bucket_list(self):
        '''
        Test updating an item that does not
        exist(e.g Wrong bucketlist id)
        '''
        data = {'name': 'Be a professional programmer'}
        response = self.app.put(
            '/bucketlists/23/items/1/',
            data=data,
            headers=self.header_content_token)
        self.assertEqual(
            response.json, {
                'message': 'No bucket list item with that Id exists'})

    def test_for_successful_update_of_item(self):
        '''Test that item was updated Successfully'''
        data = {'name': 'Be a professional programmer'}
        self.app.post(
            '/bucketlists/1/items/',
            data=data,
            headers=self.header_content_token)  # Create new item
        data = {'name': 'Be a professional programmer and teacher'}
        responseB = self.app.put(
            '/bucketlists/1/items/1/',
            data=data,
            headers=self.header_content_token)
        self.assertEqual(
            responseB.json, {
                'message': 'Item updated Successfully'})

    def test_deleting_item_from_bucketlist_that_does_not_exist(self):
        '''
        Test for deleting an item where
        given bucketlist id does not exist
        '''
        response = self.app.delete(
            '/bucketlists/23/items/1/',
            headers=self.header_content_token)
        self.assertEqual(
            response.json, {
                'message': 'No bucketlist with given ID'})

    def test_deletion_of_an_item_that_does_not_exist(self):
        '''Test deletion of item whose id does not exist'''
        response = self.app.delete(
            '/bucketlists/1/items/43/',
            headers=self.header_content_token)
        self.assertEquals(
            response.json, {
                'message': 'No bucket list item with that Id exists'})

    def test_successful_deletion_of_an_item(self):
        '''Test that an item is deleted succesfully'''
        data = {'name': 'Be a professional programmer'}
        self.app.post(
            '/bucketlists/1/items/',
            data=data,
            headers=self.header_content_token)  # Create new item
        responseB = self.app.delete(
            '/bucketlists/1/items/1/',
            data=data,
            headers=self.header_content_token)
        self.assertEqual(
            responseB.json, {
                'message': 'BucketList Deleted Successfully'})
