from marshmallow import (Schema, fields, post_dump)
import arrow
from flask import current_app


class BaseSchema(Schema):
    @post_dump
    def clear_none(self, data):
        result = {}
        for k, v in data.items():
            if v is None:
                continue
            elif isinstance(v, dict):
                result[k] = self.clear_none(v)
            else:
                result[k] = v
        return result


class BaseQuerySchema(BaseSchema):
    page = fields.Int(missing=1, location='query',
                      validate=lambda val: 1000 > val > 0)
    per_page = fields.Int(missing=10, location='query',
                          validate=lambda val: 200 > val > 0)
    q = fields.Str(location='query')
    original = fields.Int(missing=-1, location='query')
    source = fields.Str(location='query')

    class Meta:
        strict = True


class StatusQuerySchema(BaseQuerySchema):
    status = fields.Int()

    class Meta:
        strict = True


class Uri(fields.String):
    def _serialize(self, value, attr, obj):
        if value is None:
            return

        if value == '':
            return value

        if 'http' in value:
            return value

        return current_app.config['QINIU_URL_PRE'] + value

    def _deserialize(self, value, attr, data):
        if value is None:
            return

        if value == '':
            return value

        if value.startswith(current_app.config['QINIU_URL_PRE']):
            value = value[len(current_app.config['QINIU_URL_PRE']):]

        return value


class WebPUri(Uri):
    def _serialize(self, value, attr, obj):
        if value is None:
            return

        if value == '':
            return value

        if 'http' in value:
            return value + current_app.config['COVER_WEBP_STYLE']

        return current_app.config['QINIU_URL_PRE'] + value + current_app.config['COVER_WEBP_STYLE']

    def _deserialize(self, value, attr, data):
        if value is None:
            return

        if value == '':
            return value

        if value.startswith(current_app.config['QINIU_URL_PRE']):
            value = value[len(current_app.config['QINIU_URL_PRE']):]

        if value.endswith(current_app.config['COVER_WEBP_STYLE']):
            value = value[:0-len(current_app.config['COVER_WEBP_STYLE'])]

        return value


class AvatarUri(Uri):
    def _serialize(self, value, attr, obj):
        if value is None:
            return

        if value == '':
            return value

        if 'http' in value:
            return value + current_app.config['AVATAR_STYLE']

        return current_app.config['QINIU_URL_PRE'] + \
            value + current_app.config['AVATAR_STYLE']

    def _deserialize(self, value, attr, data):
        if value is None:
            return

        if value == '':
            return value

        if value.startswith(current_app.config['QINIU_URL_PRE']):
            value = value[len(current_app.config['QINIU_URL_PRE']):]

        if value.endswith(current_app.config['AVATAR_STYLE']):
            value = value[: 0-len(current_app.config['AVATAR_STYLE'])]

        return value


class QueryList(fields.String):
    def _serialize(self, value, attr, obj):
        return None

    def _deserialize(self, value, attr, data):
        if value is None:
            return
        return value.split(',')


class Timestamp(fields.DateTime):
    def _serialize(self, value, attr, obj):
        if value:
            return arrow.get(value).timestamp

    def _deserialize(self, value, attr, obj):
        return arrow.get(value).datetime

