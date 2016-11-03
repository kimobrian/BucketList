from app.models import BucketListItem
from flask import jsonify


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
