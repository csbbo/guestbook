import hashlib
import functools
import json

import bson
from aiohttp import web

import settings


class Encoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bson.objectid.ObjectId):
            return str(o)
        return json.JSONEncoder.default(o)


def jsondumps(d, **kwargs):
    kwargs['cls'] = Encoder
    return json.dumps(d, **kwargs)


def success_response(data=None, err=None):
    return web.json_response({'err': err, 'data': data}, content_type='application/json', dumps=jsondumps)


def error_response(msg=None, err='err'):
    return web.json_response({'err': err, 'msg': msg}, content_type='application/json')


def get_sid(user):
    text = user['username']
    text += settings.HASH_SALT[::2]
    text += user['password']
    text += settings.HASH_SALT[::5]
    text += str(user['_id'])
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[::2]


def set_sid(uid, sid, response):
    response.set_cookie('uid', uid, max_age=86400 * 2)
    response.set_cookie('sid', sid, max_age=86400 * 2)


async def get_login_user(request) -> dict:
    uid = request.cookies.get('uid')
    sid = request.cookies.get('sid')
    if uid and sid:
        try:
            uid = bson.ObjectId(uid)
            user = await request.app['db'].users.find_one({'_id': uid})
            if user and sid == get_sid(user):
                return user
        except bson.errors.InvalidId:
            pass
    return {}


async def validate_user(request):
    user = await get_login_user(request)
    if not user:
        return error_response(request['i18n'].login_required)
    return user


def login_required(func):
    @functools.wraps(func)
    async def wrapper(request, *args, **kw):
        ret = await validate_user(request)
        if isinstance(ret, dict):
            request['user'] = ret
            return await func(request, *args, **kw)
        else:
            return ret
    return wrapper

