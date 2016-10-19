from app import db
from datetime import datetime, timedelta
from passlib.apps import custom_app_context as pwd_context


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, index=True,
                             default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, index=True, default=db.func.current_timestamp(
    ), onupdate=db.func.current_timestamp())

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.add(self)
        db.session.delete(self)
        db.session.commit()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    id_number = db.Column(db.Integer, unique=True)
    email = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))
    bucket_list = db.relationship('BucketList', backref='owner', lazy='dynamic')

    def __init__(self, email=None, password=None):
        if email:
            self.email = email.lower()
        if password:
            self.set_password(password)

    def set_password(self, password):
        self.password = pwd_context.encrypt(password)

    def check_password(self, password):
        return pwd_context.verify(password, self.password)


class BucketLists(Base):
    __tablename__ = 'bucketlists'
    name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_by = db.Column(db.String(64))
    items = db.relationship('BucketListItem', backref='bucketlists',
                            cascade="all, delete-orphan", lazy='dynamic')

    # def to_json(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "items_count": len(self.items.all()),
    #         "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
    #         "date_modified": self.date_modified.strftime("%Y-%m-%d %H:%M:%S"),
    #         "created_by": self.created_by,
    #     }


class BucketListItem(Base):

    '''Item model defined for api service. '''

    __tablename__ = 'items'
    name = db.Column(db.String(64))
    done = db.Column(db.Boolean, default=False, nullable=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(
        'bucketlists.id'), nullable=False)

    def to_json(self):
        ''' Method to convert objects to python dictioary format.'''

        return {
            "id": self.id,
            "name": self.name,
            "date_created": self.date_created.strftime("%Y-%m-%d %H:%M:%S"),
            "date_modified": self.date_modified.strftime("%Y-%m-%d %H:%M:%S"),
            "done": self.done,
        }

