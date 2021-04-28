import logging
import bson
import pymongo

from utils import filters
from utils.filters import validate
from utils.http import login_required, success_response, error_response, get_login_user
from utils.shortcuts import utcnow

logger = logging.getLogger(__name__)


@login_required
async def handle_add_message(request):
    data = await request.json()
    err = validate({
        'title': [filters.required, filters.not_empty],
        'content': [filters.not_empty],
    }, data)
    if err:
        return error_response(err)

    try:
        insert_result = await request.app['db'].messages.insert_one({
            'uid': request['user']['_id'],
            'title': data['title'],
            'content': data['content'],
            'ip': request.remote,
            'user-agent': request.headers.get('user-agent'),
        })
    except pymongo.errors.DuplicateKeyError:
        return error_response(request['i18n'].message_not_exists)
    except Exception as e:
        logger.exception(e)
        return error_response(request['i18n'].server_error)

    return success_response({'id': str(insert_result.inserted_id)})


async def handle_get_message(request):
    try:
        message_id = bson.ObjectId(request.rel_url.query.get('id'))
    except bson.errors.InvalidId:
        return error_response(request['i18n'].message_not_exists)

    message = await request.app['db'].messages.find_one({'_id': message_id})
    if not message:
        return error_response(request['i18n'].message_not_exists)
    return success_response({'message': message})


async def handle_query_message(request):
    flt = {'delete_time': None}
    if content := request.rel_url.query.get('content'):
        flt['content'] = {'$regex': content}

    messages_list = []
    async for m in request.app['db'].messages.find(flt):
        messages_list.append({
            'id': str(m['_id']),
            'content': m['content']
        })
    return success_response({'messages': messages_list})


@login_required
async def handle_delete_message(request):
    data = await request.json()
    err = validate({
        'id': [filters.required, filters.objectid]
    }, data)
    if err:
        return error_response(err)

    update_result = await request.app['db'].messages.update_one(
        {
            '_id': bson.ObjectId(data['id']),
            'uid': request['user']['_id']
        },
        {
            '$set': {
                'delete_time': utcnow()
            }
        }
    )
    if not update_result.modified_count:
        return error_response(request['i18n'].message_not_exists)
    return success_response()


async def handle_add_comment(request):
    data = await request.json()
    err = validate({
        'mid': [filters.required, filters.objectid],
        'content': [filters.required, filters.not_empty]
    }, data)
    if err:
        return error_response(err)

    message = await request.app['db'].messages.find_one({'_id': bson.ObjectId(data['mid'])})
    if not message:
        return error_response(request['i18n'].message_not_exists)

    user = await get_login_user(request)
    data['uid'] = user['_id'] if user else None

    try:
        insert_result = await request.app['db'].comments.insert_one({
            'uid': data['uid'],
            'mid': message['_id'],
            'content': data['content'],
            'ip': request.remote,
            'user-agent': request.headers.get('user-agent'),
        })
    except Exception as e:
        logger.exception(e)
        return error_response(request['i18n'].server_error)

    return success_response({'id': str(insert_result.inserted_id)})


async def handle_get_comment(request):
    try:
        comment_id = bson.ObjectId(request.rel_url.query.get('id'))
    except bson.errors.InvalidId:
        return error_response(request['i18n'].comment_not_exists)

    comment = await request.app['db'].comments.find_one({'_id': comment_id})
    if not comment:
        return error_response(request['i18n'].comment_not_exists)
    return success_response({'comment': comment})


async def handle_query_comment(request):
    err = validate({
        'mid': [filters.objectid],
        'content': [filters.not_empty]
    }, request.rel_url.query)

    flt = {'delete_time': None}
    if err:
        return error_response(err)

    if mid := request.rel_url.query.get('mid'):
        flt.update({'mid': bson.ObjectId(mid)})

    if content := request.rel_url.query.get('content'):
        flt['content'] = {'$regex': content}

    comment_list = []
    async for m in request.app['db'].comments.find(flt):
        comment_list.append({
            'id': str(m['_id']),
            'content': m['content']
        })
    return success_response({'comments': comment_list})


async def setup(app):
    app.router.add_route('POST', '/api/message/add', handle_add_message)
    app.router.add_route('GET', '/api/message/get', handle_get_message)
    app.router.add_route('GET', '/api/message/query', handle_query_message)
    app.router.add_route('POST', '/api/message/delete', handle_delete_message)
    app.router.add_route('POST', '/api/comment/add', handle_add_comment)
    app.router.add_route('GET', '/api/comment/get', handle_get_comment)
    app.router.add_route('GET', '/api/comment/query', handle_query_comment)
