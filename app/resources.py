from flask_restful import Resource
from functools import wraps
from app.models import User, BucketList, BucketListItem
from datetime import datetime, timedelta
from flask_restful import reqparse


def create_token(user):
    '''Create JSON authentication token'''
    pass

def parse_token(req):
    '''Decode JSON authentication token'''
    pass

def login_required(f):
    '''Decorator to control API access'''
    pass

class Login(Resource):
    '''Login Controller'''

    def post(self):
        '''Login user'''
        pass

class Register(Resource):
    '''Register user'''

    def post(self):
        '''Register User'''
        pass

class BucketListsAction(Resource):
    '''Bucketlists controller'''

    def get(self, id):
        '''List all the created bucket lists'''
        '''Get single bucket list if Id is provided'''
        pass

    def post(self):
        '''Create a new bucket list'''
        pass

    def put(self, id):
        '''Update this bucket list'''
        pass

    def delete(self, id):
        '''Delete this single bucket list'''
        pass

class BucketListItemAction(Resource):
    """Bucketlists Items controller """
    def post(self, id):
        '''Create a new item in bucket list'''
        pass

    def put(self, bucketlist_id, item_id):
        '''Update a bucket list item'''
        pass

    def delete(self, bucketlist_id, item_id):
        '''Delete an item in a bucket list'''
        pass
