from .conftest import csrf, register, upload_pdf


def test_upload_list_rename_download_delete(client):
    register(client); r=upload_pdf(client); assert r.status_code==201, r.text
    fid=r.json()['file']['id']; assert client.get('/api/files').json()['total']==1
    assert client.patch(f'/api/files/{fid}', json={'original_filename':'renamed.pdf'}, headers={'X-CSRF-Token':csrf(client)}).status_code==200
    assert client.get(f'/api/files/{fid}/download').status_code==200
    assert client.delete(f'/api/files/{fid}', headers={'X-CSRF-Token':csrf(client)}).status_code==204
    assert client.get('/api/files').json()['total']==0
