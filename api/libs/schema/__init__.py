'''
    数据dump或者load的第三方库（很好用）
'''

from api.libs.schema.chain_good import GoodsEliminateQuerySchema, GoodsNewQuerySchema
from api.libs.schema.replace_good import ReplaceGoodsSchema

goods_eliminate_query_schema = GoodsEliminateQuerySchema()
goods_new_query_schema = GoodsNewQuerySchema()
replace_good_schema = ReplaceGoodsSchema()

__all__ = ['goods_eliminate_query_schema', 'goods_new_query_schema',
           'replace_good_schema']
