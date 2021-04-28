import os

import pymongo
from aiohttp.web import middleware

from utils import i18n

HTTP_LISTEN = os.getenv('HTTP_LISTEN', '0.0.0.0')
HTTP_PORT = int(os.getenv('HTTP_PORT', '7070'))
MONGODB_ADDR = os.getenv('MONGODB_ADDR', 'mongodb://127.0.0.1:27017/guestbook')

HASH_SALT = os.getenv('HASH_SALT', '94af841d6732b7bf1acdf354aa7ebadb53a9bd4f')


@middleware
async def middleware_i18n(request, handler):
    request['i18n'] = i18n.i18n(request.headers.get('accept-language'))
    return await handler(request)


async def setup_collections(app):
    db = app['db']

    # users model
    '''
    {
        '_id': ObjectId,
        'username': str,
        'password': str,
    }
    '''
    await db.users.create_index([("username", pymongo.ASCENDING)], unique=True)

    # messages model
    '''
    {
        '_id': ObjectId,
        'uid': ObjectId,
        'title': str
        'content': str,
        'delete_time': datetime(utc)
        
        'ip': str,
        'user-agent': str,
    }
    '''
    await db.messages.create_index([("content", pymongo.ASCENDING)])

    # comments model
    '''
    {
        '_id': ObjectId,
        'uid': ObjectId,
        'mid': ObjectId,
        'content': str,
        
        'ip': str,
        'user-agent': str,
    }
    '''
    await db.comments.create_index([("content", pymongo.ASCENDING)])

    # files model
    '''
    {
        '_id': ObjectId,
        'filename': str,
        'save_name': str,
    }
    '''