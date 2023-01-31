import uuid

from database.db import db
from sqlalchemy.dialects.postgresql import UUID


class Captcha(db.Model):
    __tablename__ = 'captcha'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    captcha = db.Column(db.String(length=1000), unique=False, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), unique=True, nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def delete_by_id(cls, user_id: uuid.UUID):
        cap = cls.query.filter_by(user_id=user_id).first()
        db.session.delete(cap)
        db.session.commit()
