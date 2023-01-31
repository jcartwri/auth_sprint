import datetime
import http
import uuid

from api.v1 import messages
from database.db import db
from flask_restful import abort
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    role_name = db.Column(db.String(length=30), unique=True, nullable=False)
    register_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self) -> str:
        return f"Role {self.role_name} {self.id}"

    @classmethod
    def find_by_role_id(cls, role_id: str):
        return cls.query.filter(cls.id == role_id).first()

    @classmethod
    def find_by_role_name(cls, role_name: str):
        return cls.query.filter(cls.role_name == role_name).first()

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except Exception as e:
            return {'message': 'Something went wrong: {}'.format(e)}

    @classmethod
    def delete_by_id(cls, role_id: str):
        role = cls.query.filter(cls.id == role_id).first()
        if role:
            db.session.delete(role)
            db.session.commit()
        else:
            message: dict = {"message": messages.OBJECT_NOT_FOUND, "errors": []}
            abort(http_status_code=http.HTTPStatus.NOT_FOUND, message=message)

    @classmethod
    def by_name_exist(cls, role_name: str) -> bool:
        return db.session.query(
            cls.query.filter(cls.role_name == role_name).exists()
        ).scalar()
