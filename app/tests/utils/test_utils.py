import os

import pytest
from pydub import AudioSegment

from app.utils import utils
from app.utils.utils import apply_noise, change_amplitude, speed_up_audio, distort


def test_parse_request_inputNone():
    res = utils.parse_request(None)
    assert res is None


def test_parse_request_input_empty():
    res = utils.parse_request({})
    assert res is None


def test_parse_request_missing_values():
    res = utils.parse_request({"unused_field": "RandomValue"})
    assert res.audio_bytes is None
    assert res.audio_format is None


def test_parse_request_missing_bytes():
    res = utils.parse_request({"audio_format": "wav"})
    assert res.audio_bytes is None
    assert res.audio_format == 'wav'


def test_parse_request_complete():
    res = utils.parse_request({"audio_format": "wav", 'audio_bytes': [1, 2, 4, 2, 4, 2]})
    assert res.audio_bytes == [1, 2, 4, 2, 4, 2]
    assert res.audio_format == 'wav'


# test noise and modulation
def test_apply_noise():
    # Carica un file audio di esempio
    audio = os.path.join(os.path.dirname(__file__), '..', 'resources', 'test.wav')
    a = AudioSegment.from_file(audio)
    original_dBFS = a.dBFS

    # Applica il rumore
    noisy_audio = apply_noise(audio, 0.5)

    # Controlla che il dBFS dell'audio rumoroso sia diverso dall'audio originale
    assert noisy_audio.dBFS != original_dBFS


def test_change_amplitude():
    audio = os.path.join(os.path.dirname(__file__), '..', 'resources', 'test.wav')
    a = AudioSegment.from_file(audio)

    original_dBFS = a.dBFS

    # Cambia l'ampiezza
    louder_audio = change_amplitude(audio, 5)

    # Controlla che il dBFS sia aumentato di 5 dB
    assert pytest.approx(louder_audio.dBFS, abs=0.02) == pytest.approx(original_dBFS + 5, abs=0.02)


def test_speed_up_audio():
    audio = os.path.join(os.path.dirname(__file__), '..', 'resources', 'test.wav')
    a = AudioSegment.from_file(audio)

    # Aumenta la velocità dell'audio
    sped_up_audio = speed_up_audio(audio, 2.0)

    # La durata dell'audio dovrebbe essere approssimativamente dimezzata
    assert sped_up_audio.duration_seconds == pytest.approx(a.duration_seconds / 2, 0.1)


def test_distort():
    audio = os.path.join(os.path.dirname(__file__), '..', 'resources', 'test.wav')
    a = AudioSegment.from_file(audio)

    # Distort the audio
    distorted_audio = distort(audio)

    # La durata dell'audio distorto dovrebbe rimanere la stessa
    assert distorted_audio.duration_seconds == pytest.approx(a.duration_seconds, 0.1)

    # L'audio distorto non dovrebbe essere identico all'audio originale
    assert distorted_audio.raw_data != a.raw_data
