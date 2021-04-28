import bson


# validate method return error str or None, if the key does not exist, the key is not validated
def validate(dic, data):
    for key, funcs in dic.items():
        for f in funcs:
            err = f(key, data)
            if err:
                return err


def required(key, data):
    if key not in data:
        return f'{key} is required'


def not_empty(key, data):
    if key not in data:
        return ''
    if bool(data[key]) is False:
        return f'{key} can not be empty'


def objectid(key, data):
    if key not in data:
        return ''
    try:
        bson.ObjectId(data.get(key))
    except bson.errors.InvalidId:
        return f'{key} is not invalid ObjectId'


def is_json(key, data):
    if key not in data:
        return ''
    if not isinstance(data[key], dict):
        return f'{key} is not json'
