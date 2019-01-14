from marshmallow import ValidationError, validate


def validate_elimination_rule(p):
    if p == '店均销售量':
        return 0
    elif p == '毛利率':
        return 1
    return 0


def validate_strategy(p):
    if p == '类别内销售最差':
        return 0
    elif p == '小类中销售最差':
        return 1
    return 0