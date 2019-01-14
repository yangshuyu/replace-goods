import os
import pandas as pd

from api.libs.constants import LOWEST_LEVEL
from api.models.base import BaseModel
from api.extensions import db
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION

from db_utils import get_df, REDSHIFT_DB_URL


class CategoryMapping(BaseModel):
    __tablename__ = 'category_mapping'

    cmid = db.Column(db.Integer, nullable=False)
    barcode = db.Column(db.String(100))
    category = db.Column(db.String(100))
    prob = db.Column(DOUBLE_PRECISION)

    @classmethod
    def get_barcode_by_query(cls, **kwargs):
        cmid = kwargs.get('cmid', 34)
        category = kwargs.get('category')
        condition = " and {} = '{}'".format(LOWEST_LEVEL.get(cmid), category) if category else ''
        sql = '''
                select 
                    barcode 
                from 
                    chain_goods 
                where 
                    cmid = {} 
                    {} limit 1;'''.format(cmid, condition)
        barcode_res = get_df(REDSHIFT_DB_URL, sql)
        barcode = barcode_res.iloc[0].loc['barcode']

        file_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        df = pd.read_excel('{}/file/{}.xlsx'.format(file_path, 'temp_category_search'))
        category_lv3_name = df[df['barcode'] == int(barcode)]['category_lv3_name'].values.tolist()
        if category_lv3_name:
            barcodes = df[df['category_lv3_name'] == category_lv3_name[0]]['barcode'].values.tolist()
            barcodes = [str(b) for b in barcodes]
        else:
            barcodes = []
        condition = ' and barcode in ({})'.format("'{}'".format("','".join(barcodes)))
        sql = '''
                select 
                    cmid, 
                    barcode 
                from chain_goods 
                where cmid 
                    in ({}, {}) {} 
                    and barcode not in (
                        select 
                            barcode 
                        from chain_goods where cmid = {} {});'''.format(43, 58, condition, cmid, condition)
        res = get_df(REDSHIFT_DB_URL, sql)
        return res

