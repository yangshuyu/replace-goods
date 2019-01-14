import pandas as pd
from flask_restful import Resource
from webargs.flaskparser import use_args

from api.libs.schema import replace_good_schema
from api.models.replace_good import ReplaceGood


class ReplaceGoodsResource(Resource):
    @use_args(replace_good_schema)
    def post(self, args):
        ReplaceGood.add(**args)
        return {'foreign_item_id': args.get('foreign_item_id')}, 201
