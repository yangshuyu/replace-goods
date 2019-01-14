from api.libs.constants import CHOOSE_NEW_RULE
from api.models.replace_good import ReplaceGood


class ChooseNewPresenter():
    @classmethod
    def choose_new_data(cls, res, **kwargs):
        if len(res) == 0:
            return []
        new_amount = kwargs.get('new', 3)
        replace_goods_res = ReplaceGood.get_replace_goods_by_query(**kwargs)
        replace_ids = replace_goods_res['foreign_item_id'].values.tolist()
        res = res.drop(res[res['foreign_item_id'].isin(replace_ids)].index.tolist(), axis=0)
        # res['suggest'] = res.apply(lambda x: '不选新' if x.foreign_item_id in replace_ids else '选新', axis=1)
        #店均销售量
        res['average_store_quantity'] = res['quantity'] / res['has_inventory_count']
        res['average_store_quantity'] = res['average_store_quantity'].fillna(value=1, method=None)
        # 铺货渠道数
        res['channel_amount'] = res.apply(lambda x: len(res[res['barcode'] == x['barcode']]), axis=1)
        # 铺货渠道总门店数
        total_sum = res.groupby(res['barcode']).sum()
        res['channel_store_amount'] = res.apply(lambda x: total_sum.loc[x['barcode'], 'has_inventory_count'], axis=1)
        # 计算最高毛利率
        res['interest_rate'] = res['profit'] / res['sale']
        m = res.groupby(res['barcode']).max()
        res['best_interest_rate'] = res.apply(lambda x: m.loc[x['barcode'], 'interest_rate'], axis=1)
        res['average_store_quantity'] = res['average_store_quantity'].fillna(value=1, method=None)
        res = res.fillna(value=0)

        start_price = kwargs.get('start_price', None)
        end_price = kwargs.get('end_price', None)
        start_interest = kwargs.get('start_interest', None)
        end_interest = kwargs.get('end_interest', None)

        if start_price is not None:
            res = res[res['sale_price'] >= start_price]
        if end_price is not None:
            res = res[res['sale_price'] <= end_price]
        if start_interest is not None:
            res = res[res['interest_rate'] >= start_interest/100]
        if end_interest is not None:
            res = res[res['interest_rate'] <= end_interest/100]

        res = res.sort_values(by=['{}'.format(
            CHOOSE_NEW_RULE.get(kwargs.get('new_rule', 0))), '{}'.format(
            CHOOSE_NEW_RULE.get(1))]
            , ascending=[False, False])
        res['suggest'] = '不选'
        res = res.reset_index(drop=True)
        res = res.round(decimals=2)
        for i in range(new_amount):
            if len(res) > i:
                res.ix[i, 'suggest'] = '选新'
        res = res[['cmid', 'foreign_item_id', 'foreign_category_lv3',
                   'show_code', 'item_name', 'barcode', 'foreign_category_lv4',
                   'sale_price', 'quantity', 'sale', 'cost', 'profit',
                   'has_inventory_count', 'has_sell_count',
                   'channel_amount', 'channel_store_amount', 'interest_rate', 'best_interest_rate',
                   'average_store_quantity', 'suggest']]
        data = res.to_dict(orient='records')
        return data
