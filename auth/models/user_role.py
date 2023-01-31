import datetime
import http
import uuid

from api.v1 import messages
from database.db import db
from flask_restful import abort
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID


class UserRole(db.Model):
    __tablename__ = "user_role"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), nullable=False)
    register_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_row_by_ids(cls, user_id: str, role_id: str) -> bool:
        return cls.query.filter(cls.user_id == user_id, cls.role_id == role_id).first()

    @classmethod
    def is_row_exist(cls, user_id: uuid.UUID, role_id: uuid.UUID) -> bool:
        return db.session.query(
            cls.query.filter(cls.user_id == user_id, cls.role_id == role_id).exists()
        ).scalar()

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except Exception as e:
            return {'message': 'Something went wrong: {}'.format(e)}

    @classmethod
    def delete_by_id(cls, user_role_id: uuid.UUID):
        role = cls.query.filter_by(id=user_role_id).first()
        if role:
            db.session.delete(role)
            db.session.commit()
        else:
            message: dict = {"message": messages.OBJECT_NOT_FOUND, "errors": []}
            abort(http_status_code=http.HTTPStatus.NOT_FOUND, message=message)
