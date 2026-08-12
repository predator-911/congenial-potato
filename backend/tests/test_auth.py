from .conftest import csrf, login, register


def test_register_login_logout_me(client):
    r=register(client); assert r.status_code==201; assert client.get('/api/auth/me').status_code==200
    assert csrf(client)
    assert client.post('/api/auth/logout', headers={'X-CSRF-Token':csrf(client)}).status_code==204
    assert client.get('/api/auth/me').status_code==401

def test_duplicate_and_wrong_password(client):
    assert register(client).status_code==201
    assert register(client).status_code==409
    assert login(client,password='wrongpassword').status_code==401
