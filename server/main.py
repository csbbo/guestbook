#! /usr/bin python3
# -*- encode: utf-8 -*-

import asyncio
import sys
import logging
from functools import partial

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient
from bson.codec_options import CodecOptions

import settings
from settings import middleware_i18n

logger = logging.getLogger(__name__)


async def setup_app(app):
    await settings.setup_collections(app)

    import account
    await account.setup(app)

    import message
    await message.setup(app)


def create_app(loop):
    db_client = AsyncIOMotorClient(settings.MONGODB_ADDR, serverSelectionTimeoutMS=3000)
    db = db_client.get_database(codec_options=CodecOptions(tz_aware=True))

    app = web.Application(middlewares=[middleware_i18n], client_max_size=(1024 ** 2) * 10)
    app['db'] = db

    loop.run_until_complete(setup_app(app))
    return app


def main():
    loop = asyncio.get_event_loop()
    logger.error(f'listening http server at {settings.HTTP_LISTEN}:{settings.HTTP_PORT}')
    web.run_app(create_app(loop), host=settings.HTTP_LISTEN, port=settings.HTTP_PORT,
                print=partial(logger.info, color='white', attrs=['bold']), shutdown_timeout=2)
    loop.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
