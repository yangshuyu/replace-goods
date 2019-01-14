import pandas as pd

from flask_restful import Resource
from webargs.flaskparser import use_args
from api.libs.constants import LOWEST_LEVEL
from api.libs.schema import goods_eliminate_query_schema, goods_new_query_schema
from api.models.category_mapping import CategoryMapping
from api.models.chain_category import ChainCategory
from api.models.chain_good import ChainGoods
from api.models.cost import Cost
from api.models.inventory import Inventory
from api.models.item_storage_area import ItemStorageArea
from api.presenter.choose_new_presenter import ChooseNewPresenter
from api.presenter.eliminate_presenter import EliminatePresenter


class GoodsEliminateResource(Resource):
    # @cache.cached(20000)
    @use_args(goods_eliminate_query_schema)
    def get(self, args):
        cmid = args.get('cmid')
        strategy = args.get('strategy')
        storage_area = args.get('storage_area')

        goods_res = ChainGoods.get_normal_goods_by_query(**args)
        category_res = ChainCategory.get_categories_by_query(**args)
        item_cost_res = Cost.get_item_cost_by_query(**args)
        category_cost_res = Cost.get_category_cost_by_query(**args)
        inventory_res = Inventory.get_inventories_by_query(**args)
        sell_store_count_res = Cost.get_sale_store_count_by_query(**args)
        res = pd.merge(goods_res, category_res, how='left', on=['foreign_category_lv3', 'foreign_category_lv4'])
        res = pd.merge(res, item_cost_res, how='left', on='foreign_item_id')
        res = pd.merge(res, category_cost_res, how='left', on=LOWEST_LEVEL.get(cmid))
        res = pd.merge(res, inventory_res, how='left', on=['foreign_item_id'])
        res = pd.merge(res, sell_store_count_res, how='left', on=['foreign_item_id'])
        if strategy == 0 and (storage_area and storage_area != '无'):
            storage_area_res = ItemStorageArea.get_item_by_query(**args)
            res = pd.merge(storage_area_res, res, how='inner', on=['foreign_item_id'])
        data = EliminatePresenter.eliminate_data(res, **args)
        return data


class NewGoodsResource(Resource):
    @use_args(goods_new_query_schema)
    def get(self, args):
        category_mapping_res = CategoryMapping.get_barcode_by_query(**args)
        cmid_barcodes = category_mapping_res.groupby(['cmid'])['barcode'].apply(lambda x: x.tolist()).to_dict()
        data, columns = [], ['cmid', 'foreign_item_id', 'foreign_category_lv3', 'foreign_category_lv4',
                             'item_name', 'show_code', 'barcode', 'quantity', 'sale', 'cost', 'profit',
                             'has_inventory_count', 'has_sell_count', 'sale_price']
        all_res = pd.DataFrame(columns=columns)
        for key, value in cmid_barcodes.items():
            args['is_barcode'], args['cmid'], args['barcodes'] = True, key, value
            goods_res = ChainGoods.get_normal_goods_by_query(**args)
            item_cost_res = Cost.get_item_cost_by_query(**args)
            inventory_res = Inventory.get_inventories_by_query(**args)
            sell_store_count_res = Cost.get_sale_store_count_by_query(**args)
            res = pd.merge(goods_res, item_cost_res, how='left', on='foreign_item_id')
            res = pd.merge(res, inventory_res, how='left', on=['foreign_item_id'])
            res = pd.merge(res, sell_store_count_res, how='left', on=['foreign_item_id'])
            if len(res) > 0:
                data.append(res)
        for d in data:
            d = d.fillna(value=0)
            all_res = pd.merge(all_res, d, how='outer', on=columns)
        data = ChooseNewPresenter.choose_new_data(all_res, **args)
        return data

