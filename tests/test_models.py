from app.models import BucketListItem
from setup_tests import BaseTestSetup


class ModelTests(BaseTestSetup):
    '''Testing the model structure e.g Relationships'''

    def test_cascading_deletion_of_items(self):
        '''Test that deltion of BucketList also deletes the items for the bucketlist'''
        data = {'name': 'My Bucket List Item'}
        response = self.app.post('/bucketlists/1/items/', data=data, headers=self.header_content_token)
        delete_response = self.app.delete('/bucketlists/1/', headers=self.header_content_token)
        items_count = BucketListItem.query.filter_by(bucketlist_id=1).count()
        self.assertEquals(items_count, 0)
