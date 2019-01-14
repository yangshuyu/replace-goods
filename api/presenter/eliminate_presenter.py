import pandas as pd

from api.libs.constants import ELIMINATION_RULE, LOWEST_LEVEL
from api.models.replace_good import ReplaceGood


class EliminatePresenter():
    @classmethod
    def eliminate_data(cls, res, **kwargs):
        cmid = kwargs.get('cmid')
        eliminate_amount = kwargs.get('eliminate_amount', 3)
        replace_goods_res = ReplaceGood.get_replace_goods_by_query(**kwargs)
        replace_ids = replace_goods_res['foreign_item_id'].values.tolist()
        res = res.drop(res[res['foreign_item_id'].isin(replace_ids)].index.tolist(), axis=0)

        res['has_sell_count'] = res['has_sell_count'].fillna(value=0, method=None)
        res['has_inventory_count'] = res['has_inventory_count'].fillna(value=0, method=None)
        res['quantity'] = res['quantity'].fillna(value=0, method=None)

        # 店均销售
        res['average_store_quantity'] = res['quantity'] / res['has_inventory_count']
        res['average_store_quantity'] = res['average_store_quantity'].fillna(value=1, method=None)
        res['store_quantity_rank'] = res['average_store_quantity'].groupby(res[LOWEST_LEVEL.get(cmid)]).rank()
        # 销量
        res['quantity_rank'] = res['quantity'].groupby(res[LOWEST_LEVEL.get(cmid)]).rank()
        # 销售额
        res['sale_rank'] = res['sale'].groupby(res[LOWEST_LEVEL.get(cmid)]).rank()
        # 毛利额
        res['profit_rank'] = res['profit'].groupby(res[LOWEST_LEVEL.get(cmid)]).rank()
        # 毛利率
        res['interest_rate'] = res['profit'] / res['sale']
        # 上架率
        res['self_rate'] = res['has_inventory_count'] / 375 * 100
        # 动销率
        res['marketing_rate'] = res['has_sell_count'] / res['has_inventory_count'] * 100
        res = res.sort_values(by='{}'.format(
            ELIMINATION_RULE.get(kwargs.get('elimination_rule', 0))), ascending=True)
        res = res.fillna(value=0)
        res['suggest'] = '保留'
        res = res.reset_index(drop=True)
        for i in range(eliminate_amount):
            if len(res) > i:
                res.ix[i, 'suggest'] = '淘汰'
        res = res[['cmid', 'foreign_item_id', 'foreign_category_lv3', 'foreign_category_lv4', 'foreign_category_lv3_name', 'foreign_category_lv4_name',
                   'item_status', 'show_code', 'item_name', 'barcode', 'brand_name', 'supplier_name',
                   'sale_price', 'quantity', 'sale', 'cost', 'profit', 'total_quantity', 'total_sale',
                   'total_cost', 'total_profit', 'has_inventory_count', 'has_sell_count', 'average_store_quantity',
                   'store_quantity_rank', 'quantity_rank', 'sale_rank', 'profit_rank', 'interest_rate',
                   'self_rate', 'marketing_rate', 'suggest']]
        res = res.round(decimals=2)
        result = res.to_dict(orient='records')
        return result
