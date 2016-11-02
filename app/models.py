from app import db
from passlib.apps import custom_app_context as pwd_context


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(
        db.DateTime,
        index=True,
        default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime,
        index=True,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128))
    bucket_list = db.relationship(
        'BucketList',
        backref='owner',
        lazy='dynamic')

    def __init__(self, email, password):
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = pwd_context.encrypt(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)


class BucketList(BaseModel):
    __tablename__ = 'bucketlists'
    name = db.Column(db.String(64), unique=True)
    created_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    items = db.relationship(
        'BucketListItem',
        backref='bucketlists',
        passive_deletes=True)


class BucketListItem(BaseModel):
    '''Item model defined for api service. '''
    __tablename__ = 'items'
    name = db.Column(db.String(64))
    done = db.Column(db.Boolean, default=False, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
        'bucketlists.id', ondelete='CASCADE'), nullable=False)

    def to_json(self):
        ''' Return bucket list item details'''
        b_list_item_details = {}
        b_list_item_details['id'] = self.id
        b_list_item_details['name'] = self.name
        b_list_item_details['date_created'] = self.date_created
        b_list_item_details['date_modified'] = self.date_modified
        b_list_item_details['done'] = self.done
        return b_list_item_details
