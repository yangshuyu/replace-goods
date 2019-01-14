from marshmallow import fields

from api.libs.schema.base import BaseSchema, Timestamp
from api.libs.schema.validator import validate_elimination_rule, validate_strategy


class ReplaceGoodsSchema(BaseSchema):
    cmid = fields.Int(missing=34)
    foreign_item_id = fields.Str()
    item_status = fields.Str()
    date = Timestamp(dump_only=True)

    class Meta:
        strict = True
