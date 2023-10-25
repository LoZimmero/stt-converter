from app.core.mainSTT import transcribe


def test_transcribe_null_path():
    data = transcribe(None)
    assert data == ""


def test_transcribe_non_existsing_file():
    data = transcribe('./aaaa/bbbbb')
    assert data == ""


def test_transcribe_ok():
    data = transcribe('./app/tests/resources/test.wav')
    assert 'ciao' in data.lower()
