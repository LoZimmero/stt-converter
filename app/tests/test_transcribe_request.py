from werkzeug.test import TestResponse, Client

def test_transcribe_null_body(client: Client):
    response: TestResponse = client.post("/api/stt",data=None)
    status = response.status_code
    data = response.json

    assert 500 == status
    assert data['status'] == 'KO'
    assert data['data'] == None
    assert data['error-message'] != None