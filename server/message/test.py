import bson


async def test_add_message(r):
    data = {
        'title': 'message title',
        'content': f'add test message content',
        'comment_struct': {'name': 'xiaoming', 'age': 18, 'lessons': ['yuwen', 'shuxue', 'yingyu']}
    }
    resp = await r.post('/api/message/add', data, headers={'accept-language': 'zh-CN'})
    return r.success(resp)


async def test_get_message(r):
    insert_result = await r.db.messages.insert_one({
        'content': 'message for get',
    })
    message_id = str(insert_result.inserted_id)
    resp = await r.get(f'/api/message/get?id={message_id}')
    return r.success(resp)


async def test_query_message(r):
    params = '?content=test message'
    resp = await r.get('/api/message/query'+params)
    return r.success(resp)


async def test_delete_message(r):
    insert_result = await r.db.messages.insert_one({
        'uid': bson.ObjectId(r.user['uid']),
        'content': 'message for delete',
    })

    resp = await r.post('/api/message/delete', {'id': str(insert_result.inserted_id)})
    return r.success(resp)


async def test_add_comment(r):
    insert_result = await r.db.messages.insert_one({
        'content': 'comment a message',
    })

    data = {'mid': str(insert_result.inserted_id), 'content': f'comment a message'}
    resp = await r.post('/api/comment/add', data, login=False)
    return r.success(resp)


async def test_get_comment(r):
    insert_result = await r.db.comments.insert_one({
        'content': 'add comment for get',
    })
    resp = await r.get(f'/api/comment/get?id={str(insert_result.inserted_id)}')
    return r.success(resp)


async def test_query_comment(r):
    message_insert_result = await r.db.messages.insert_one({
        'content': 'comment a message',
    })
    await r.db.comments.insert_one({
        'mid': message_insert_result.inserted_id,
        'content': 'add comment for query1',
    })
    await r.db.comments.insert_one({
        'mid': message_insert_result.inserted_id,
        'content': 'add comment for query2',
    })
    resp = await r.get(f'/api/comment/query?mid={str(message_insert_result.inserted_id)}')
    # print(resp['data'])
    return r.success(resp)
