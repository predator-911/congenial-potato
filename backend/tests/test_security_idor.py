from .conftest import csrf, register, upload_pdf


def test_bob_cannot_access_alice_file_by_id(client):
    register(client,'alice@example.com','longpassword1'); alice_file=upload_pdf(client,'secret.pdf').json()['file']; alice_csrf=csrf(client)
    alice_cookie=client.cookies.get('sfs_session')
    client.post('/api/auth/logout', headers={'X-CSRF-Token':alice_csrf})
    register(client,'bob@example.com','longpassword2'); bob_csrf=csrf(client); fid=alice_file['id']
    assert client.get(f'/api/files/{fid}').status_code == 404
    assert client.get(f'/api/files/{fid}/download').status_code == 404
    assert client.patch(f'/api/files/{fid}', json={'original_filename':'pwned.pdf'}, headers={'X-CSRF-Token':bob_csrf}).status_code == 404
    assert client.post(f'/api/files/{fid}/share', json={}, headers={'X-CSRF-Token':bob_csrf}).status_code == 404
    assert client.delete(f'/api/files/{fid}/share', headers={'X-CSRF-Token':bob_csrf}).status_code == 404
    assert client.delete(f'/api/files/{fid}', headers={'X-CSRF-Token':bob_csrf}).status_code == 404
    client.cookies.set('sfs_session', alice_cookie); client.cookies.set('sfs_csrf', alice_csrf)
    assert client.get(f'/api/files/{fid}').json()['file']['original_filename'] == 'secret.pdf'
