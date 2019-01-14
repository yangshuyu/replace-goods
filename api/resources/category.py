#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import pandas as pd
from flask import request
from flask_restful import Resource

from api.models.category_mapping import CategoryMapping
from api.models.chain_category import ChainCategory
from api.models.item_storage_area import ItemStorageArea


class CategoriesResource(Resource):
    def get(self):
        cmid = request.args.get('cmid', 34)
        file_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
        df = pd.read_excel('{}/file/{}_{}.xlsx'.format(file_path, 'category', cmid))
        # df = ChainCategory.get_categories_by_query()
        foreign_lv1 = list(set(df['foreign_category_lv1'].values.tolist()))
        type_1 = df.groupby(['foreign_category_lv1'])['foreign_category_lv2'].apply(lambda x: x.tolist()).to_dict()
        type_2 = df.groupby(['foreign_category_lv2'])['foreign_category_lv3'].apply(lambda x: x.tolist()).to_dict()
        type_3 = df.groupby(['foreign_category_lv3'])['foreign_category_lv4'].apply(lambda x: x.tolist()).to_dict()

        data = []
        for lv1 in foreign_lv1:
            a = {'id': lv1, 'name': df[df['foreign_category_lv1'] == lv1].iloc[0].loc['foreign_category_lv1_name'],
                 'foreign_category_lv2s': []}
            for lv2 in list(set(type_1.get(lv1))):
                b = {'id': lv2, 'name': df[df['foreign_category_lv2'] == lv2].iloc[0].loc['foreign_category_lv2_name'],
                     'foreign_category_lv3s': []}
                a['foreign_category_lv2s'].append(b)
                for lv3 in list(set(type_2.get(lv2))):
                    c = {'id': lv3,
                         'name': df[df['foreign_category_lv3'] == lv3].iloc[0].loc['foreign_category_lv3_name'],
                         'foreign_category_lv4s': []}
                    b['foreign_category_lv3s'].append(c)
                    for lv4 in list(set(type_3.get(lv3))):
                        d = {'id': lv4,
                             'name': df[df['foreign_category_lv4'] == lv4].iloc[0].loc['foreign_category_lv4_name']}
                        c['foreign_category_lv4s'].append(d)

            data.append(a)
        return data


class StorageAreaResource(Resource):
    def get(self):
        storage_area_res = ItemStorageArea.get_all_storage_area()
        data = storage_area_res.to_dict(orient='records')
        return data

