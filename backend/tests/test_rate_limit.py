def test_login_rate_limit(client):
    for _ in range(5): client.post('/api/auth/login', json={'email':'none@example.com','password':'longpassword1'})
    assert client.post('/api/auth/login', json={'email':'none@example.com','password':'longpassword1'}).status_code==429
