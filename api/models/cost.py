import arrow

from api.extensions import db
from api.libs.constants import LOWEST_LEVEL
from api.models.base import BaseModel
from sqlalchemy.dialects.postgresql import REAL

from db_utils import get_df, REDSHIFT_DB_URL


class Cost(BaseModel):
    __tablename__ = 'cost'

    cmid = db.Column(db.Integer)
    source_id = db.Column(db.String(16))
    foreign_store_id = db.Column(db.String(255))
    foreign_item_id = db.Column(db.String(255))
    date = db.Column(db.DateTime)
    cost_type = db.Column(db.String(255))
    total_quantity = db.Column(REAL, nullable=False)
    total_sale = db.Column(REAL, nullable=False)
    total_cost = db.Column(REAL, nullable=False)
    foreign_category_lv1 = db.Column(db.String(20), nullable=False)
    foreign_category_lv2 = db.Column(db.String(20), nullable=False)
    foreign_category_lv3 = db.Column(db.String(20), nullable=False)
    foreign_category_lv4 = db.Column(db.String(20), nullable=False)
    foreign_category_lv5 = db.Column(db.String(20), nullable=False)

    @classmethod
    def get_category_cost_by_query(cls, **kwargs):
        cmid = kwargs.get('cmid', 34)
        start_at = kwargs.get('start_at', arrow.now().shift(months=-2).ceil('month').date())
        end_at = kwargs.get('end_at', arrow.now().shift(months=-1).ceil('month').date())
        sql = '''
                select 
                    c.{}, 
                    sum(c.total_quantity) as total_quantity,
                    sum(c.total_sale) as total_sale,
                    sum(c.total_cost) as total_cost,
                    sum(c.total_sale - c.total_cost) as total_profit
                from cost_{}yyyyyyyyyyyyy c 
                left join 
                    chain_goods cg 
                on 
                    cg.foreign_item_id = c.foreign_item_id 
                where 
                    c.date  > '{}' 
                    and c.date  < '{}' 
                    and cg.cmid = {} 
                group by c.{};'''.format(LOWEST_LEVEL.get(cmid), cmid, start_at, end_at, cmid, LOWEST_LEVEL.get(cmid))

        res = get_df(REDSHIFT_DB_URL, sql)
        return res

    @classmethod
    def get_item_cost_by_query(cls, **kwargs):
        cmid = kwargs.get('cmid', 34)
        barcodes = kwargs.get('barcodes', [])
        is_barcode = kwargs.get('is_barcode', None)
        start_at = kwargs.get('start_at', arrow.now().shift(months=-2).ceil('month').date())
        end_at = kwargs.get('end_at', arrow.now().shift(months=-1).ceil('month').date())
        condition = 'and cg.barcode in ({})'.format("'{}'".format("','".join(barcodes))) if is_barcode else ''
        sql = '''
                select 
                    c.foreign_item_id,
                    sum(c.total_quantity) as quantity,
                    sum(c.total_sale) as sale,
                    sum(c.total_cost) as cost,
                    sum(c.total_sale - c.total_cost) as profit
                from 
                    cost_{}yyyyyyyyyyyyy c 
                left join chain_goods cg 
                on 
                    c.foreign_item_id = cg.foreign_item_id
                where 
                    c.date  > '{}' 
                    and c.date  < '{}' 
                    and cg.cmid = {}
                    {} 
                group by c.foreign_item_id;'''.\
            format(cmid, start_at, end_at, cmid, condition)

        res = get_df(REDSHIFT_DB_URL, sql)
        return res

    @classmethod
    def get_sale_store_count_by_query(cls, **kwargs):
        cmid = kwargs.get('cmid', 34)
        start_at = kwargs.get('start_at', arrow.now().shift(months=-2).ceil('month').date())
        end_at = kwargs.get('end_at', arrow.now().shift(months=-1).ceil('month').date())
        sql = '''
                select 
                    foreign_item_id, 
                    count(distinct foreign_store_id) as has_sell_count
                from cost_{}yyyyyyyyyyyyy 
                where 
                    date  > '{}' 
                    and date  < '{}'
                group by foreign_item_id;'''.format(cmid, start_at, end_at)

        res = get_df(REDSHIFT_DB_URL, sql)
        return res

