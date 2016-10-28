from app.models import User, BucketList, BucketListItem
from setup_tests import BaseTestSetup
from nose.tools import assert_equal


class ModelTests(BaseTestSetup):

    def test_user_saved(self):
        users = User.query.count()
        assert users == 1

    def test_bucketlist_created(self):
        bucketlists = BucketList.query.count()
        assert_equal(bucketlists, 1)

    def test_bucketlist_item_created(self):
        bucketlist_items = BucketListItem.query.count()
        assert_equal(bucketlist_items, 1)
