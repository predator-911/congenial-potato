from .conftest import csrf, register


def test_invalid_extension_and_traversal_and_double_ext(client):
    register(client)
    for name in ['evil.exe','../secret.pdf','photo.jpg.php']:
        r=client.post('/api/files', files={'file':(name,b'bad','application/octet-stream')}, headers={'X-CSRF-Token':csrf(client)})
        assert r.status_code in (415,422)

def test_spoofed_mime_and_oversized_cleanup(client):
    register(client)
    assert client.post('/api/files', files={'file':('fake.pdf',b'not pdf','application/pdf')}, headers={'X-CSRF-Token':csrf(client)}).status_code==415
    big=b'%PDF-1.4\n'+b'a'*(3*1024*1024)
    assert client.post('/api/files', files={'file':('big.pdf',big,'application/pdf')}, headers={'X-CSRF-Token':csrf(client)}).status_code==413
