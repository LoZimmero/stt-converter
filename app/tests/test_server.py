import os
import json
import tempfile
from app.server import create_app

import pytest


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        yield client


def test_index(client):
    """ Test the index endpoint """
    response = client.get('/')
    assert b'Welcome!' in response.data


def test_stt_without_audio(client):
    """ Test the /api/stt endpoint without audio """
    response = client.post('/api/stt')
    assert response.status_code == 400
    assert json.loads(response.data)['error-message'] == "No audio file provided."


def test_stt_with_large_file(client):
    """ Test the /api/stt endpoint with a file larger than the limit """
    dummy_file = tempfile.NamedTemporaryFile(suffix='.wav')
    dummy_file.write(b'0' * (int(os.environ.get('MAX_FILE_SIZE_MB', default=5)) * 1024 * 1024))

    response = client.post('/api/stt', content_type='multipart/form-data',
                           data={"audio": (dummy_file, "dummy.wav")})

    assert response.status_code == 400
    assert json.loads(response.data)['error-message'] == "File size exceeds the maximum limit."


def test_stt_ok(client):
    """ Test the /api/stt endpoint with a valid audio file """
    with open('./app/tests/resources/test.wav', 'rb') as f:
        response = client.post('/api/stt', content_type='multipart/form-data',
                               data={"audio": (f, "test.wav")})
    assert response.status_code == 200
    assert json.loads(response.data)['status'] == "OK"

# You can expand on these tests by:
# 3. Testing error handling when the transcribe function fails
