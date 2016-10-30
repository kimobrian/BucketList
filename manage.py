from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.resources import Homepage, Login, Register, BucketListsAction, \
    BucketListItemAction
from flask_restful import Api

manager = Manager(app)
api = Api(app)
migrate = Migrate(app, db)

api.add_resource(Homepage, '/', endpoint='homepage')
api.add_resource(Login, '/auth/login/', endpoint='login')
api.add_resource(Register, '/auth/register/', endpoint='register')
api.add_resource(
    BucketListsAction,
    '/bucketlists/<bucketlist_id>/',
    endpoint='single_bucket_list')
api.add_resource(BucketListsAction, '/bucketlists/', endpoint='bucketlists')
api.add_resource(
    BucketListItemAction,
    '/bucketlists/<bucketlist_id>/items/',
    endpoint='bucket_list_items')
api.add_resource(
    BucketListItemAction,
    '/bucketlists/<bucketlist_id>/items/<item_id>/',
    endpoint='bucketlist_item_update_delete')

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
