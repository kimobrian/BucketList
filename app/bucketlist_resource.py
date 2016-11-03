from app import db
from app.models import BucketList
from flask import g, jsonify
from flask_restful import Resource, request
from helpers import validate_input, bucketlists_details
from main_resource import login_required
from sqlalchemy.orm.exc import NoResultFound


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
            except NoResultFound:
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
        except NoResultFound:  # No Result Found
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
                db.session.rollback()
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
        except NoResultFound:  # No bucketlist with the name found(Safe update)
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
                    db.session.rollback()
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
