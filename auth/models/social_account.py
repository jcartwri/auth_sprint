import uuid

from database.db import db
from models.user import User
from sqlalchemy.dialects.postgresql import UUID


class SocialAccount(db.Model):
    __tablename__ = 'social_account'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    user = db.relationship(User, backref=db.backref('social_accounts', lazy=True),)

    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)
    __table_args__ = (db.UniqueConstraint('social_id', 'social_name', name='social_pk'),)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_row(cls, social_id, social_name):
        return cls.query.filter_by(social_name=social_name, social_id=social_id).first()

    def __repr__(self):
        return f'<SocialAccount {self.social_name}:{self.user_id}>'
