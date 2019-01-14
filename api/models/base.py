import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import BaseQuery
from sqlalchemy import func

from api.extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(UUID, default=lambda: str(uuid.uuid4()), primary_key=True)

    # created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, index=True)
    # updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
    #                        onupdate=datetime.datetime.utcnow, index=True)

    filter_fields = []

    def __repr__(self):
        return '<{} {}>' .format(self.__class__.__name__, self.id)

    @classmethod
    def check_target_valid(cls, target_id, target_type):
        from api import models
        try:
            model = getattr(models, target_type.capitalize())
        except AttributeError:
            return None

        return model.query.get(target_id)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter(cls.id == _id).first()

    @classmethod
    def find_by_ids(cls, ids):
        if not ids:
            return []

        query = cls.query.filter(cls.id.in_(ids))
        query = query.order_by(cls.created_at.desc())
        return query.all()

    @classmethod
    def add(cls, **kwargs):
        self = cls(**kwargs)
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

        return self

    def update(self, **kwargs):
        try:
            for k, v in kwargs.items():
                setattr(self, k, v)

            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
            raise e

        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def check_unique(cls, **kwargs):
        if cls.query.filter_by(**kwargs).first():
            return False

        return True

    @classmethod
    def get_count(cls, q):
        count_q = q.statement.with_only_columns(
            [func.count()]).order_by(None)
        count = q.session.execute(count_q).scalar()
        return count


class QueryWithSoftDelete(BaseQuery):
    def __new__(cls, *args, **kwargs):
        obj = super(QueryWithSoftDelete, cls).__new__(cls)
        with_deleted = kwargs.pop('_with_deleted', False)
        if len(args) > 0:
            super(QueryWithSoftDelete, obj).__init__(*args, **kwargs)
            return obj.filter_by(deleted_at=None) if not with_deleted else obj
        return obj

    def __init__(self, *args, **kwargs):
        pass

    def with_deleted(self):
        return self.__class__(db.class_mapper(self._mapper_zero().class_),
                              session=db.session(), _with_deleted=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super(QueryWithSoftDelete, self).get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_deleted()._get(*args, **kwargs)
        return obj if obj is not None and not obj.deleted_at else None
