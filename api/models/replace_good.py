import arrow

from api.extensions import db
from api.models.base import BaseModel
from db_utils import get_df, SERVERDB_DB_URL


class ReplaceGood(BaseModel):
    __tablename__ = 'replace_goods'

    cmid = db.Column(db.Integer, nullable=False)
    foreign_item_id = db.Column(db.String(100), nullable=False)
    item_status = db.Column(db.String(50))
    date = db.Column(db.DateTime)

    @classmethod
    def add(cls, **kwargs):
        item_status = '淘汰'
        cmid = kwargs.get('cmid')
        foreign_item_id = kwargs.get('foreign_item_id')
        date = arrow.now().datetime
        sql = '''
                insert into 
                    replace_goods (foreign_item_id, cmid, item_status,date) 
                values ('{}', {},'{}','{}')'''.format(foreign_item_id, cmid, item_status, date)
        get_df(SERVERDB_DB_URL, sql)

    @classmethod
    def get_replace_goods_by_query(cls, **kwargs):
        cmid = kwargs.get('cmid', 34)
        start_at = arrow.now().shift(months=-1).ceil('month').date()
        end_at = arrow.now().shift(days=-1).date()
        sql = '''
                select 
                    foreign_item_id 
                from 
                    replace_goods 
                where date > '{}'
                    and date < '{}'
                    and cmid = {}                    
                group by 
                    foreign_item_id;'''.format(start_at, end_at, cmid)
        res = get_df(SERVERDB_DB_URL, sql)
        return res
