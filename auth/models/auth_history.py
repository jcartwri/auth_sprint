import datetime
import uuid

from database.db import db
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID


def create_partition(target, connection, **kw) -> None:
    """ creating partition by user_sign_in """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_tablet" PARTITION OF "history" FOR VALUES IN ('tablet')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_mobile" PARTITION OF "history" FOR VALUES IN ('mobile')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_web" PARTITION OF "history" FOR VALUES IN ('web')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_bot" PARTITION OF "history" FOR VALUES IN ('bot')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_test" PARTITION OF "history" FOR VALUES IN ('test')"""
    )


class AuthHistory(db.Model):
    __tablename__ = 'history'
    __table_args__ = (db.UniqueConstraint('id', 'user_device_type'),
                      {'postgresql_partition_by': 'LIST (user_device_type)',
                       'listeners': [('after_create', create_partition)]})

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.id', ondelete="CASCADE"))

    user_agent = db.Column(db.Text)
    user_device_type = db.Column(db.Text, primary_key=True)
    auth_date = db.Column(DateTime, default=datetime.datetime.utcnow)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_user_id(cls, id_):
        return cls.query.filter_by(user_id=id_).first()

    @classmethod
    def return_all(cls, id_, page_number=1):
        def to_json(x):
            return {
                'user_id': str(x.user_id),
                'user_agent': str(x.user_agent),
                'auth_date': str(x.auth_date)
            }

        return {'history': list(map(lambda x: to_json(x), AuthHistory.query.filter_by(user_id=id_)
                                    .paginate(page=page_number, per_page=10)))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except Exception as e:
            return {'message': 'Something went wrong: {}'.format(e)}

    def __repr__(self):
        return f'<Auth history {self.user_id}>'
