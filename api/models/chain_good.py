from sqlalchemy import or_

from api.extensions import db
from api.libs.constants import NORMAL_STATUS, LOWEST_LEVEL
from api.models.base import BaseModel
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

from db_utils import get_df, REDSHIFT_DB_URL


class ChainGoods(BaseModel):
    __tablename__ = 'chain_goods'

    cmid = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(100))
    foreign_item_id = db.Column(db.String(100), nullable=False)
    item_name = db.Column(db.String(512))
    lastin_price = db.Column(DOUBLE_PRECISION)
    sale_price = db.Column(DOUBLE_PRECISION)
    item_unit = db.Column(db.String(20))
    item_status = db.Column(db.String(50))
    foreign_category_lv1 = db.Column(db.String(50))
    foreign_category_lv2 = db.Column(db.String(50))
    foreign_category_lv3 = db.Column(db.String(50))
    foreign_category_lv4 = db.Column(db.String(512))
    foreign_category_lv5 = db.Column(db.String(512))
    storage_time = db.Column(db.DateTime)
    last_updated = db.Column(db.DateTime)
    isvalid = db.Column(db.String(10))
    warranty = db.Column(db.String(50))
    show_code = db.Column(db.String(50))
    allot_method = db.Column(db.String(255))
    supplier_name = db.Column(db.String(255))
    supplier_code = db.Column(db.String(100))
    brand_name = db.Column(db.String(100))

    @classmethod
    def get_normal_goods_by_query(cls, **kwargs):
        cmid = kwargs.get('cmid', 34)
        chain_category = kwargs.get('chain_category', None)
        barcodes = kwargs.get('barcodes', [])
        is_barcode = kwargs.get('is_barcode', None)
        condition1 = " and cg.{} = '{}'".format(LOWEST_LEVEL.get(cmid), chain_category) if chain_category else ''
        condition2 = ' and cg.barcode in ({})'.format("'{}'".format("','".join(barcodes))) if is_barcode else ''
        sql = '''
                select 
                    cg.cmid,
                    cg.foreign_item_id, 
                    cg.foreign_category_lv3,
                    cg.foreign_category_lv4,
                    cg.item_status, 
                    cg.show_code,
                    cg.item_name, 
                    cg.barcode,
                    cg.brand_name,
                    cg.supplier_name,
                    cg.sale_price 
                from chain_goods cg 
                left join 
                    data_warehouse_{}yyyyyyyyyyyyy dw 
                on dw.foreign_item_id = cg.foreign_item_id 
                where 
                    cg.cmid = {} 
                    and dw.warehouse_name != '' 
                    and cg.item_status = '{}'
                    {}
                    {} 
                group by
                    cg.cmid, 
                    cg.foreign_item_id, 
                    cg.foreign_category_lv3,
                    cg.foreign_category_lv4,
                    cg.item_status, 
                    cg.show_code,
                    cg.item_name, 
                    cg.barcode,
                    cg.brand_name,
                    cg.supplier_name,
                    cg.sale_price;'''.\
            format(cmid, cmid, NORMAL_STATUS.get(cmid), condition1, condition2)
        res = get_df(REDSHIFT_DB_URL, sql)
        return res
