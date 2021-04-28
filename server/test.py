#! /usr/bin python3
# -*- encode: utf-8 -*-

import asyncio
import copy
import importlib
import multiprocessing
import os
import sys
import time
import inspect
import aiohttp
from bson import CodecOptions
from motor.motor_asyncio import AsyncIOMotorClient
import main
import settings


_mongodb_addr = settings.MONGODB_ADDR + '_default'
_http_port = str(settings.HTTP_PORT + 1)
_db_name = _mongodb_addr.split('/')[-1]
os.environ['MONGODB_ADDR'] = _mongodb_addr
os.environ['HTTP_PORT'] = _http_port
_host = f'http://127.0.0.1:{_http_port}'
_db_client = AsyncIOMotorClient(_mongodb_addr)  # mongo数据操作对本次单元测试所有测试方法全局生效

_modules = [
    'account',
    'message',
]


def pprint(s, color='none', background=False, output=True):
    clr_lst = ['white', 'red', 'light_yellow', 'yellow', 'blue', 'purple', 'cyan', 'grey', 'light_grey']
    if color in clr_lst:
        index = str(clr_lst.index(color))
        num = '4' + index if background else '3' + index
        s = f'\033[1;{num}m{s}\033[0m'
    if output:
        print(s)
    return s


class Request:
    g = {}
    db = _db_client.get_database(codec_options=CodecOptions(tz_aware=True))
    user = {}

    def __init__(self, username='abc', password='123'):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
            'accept-language': 'en-US,zh;q=0.9,en;q=0.8',
        }
        self.cookies = {}
        Request.user = {'username': username, 'password': password}

    async def get(self, api, **kw):
        headers = copy.deepcopy(self.headers)
        cookies = copy.deepcopy(self.cookies)

        for k, v in kw.get('headers', {}).items():
            headers[k] = v

        if 'login' in kw and kw['login'] is False:
            cookies = {}

        async with aiohttp.ClientSession(headers=headers, cookies=cookies, timeout=aiohttp.ClientTimeout(total=0.5)) as session:
            async with session.get(_host+api) as resp:
                try:
                    json_data = await resp.json()
                    json_data['headers'] = resp.headers
                    json_data['cookies'] = resp.cookies
                    return json_data
                except:
                    pprint('错误，无法解析响应数据')
                    pprint(resp.status)
                    text = await resp.text()
                    pprint(text)
                    sys.exit(-1)

    async def post(self, api, data={}, **kw):
        headers = copy.deepcopy(self.headers)
        cookies = copy.deepcopy(self.cookies)

        for k, v in kw.get('headers', {}).items():
            headers[k] = v
        if 'login' in kw and kw['login'] is False:
            cookies = {}

        async with aiohttp.ClientSession(headers=headers, cookies=cookies, timeout=aiohttp.ClientTimeout(total=0.5)) as session:
            async with session.post(_host+api, json=data) as resp:
                try:
                    json_data = await resp.json()
                    json_data['headers'] = resp.headers
                    json_data['cookies'] = resp.cookies
                    return json_data
                except:
                    pprint('错误，无法解析响应数据')
                    pprint(resp.status)
                    text = await resp.text()
                    pprint(text)
                    sys.exit(-1)

    async def create_user(self):
        await self.post('/api/register', data=Request.user)
        r = await self.post('/api/login', data=Request.user)
        self.cookies = r['cookies']
        Request.user['uid'] = str(self.cookies.get('uid')).split()[1].split('=')[-1][:-1]
        Request.user['sid'] = str(self.cookies.get('sid')).split()[1].split('=')[-1][:-1]
        return r['cookies']

    def success(self, resp):
        try:
            if resp['err']:
                return pprint(resp['msg'], output=False)
        except Exception as e:
            return pprint(repr(e), color='red', output=False)

    def error(self, resp):
        try:
            if not resp['err']:
                return pprint('expected fail but it succeed!\n', output=False)
        except Exception as e:
            return pprint(repr(e), color='red', output=False)


async def run_test(r, test_module=None, test_func=None):
    await r.create_user()
    start = time.time()
    success_count, fail_count = 0, 0

    if test_module and test_module not in _modules:
        raise Exception(f'module not found: {test_module}')

    for item in ([test_module] if test_module else _modules):
        pprint(f'\n{item}', color='blue')
        try:
            load_module = importlib.import_module(item + ".test")
        except ModuleNotFoundError:
            continue
        funcs = inspect.getmembers(load_module, lambda x: inspect.isfunction(x) and x.__name__.startswith('test_'))
        funcs.sort(key=lambda x: inspect.getsourcelines(x[-1])[-1])
        if test_func:
            funcs = list(filter(lambda x: x[0] == test_func, funcs))
            if not funcs:
                raise Exception(f'method not found: {test_func}')
        for name, func in funcs:
            pprint(f'[{name}]', color='light_yellow')
            try:
                error = await func(r)
                if error:
                    fail_count += 1
                    pprint(error)
                else:
                    success_count += 1
            except Exception as e:
                fail_count += 1
                raise e

    end = time.time()
    pprint(f'\nRan {success_count+fail_count} tests in {round(end-start, 2)}s')
    if fail_count > 0:
        pprint(f'failures is {fail_count}')
    else:
        pprint('OK')


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=main.main)
    p1.start()
    pprint(f'create test database {_db_name}')
    time.sleep(0.5)

    try:
        test_module, test_func = None, None
        if len(sys.argv) == 2:
            lst = sys.argv[1].split('.')
            if len(lst) > 0:
                test_module = lst[0]
            if len(lst) > 1:
                test_func = lst[1]
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run_test(Request(), test_module=test_module, test_func=test_func))
        # loop.close()
    finally:
        p1.terminate()
        _db_client.drop_database(_db_name)
        pprint(f'Destroying test database {_db_name}\n')
