from setup_tests import BaseTestSetup
from app.models import BucketListItem
from app.resources import validate_input


class TestModels(BaseTestSetup):
    '''Tests for db models'''

    def test_table_relationships(self):
        '''Test for the cascading properties of the relationships'''
        data = {'name': 'My Bucketlist Item', 'done': 'False'}
        self.app.post(
            '/v1/bucketlists/1/items/',
            data=data,
            headers=self.header_content_token)
        self.app.delete(
            '/v1/bucketlists/1/',
            headers=self.header_content_token)
        item_count = BucketListItem.query.count()
        self.assertEqual(item_count, 0)

    def test_page_and_limit_values(self):
        '''Test that the page and limit values are integers'''
        limit_status = validate_input('fhdjjd', 'Limit')
        page_status = validate_input('page2', 'Page')
        assert limit_status is not True
        assert page_status is not True
