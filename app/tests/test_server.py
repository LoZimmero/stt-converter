import io
import json
import os

import pytest

from app.server import create_app


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


def generate_large_file(size_mb):
    """Generates an in-memory binary stream of the given size in MB."""
    return io.BytesIO(b"\0" * size_mb * 1024 * 1024)


def test_stt_with_large_file():
    # Create a test client
    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    # Generate a 6 MB dummy file (or any size that exceeds your set limit)
    audio_file = generate_large_file(6)

    # Reset the file pointer to the beginning
    audio_file.seek(0)

    # Get the actual file size
    actual_size = len(audio_file.read())
    print(f"Actual file size: {actual_size} bytes")
    audio_file.seek(0)  # Reset the file pointer again to ensure the client can read it

    # Make a POST request
    response = client.post('/api/stt', content_type='multipart/form-data', data={'audio': (audio_file, 'test.wav')})

    # Assertions to check the response
    assert response.status_code == 400


def test_stt_ok(client):
    """ Test the /api/stt endpoint with a valid audio file """
    test_wav_path = os.path.join(os.path.dirname(__file__), 'resources', 'test.wav')
    with open(test_wav_path, 'rb') as f:
        response = client.post('/api/stt', content_type='multipart/form-data',
                               data={"audio": (f, "test.wav")})

    assert response.status_code == 200
    assert json.loads(response.data)['status'] == "OK"

# You can expand on these tests by:
# 3. Testing error handling when the transcribe function fails
