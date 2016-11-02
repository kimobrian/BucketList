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


def bucketlists_details(bucket_list):
    bucketlist_details = {}
    bucketlist_details['id'] = bucket_list.id
    bucketlist_details['name'] = bucket_list.name
    bucketlist_details['items'] = []
    bucket_list_items = BucketListItem.query.filter_by(
        bucketlist_id=bucket_list.id).all()
    if len(bucket_list_items) > 0:
        for bucketlist_item in bucket_list_items:
            b_list_item_details = bucketlist_item.to_json()
            bucketlist_details['items'].append(b_list_item_details)
    bucketlist_details['date_created'] = bucket_list.date_created
    bucketlist_details['date_modified'] = bucket_list.date_modified
    bucketlist_details['created_by'] = bucket_list.created_by
    return bucketlist_details


def validate_input(value, query_type):
    try:
        value = int(value)
        return True
    except ValueError:
        response = jsonify(
            {'message': query_type + ' must be a number'})
        response.status_code = 200
        return response


class BucketListsAction(Resource):
    '''Bucketlists controller'''

    @login_required
    def get(self, bucketlist_id=None):
        '''List all the created bucket lists by a user'''
        '''Get single bucket list if Id is provided'''

        if bucketlist_id is None:
            query_string = request.args.to_dict()
            limit = query_string.get('limit', 5)
            page = query_string.get('page', 1)
            limit_check = validate_input(limit, 'Limit')
            if limit_check is not True:
                return limit_check
            limit = int(limit)
            page_check = validate_input(page, 'Page')
            if page_check is not True:
                return page_check
            page = int(page)

            if 'q' in query_string:
                bucketlist_name = query_string.get('q')
                bucket_lists = BucketList.query.filter(BucketList.name.ilike(
                    '%' + bucketlist_name + '%')).filter_by(
                    created_by=g.user_id).paginate(page, limit, False)
                if len(bucket_lists.items) < 0:
                    response = jsonify(
                        {'message': 'No Bucket Lists Containing that word'})
                    response.status_code = 200
                    return response
            else:
                bucket_lists = BucketList.query.filter_by(
                    created_by=g.user_id).paginate(page, limit, False)
            all_bucket_lists = []
            if len(bucket_lists.items) > 0:
                for bl in bucket_lists.items:
                    bl_details = bucketlists_details(bl)
                    all_bucket_lists.append(bl_details)
            total_pages = bucket_lists.pages
            next_item = bucket_lists.has_next
            previous_item = bucket_lists.has_prev
            if next_item:
                next_page = str(request.url_root) + 'v1/bucketlists?limit=' + \
                    str(limit) + '&page=' + str(page + 1)
            else:
                next_page = 'None'
            if previous_item:
                previous_page = request.url_root + 'v1/bucketlists?limit=' + \
                    str(limit) + '&page=' + str(page - 1)
            else:
                previous_page = 'None'
            response = jsonify({'bucketlists': all_bucket_lists,
                                'pages': total_pages,
                                'previous': previous_page,
                                'next': next_page})
            response.status_code = 200
            return response
        else:
            try:
                bucket_list = BucketList.query.filter_by(
                    id=int(bucketlist_id), created_by=g.user_id).one()
                bl_details = bucketlists_details(bucket_list)
                response = jsonify({'Bucket List': bl_details})
                response.status_code = 200
                return response
            except Exception:
                response = jsonify({'message': 'No Bucket List with that ID'})
                response.status_code = 200
                return response

    @login_required
    def post(self, bucketlist_id=None):
        '''Create a new bucket list'''
        if bucketlist_id is not None:
            response = jsonify(
                {'message': 'New bucketlist creation does not require an ID'})
            response.status_code = 400
            return response
        name = request.form['name']
        if not name:
            response = jsonify(
                {'message': 'Please provide name for your bucketlist'})
            response.status_code = 400
            return response
        try:
            BucketList.query.filter_by(
                name=name, created_by=g.user_id).one()
            response = jsonify({'message': 'Bucketlist name already exists'})
            response.status_code = 400
            return response
        except Exception:  # No Result Found
            bucketlist = BucketList()
            bucketlist.name = name
            bucketlist.created_by = g.user_id
            db.session.add(bucketlist)
            try:
                db.session.commit()
                response = jsonify(
                    {'message': 'Bucketlist Created Successfully'})
                response.status_code = 200
                return response
            except Exception:
                response = jsonify(
                    {'message': 'Error Occurred Saving Bucketlist'})
                response.status_code = 200
                return response

    @login_required
    def put(self, bucketlist_id=None):
        '''Update this bucket list'''
        if bucketlist_id is None:
            response = jsonify(
                {'message': 'Provide Id of Bucketlist to Edit'})
            response.status_code = 200
            return response
        new_data = request.form['name']
        if not new_data:
            response = jsonify(
                {'message': 'Please provide new Bucket List Name'})
            response.status_code = 200
            return response
        try:
            BucketList.query.filter_by(
                name=new_data, created_by=g.user_id).one()
            response = jsonify({'message': 'Name already in use'})
            response.status_code = 200
            return response
        except Exception:  # No bucketlist with the name found(Safe update)
            updated_rows = BucketList.query.filter_by(
                id=bucketlist_id, created_by=g.user_id).update(
                {'name': new_data})
            if updated_rows == 0:
                response = jsonify({'message': 'No bucketlist with that ID'})
                response.status_code = 200
                return response
            elif updated_rows > 0:
                try:
                    db.session.commit()
                    response = jsonify(
                        {'message': 'Bucket List updated Successfully'})
                    response.status_code = 200
                    return response
                except Exception:
                    response = jsonify(
                        {'message': 'Error Occurred Updating Bucket List'})
                    response.status_code = 200
                    return response

    @login_required
    def delete(self, bucketlist_id=None):
        '''Delete this single bucket list'''
        if bucketlist_id is None:
            response = jsonify(
                {'message': 'Provide Id of bucket list to delete'})
            response.status_code = 200
            return response
        deleted_rows = BucketList.query.filter_by(
            created_by=g.user_id, id=bucketlist_id).delete()
        db.session.commit()
        if deleted_rows == 0:
            response = jsonify({'message': 'No Bucket List with that ID'})
            response.status_code = 200
            return response
        elif deleted_rows > 0:
            response = jsonify({'message': 'BucketList Deleted Successfully'})
            response.status_code = 200
            return response


