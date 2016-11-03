from flask_restful import Resource, request
from functools import wraps
from app import db
from app.models import User
from datetime import datetime, timedelta
import jwt
from flask import jsonify, g


encryption_secret = 'gd46.;[/]9j$%^gk)-jt+4'


def create_token(user):
    '''Create JSON authentication token'''
    payload = {
        'sub': user.id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=10)
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
        except jwt.DecodeError:
            response = jsonify(message='Token is invalid')
            response.status_code = 401
            return response
        except jwt.ExpiredSignature:
            response = jsonify(message='Token has expired')
            response.status_code = 401
            return response

        g.user_id = payload['sub']

        return f(*args, **kwargs)

    return decorated_function


class Homepage(Resource):

    def get(self):
        response = jsonify({'message': 'Welcome to BucketList API'})
        response.status_code = 200
        return response


class Login(Resource):
    '''Login Controller'''

    def post(self):
        '''Login user'''
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            response = jsonify(
                {'message': 'Provide both username and password'})
            response.status_code = 400
            return response
        try:
            user = User.query.filter_by(email=email).one()
            passcode_status = user.check_password(password)
            if passcode_status:
                token = create_token(user)
                response = jsonify({'message': 'Logged In', 'token': token})
                response.status_code = 200
                return response
            else:
                response = jsonify({'message': 'Failed Logged In'})
                response.status_code = 401
                return response
        except Exception:
            db.session.rollback()
            response = jsonify(
                {'message': 'Invalid email, password combination'})
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
        db.session.add(user)
        try:
            db.session.commit()
            response = jsonify({'message': 'Registered Successfully'})
            response.status_code = 200
            return response
        except Exception:
            response = jsonify({'message': 'Email address already in use'})
            response.status_code = 400
            return response
