from app.utils import utils
from app.core.models import TranscriptionRequest

def test_parse_request_inputNone():
    res = utils.parse_request(None)
    assert res == None


def test_parse_request_input_empty():
    res = utils.parse_request({})
    assert res == None

def test_parse_request_missing_values():
    res = utils.parse_request({"unused_field":"RandomValue"})
    assert res.audio_bytes == None
    assert res.audio_format == None


def test_parse_request_missing_bytes():
    res = utils.parse_request({"audio_format":"wav"})
    assert res.audio_bytes == None
    assert res.audio_format == 'wav'

def test_parse_request_complete():
    res = utils.parse_request({"audio_format":"wav", 'audio_bytes': [1,2,4,2,4,2]})
    assert res.audio_bytes == [1,2,4,2,4,2]
    assert res.audio_format == 'wav'