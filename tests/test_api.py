def test_api(client):
    res = client.get('/api/hello_world')
    assert res.status_code == 200
    assert res.data == b'hello world!'
