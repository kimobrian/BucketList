from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db
from app.resources import *
from flask_restful import Api

manager = Manager(app)
api = Api(app)
migrate = Migrate(app, db)

api.add_resource(HelloWorld, '/')

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()