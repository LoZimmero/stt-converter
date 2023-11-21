import json

from werkzeug.test import TestResponse, Client


def test_transcribe_null_body(client: Client):
    response: TestResponse = client.post("/api/stt", data=None)

    assert response.status_code == 400
    assert json.loads(response.data)['status'] == 'KO'
    assert json.loads(response.data)['data'] is None
    assert json.loads(response.data)['error-message'] is not None