class BucketListItemAction(Resource):
    """Bucketlists Items controller """
    @login_required
    def post(self, bucketlist_id):
        '''Create a new item in bucket list'''
        try:
            BucketList.query.filter_by(
                id=bucketlist_id).one()
            item_name = request.form['name']
            if not item_name:
                response = jsonify(
                    {'message': 'Please provide bucketlist item data'})
                response.status_code = 200
                return response
            else:
                check_item = BucketListItem.query.filter_by(
                    name=item_name, bucketlist_id=bucketlist_id).all()
                if len(check_item) > 0:
                    response = jsonify({
                        'message':
                        'Bucket List Item with that description exists'
                    })
                    response.status_code = 200
                    return response
                else:
                    bucket_list_item = BucketListItem()
                    bucket_list_item.name = item_name
                    bucket_list_item.bucketlist_id = bucketlist_id
                    db.session.add(bucket_list_item)
                    try:
                        db.session.commit()
                        response = jsonify(
                            {'message': 'Bucket List Item Saved Successfully'})
                        response.status_code = 200
                        return response
                    except Exception:
                        response = jsonify(
                            {'message': 'Error Occurred Saving Item'})
                        response.status_code = 200
                        return response
        except Exception:
            response = jsonify({'message': 'Missing bucketlist ID'})
            response.status_code = 200
            return response

    @login_required
    def put(self, bucketlist_id, item_id=None):
        '''Update a bucket list item'''
        if item_id is None:
            response = jsonify(
                {'message': 'Please provide Id of Item to update'})
            response.status_code = 200
            return response
        data = request.form['name']
        done = request.form['done']
        if not done:
            done = False
        if done.lower() not in ['true', 'false']:
            response = jsonify({'message': 'Done can either be True or False'})
            response.status_code = 200
            return response
        if not data:
            response = jsonify({'message': 'Please provide update info'})
            response.status_code = 200
            return response
        try:
            BucketListItem.query.filter_by(
                id=item_id, bucketlist_id=bucketlist_id).one()
            try:
                BucketListItem.query.filter_by(
                    name=data, bucketlist_id=bucketlist_id).one()
                response = jsonify(
                    {'message':
                     'Bucket List Item with that description exists'})
                response.status_code = 200
                return response
            except Exception:
                try:
                    # Check bucketlist ID
                    BucketList.query.filter_by(
                        id=bucketlist_id).one()
                    BucketListItem.query.filter_by(id=item_id).update(
                        {'name': data, 'done': done})
                    try:
                        db.session.commit()
                        response = jsonify(
                            {'message': 'Item updated Successfully'})
                        response.status_code = 200
                        return response
                    except Exception:
                        response = jsonify(
                            {'message': 'Error Occurred Updating Item'})
                        response.status_code = 200
                        return response
                except Exception as exc:
                    print(exc)
                    response = jsonify(
                        {'message':
                         'The Item does not belong to any known bucketlist'})
                    response.status_code = 200
                    return response
        except Exception:
            response = jsonify(
                {'message': 'No bucket list item with that Id exists'})
            response.status_code = 200
            return response

    @login_required
    def delete(self, bucketlist_id, item_id=None):
        '''Delete an item in a bucket list'''
        if item_id is None:
            response = jsonify(
                {'message': 'Please provide Id of item to delete'})
            response.status_code = 200
            return response
        try:
            # Check list ID
            BucketList.query.filter_by(
                id=bucketlist_id).one()
        except Exception:
            db.session.commit()
            response = jsonify({'message': 'No bucketlist with given ID'})
            response.status_code = 200
            return response
        try:
            # Check item ID
            BucketListItem.query.filter_by(
                id=item_id, bucketlist_id=bucketlist_id).one()
            deleted_records = BucketListItem.query.filter_by(
                id=item_id, bucketlist_id=bucketlist_id).delete()
            if deleted_records > 0:
                db.session.commit()
                response = jsonify(
                    {'message': 'BucketList Deleted Successfully'})
                response.status_code = 200
                return response
        except Exception:
            response = jsonify(
                {'message': 'No bucket list item with that Id exists'})
            response.status_code = 200
            return response
