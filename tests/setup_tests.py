from app import app, db
from flask_testing import TestCase
from app.models import User, BucketList, BucketListItem
from datetime import datetime
import glob


class BaseTestSetup(TestCase):

    def create_app(self):
        """Test Configuration"""
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tests/testdb.sqlite'
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.app = self.create_app().test_client()
        db.create_all()

        user = User(
            # username="Brian Kimo",
            email="brian@gmail.com",
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


    def tearDown(self):
        """Clearing all DB contents"""
        db.session.remove()
        db.drop_all()
