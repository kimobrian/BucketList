from app import db
from datetime import datetime, timedelta
from passlib.apps import custom_app_context as pwd_context


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, index=True, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, index=True, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def save(self):
        pass

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128))
    bucket_list = db.relationship('BucketList', backref='owner', lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def set_password(self, password):
        pass

    def check_password(self, password):
        pass


class BucketList(BaseModel):
    __tablename__ = 'bucketlists'
    name = db.Column(db.String(64), unique=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('BucketListItem', backref='bucketlists',
                            cascade="all, delete-orphan", lazy='dynamic')


class BucketListItem(BaseModel):

    '''Item model defined for api service. '''

    __tablename__ = 'items'
    name = db.Column(db.String(64))
    done = db.Column(db.Boolean, default=False, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
        'bucketlists.id'), nullable=False)

    def to_json(self):
        ''' Return bucket list item details'''
        pass
