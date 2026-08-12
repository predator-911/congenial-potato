from .conftest import csrf, register, upload_pdf


def test_public_share_and_revoke(client):
    register(client); fid=upload_pdf(client).json()['file']['id']
    assert client.post(f'/api/files/{fid}/share', json={}, headers={'X-CSRF-Token':csrf(client)}).status_code==409
    client.patch(f'/api/files/{fid}', json={'visibility':'public'}, headers={'X-CSRF-Token':csrf(client)})
    r=client.post(f'/api/files/{fid}/share', json={}, headers={'X-CSRF-Token':csrf(client)}); assert r.status_code==201
    token=r.json()['share']['url'].rsplit('/',1)[1]
    assert client.get(f'/api/share/{token}').status_code==200
    assert client.get(f'/api/share/{token}/download').status_code==200
    assert client.delete(f'/api/files/{fid}/share', headers={'X-CSRF-Token':csrf(client)}).status_code==204
    assert client.get(f'/api/share/{token}').status_code==404
