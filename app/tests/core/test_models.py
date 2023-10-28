from app.core.models import TranscriptionRequest


def test_TranscriptionRequest_creation():
    tr = TranscriptionRequest([1, 2, 4, 6], 'wav')
    assert tr is not None
    assert tr.audio_bytes == [1, 2, 4, 6]
    assert tr.audio_format == 'wav'
