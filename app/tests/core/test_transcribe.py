import os

from app.core.mainSTT import transcribe


def test_transcribe_null_path():
    data = transcribe(None)
    assert data == ""


def test_transcribe_non_existing_file():
    data = transcribe('./aaaa/bbbbb')
    assert data == ""


def test_transcribe_ok():
    test_wav_path = os.path.join(os.path.dirname(__file__), '..', 'resources', 'test.wav')
    data = transcribe(test_wav_path)
    assert 'ciao' in data.lower()
