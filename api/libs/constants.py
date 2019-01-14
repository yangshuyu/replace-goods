'''
    常亮类
'''

import enum


class BaseEnum(enum.Enum):
    @classmethod
    def values(cls):
        return [e.value for e in cls]

    @classmethod
    def keys(cls):
        return [e.name for e in cls]


class AuthType(BaseEnum):
    WECHAT = 1
    WEIBO = 2
    QQ = 3


class GenderType(BaseEnum):
    MALE = 1
    FEMALE = 2
    UNKNOWN = 3


class LoginType(BaseEnum):
    PHONE = 1
    AUTH = 2
    BIND = 3


class MessageType(BaseEnum):
    GIFT = 1000 # 礼物消息
    INTERACTION = 2000 # 互动消息
    REMIND = 3000 # 提醒信息
    ANNOUNCEMENT = 4000 # 全员通告


class LikeTargetType(BaseEnum):
    POST = 1
    USER = 2


ELIMINATION_RULE = {
    0: 'average_store_quantity'
}

CHOOSE_NEW_RULE = {
    0: 'best_interest_rate',
    1: 'average_store_quantity',
}

NORMAL_STATUS = {
    34: '正常品',
    43: '正常',
    58: '导入期'
}

LOWEST_LEVEL = {
    34: 'foreign_category_lv4',
    43: 'foreign_category_lv3',
    58: 'foreign_category_lv3'
}
