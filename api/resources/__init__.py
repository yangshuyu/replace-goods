#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint

from api.libs.api import CustomApi
from api.resources.category import CategoriesResource, StorageAreaResource
from api.resources.chain_good import NewGoodsResource, GoodsEliminateResource
from api.resources.demo import DemoResource
from api.resources.replace_good import ReplaceGoodsResource

'''
    api的url同意注册口
'''

api_bp_v1 = Blueprint('api_v1', __name__)
api_v1 = CustomApi(api_bp_v1, prefix='/v1')

api_v1.add_resource(DemoResource, '/demo')

#类别
api_v1.add_resource(CategoriesResource, '/categories')
api_v1.add_resource(StorageAreaResource, '/storage_area')

#淘汰
api_v1.add_resource(GoodsEliminateResource, '/goods/eliminate')
api_v1.add_resource(ReplaceGoodsResource, '/replace_goods')

#选新
api_v1.add_resource(NewGoodsResource, '/new_goods')

BLUEPRINTS = [
    api_bp_v1
]

__all__ = ['BLUEPRINTS']
