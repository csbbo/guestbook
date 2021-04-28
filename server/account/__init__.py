import asyncio
import logging
import pymongo

from utils import filters
from utils.filters import validate
from utils.http import get_sid, set_sid, login_required, success_response, error_response
from utils.shortcuts import hash_pass

logger = logging.getLogger(__name__)


async def handle_register(request):
    data = await request.json()
    err = validate({
        'username': [filters.required, filters.not_empty],
        'password': [filters.required, filters.not_empty]
    }, data)
    if err:
        return error_response(err)

    try:
        insert_result = await request.app['db'].users.insert_one({
            'username': data['username'],
            'password': hash_pass(data['password']),
        })
    except pymongo.errors.DuplicateKeyError:
        return error_response(request['i18n'].user_exists)
    except Exception as e:
        logger.exception(e)
        return error_response(request['i18n'].server_error)

    uid = insert_result.inserted_id
    return success_response({'uid': str(uid)})


async def handle_login(request):
    data = await request.json()
    err = validate({
        'username': [filters.required, filters.not_empty],
        'password': [filters.required]
    }, data)
    if err:
        return error_response(err)

    user = await request.app['db'].users.find_one({'username': data['username']})
    if not user:
        return error_response(request['i18n'].user_not_exists)
    if hash_pass(data['password']) != user.get('password'):
        return error_response(request['i18n'].password_error)

    sid = get_sid(user)
    response = success_response()
    set_sid(str(user['_id']), sid, response)
    return response


@login_required
async def handle_get_user(request):
    await asyncio.sleep(0.001)
    user = request['user']
    return success_response({'username': user['username']})


async def setup(app):
    app.router.add_route('POST', '/api/register', handle_register)
    app.router.add_route('POST', '/api/login', handle_login)
    app.router.add_route('GET', '/api/user', handle_get_user)
