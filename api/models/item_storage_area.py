import arrow

from api.extensions import db
from api.libs.constants import LOWEST_LEVEL
from api.models.base import BaseModel
from sqlalchemy.dialects.postgresql import REAL

from db_utils import get_df, REDSHIFT_DB_URL


class ItemStorageArea(BaseModel):
    __tablename__ = 'item_storage_area'

    cmid = db.Column(db.Integer)
    foreign_item_id = db.Column(db.String(30))
    item_name = db.Column(db.String(255))
    storage_area = db.Column(db.String(100))

    @classmethod
    def get_all_storage_area(cls):
        sql = '''
                select 
                    storage_area 
                from 
                    item_storage_area 
                group by storage_area;'''

        res = get_df(REDSHIFT_DB_URL, sql)
        return res

    @classmethod
    def get_item_by_query(cls, **kwargs):
        storage_area = kwargs.get('storage_area')
        sql = '''
                select 
                    foreign_item_id, 
                    storage_area 
                from 
                    item_storage_area 
                where 
                    storage_area = '{}';'''.format(storage_area)

        res = get_df(REDSHIFT_DB_URL, sql)
        return res