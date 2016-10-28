from flask_restful import Resource, request
from functools import wraps
from app import db
from app.models import User, BucketList, BucketListItem
from datetime import datetime, timedelta
import jwt
from flask import jsonify


encryption_secret = 'gd46.;[/]9j$%^gk)-jt+4'
def create_token(user):
    '''Create JSON authentication token'''
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=5)
    }
    token = jwt.encode(payload, encryption_secret, algorithm='HS256')
    return token.decode('unicode_escape')

def parse_token(req):
    '''Decode JSON authentication token'''
    token = req.headers.get('Authorization')
    return jwt.decode(token, encryption_secret)

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
        response = jsonify({'message': 'Welcome to Bucketlist API'})
        response.status_code = 200
        return response

class Login(Resource):
    '''Login Controller'''

    def post(self):
        '''Login user'''
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            response = jsonify({'message': 'Provide both username and password'})
            response.status_code = 400
            return response
        try:
            user = User.query.filter_by(email=email).one()
        except Exception as e:
            response = jsonify({'message': 'Invalid email, password combination'})
            response.status_code = 401
            return response
        passcode_status = user.check_password(password)
        if(passcode_status):
            token = create_token(user)
            response = jsonify({'message': 'Logged In', 'token': token})
            response.status_code = 200
            return response
        else:
            response = jsonify({'message': 'Failed Logged In'})
            response.status_code = 401
            return response

class Register(Resource):
    '''Register user'''

    def post(self):
        '''Register User'''
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            response = jsonify({'message': 'Provide both email and password'})
            response.status_code = 400
            return response
        user = User(email, password)
        user.set_password(password)
        db.session.add(user)
        try:
            db.session.commit()
        except Exception as exc:
            print(exc)
            response = jsonify({'message': 'Email address already in use'})
            response.status_code = 400
            return response
        response = jsonify({'message': 'Registered Successfully'})
        response.status_code = 200
        return response

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
