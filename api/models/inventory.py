import arrow

from api.extensions import db
from api.models.base import BaseModel
from sqlalchemy.dialects.postgresql import REAL

from db_utils import get_df, REDSHIFT_DB_URL


class Inventory(BaseModel):
    __tablename__ = 'inventory'

    cmid = db.Column(db.Integer)
    foreign_store_id = db.Column(db.String(20))
    foreign_item_id = db.Column(db.String(20))
    date = db.Column(db.DateTime)
    quantity = db.Column(REAL)
    amount = db.Column(REAL)

    @classmethod
    def get_inventories_by_query(cls, **kwargs):
        cmid = kwargs.get('cmid', 34)
        start_at = kwargs.get('start_at', arrow.now().shift(months=-2).ceil('month').date())
        end_at = kwargs.get('end_at', arrow.now().shift(months=-1).ceil('month').date())
        sql = '''
                select 
                    foreign_item_id, 
                    count(distinct foreign_store_id) as has_inventory_count
                from inventory_{}yyyyyyyyyyyyy 
                where 
                    quantity > 0 
                    and date  > '{}' 
                    and date  < '{}'
                group by foreign_item_id;'''.format(cmid, start_at, end_at)
        res = get_df(REDSHIFT_DB_URL, sql)
        return res
