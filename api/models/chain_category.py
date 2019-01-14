from api.extensions import db
from api.models.base import BaseModel
from db_utils import get_df, REDSHIFT_DB_URL


class ChainCategory(BaseModel):
    __tablename__ = 'chain_category'


    cmid = db.Column(db.Integer, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    foreign_category_lv1 = db.Column(db.String(20))
    foreign_category_lv2 = db.Column(db.String(20))
    foreign_category_lv3 = db.Column(db.String(20))
    foreign_category_lv4 = db.Column(db.String(20))
    foreign_category_lv5 = db.Column(db.String(20))
    foreign_category_lv1_name = db.Column(db.String(100))
    foreign_category_lv2_name = db.Column(db.String(100))
    foreign_category_lv3_name = db.Column(db.String(100))
    foreign_category_lv4_name = db.Column(db.String(100))
    foreign_category_lv5_name = db.Column(db.String(512))
    last_updated = db.Column(db.DateTime)

    @classmethod
    def get_categories_by_query(cls, **kwargs):
        cmid = kwargs.get('cmid', 34)
        sql = '''
                select 
                    foreign_category_lv1,
                    foreign_category_lv1_name,
                    foreign_category_lv2,
                    foreign_category_lv2_name,
                    foreign_category_lv3,
                    foreign_category_lv3_name,
                    foreign_category_lv4,
                    foreign_category_lv4_name  
                from chain_category 
                where cmid={};'''.format(cmid)

        res = get_df(REDSHIFT_DB_URL, sql)
        return res
