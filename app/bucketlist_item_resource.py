from app import db
from app.models import BucketList, BucketListItem
from flask import jsonify
from flask_restful import Resource, request
from main_resource import login_required
from sqlalchemy.orm.exc import NoResultFound


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
                        db.session.rollback()
                        response = jsonify(
                            {'message': 'Error Occurred Saving Item'})
                        response.status_code = 200
                        return response
        except NoResultFound:
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
            except NoResultFound:
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
        except NoResultFound:
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
        except NoResultFound:
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
        except NoResultFound:
            response = jsonify(
                {'message': 'No bucket list item with that Id exists'})
            response.status_code = 200
            return response
