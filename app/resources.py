from flask_restful import Resource, request
from functools import wraps
from app import db
from app.models import User, BucketList, BucketListItem
from datetime import datetime, timedelta
import jwt
from flask import jsonify, g


encryption_secret = 'gd46.;[/]9j$%^gk)-jt+4'
def create_token(user):
    '''Create JSON authentication token'''
    pass

def parse_token(req):
    '''Decode JSON authentication token'''
    pass

def login_required(f):
    '''Decorator to control API access'''
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.headers.get('Authorization'):
            response = jsonify(message='Missing authorization header')
            response.status_code = 401  # Unauthorized access
            return response

        try:
            payload = parse_token(request)
        except DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function

class Homepage(Resource):
    def get(self):
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

    @login_required
    def get(self, bucketlist_id=None):
        '''List all the created bucket lists by a user'''
        '''Get single bucket list if Id is provided'''
        pass
    @login_required
    def post(self):
        '''Create a new bucket list'''
        pass

    @login_required
    def put(self, bucketlist_id=None):
        '''Update this bucket list'''
        pass

    @login_required
    def delete(self, bucketlist_id=None):
        '''Delete this single bucket list'''
        pass

class BucketListItemAction(Resource):
    """Bucketlists Items controller """
    @login_required
    def post(self, bucketlist_id):
        '''Create a new item in bucket list'''
        pass

    @login_required
    def put(self, bucketlist_id, item_id):
        '''Update a bucket list item'''
        pass

    @login_required
    def delete(self, bucketlist_id, item_id):
        '''Delete an item in a bucket list'''
        pass
