from marshmallow import fields

from api.libs.schema.base import BaseSchema, Timestamp, BaseQuerySchema


class GoodsEliminateQuerySchema(BaseSchema):
    cmid = fields.Int(missing=34)
    start_at = Timestamp()
    end_at = Timestamp()
    elimination_rule = fields.Int()
    strategy = fields.Int()
    chain_category = fields.Str(required=True)
    storage_area = fields.Str()
    eliminate_amount = fields.Int(missing=1)

    class Meta:
        strict = True


class GoodsNewQuerySchema(BaseQuerySchema):
    cmid = fields.Int(missing=34)
    start_at = Timestamp()
    end_at = Timestamp()
    new_rule = fields.Int()
    strategy = fields.Int()
    chain_category = fields.Str()
    new_amount = fields.Int(missing=1)
    start_price = fields.Float()
    end_price = fields.Float()
    start_interest = fields.Float()
    end_interest = fields.Float()
    category = fields.Str()

    class Meta:
        strict = True

