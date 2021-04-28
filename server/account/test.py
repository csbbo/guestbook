
async def test_get_user(r):
    resp = await r.get('/api/user')
    return r.success(resp)
