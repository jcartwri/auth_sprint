import datetime
import uuid

from database.db import db
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    login = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True)
    last_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    is_staff = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True, server_default='true')
    is_superuser = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.String)
    subscription = db.Column(db.String, default=False)
    register_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def change_credential(self, password):
        self.password = self.generate_hash(password)

    @classmethod
    def find_by_username(cls, login):
        return cls.query.filter_by(login=login).first()

    @classmethod
    def find_by_user_id(cls, id_):
        return cls.query.filter_by(id=id_).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': str(x.login),
                'password': str(x.password),
                'email': str(x.email)
            }
        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except Exception as e:
            return {'message': 'Something went wrong: {}'.format(e)}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

    def __repr__(self):
        return f'<User {self.login}>'


