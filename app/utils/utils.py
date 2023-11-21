import numpy as np
from app.core.models import TranscriptionRequest
from pydub import AudioSegment
from pydub.generators import WhiteNoise


def parse_request(req_json: dict) -> TranscriptionRequest:
    if not req_json:
        return None

    audio_bytes = req_json.get('audio_bytes')
    audio_format = req_json.get('audio_format')

    return TranscriptionRequest(audio_bytes, audio_format)


def apply_noise(audiopath, noise_level):
    audio = AudioSegment.from_file(audiopath)
    # Calcola la durata dell'audio in millisecondi
    duration_ms = len(audio)

    # Crea un generatore di rumore bianco della stessa durata dell'audio
    noise = WhiteNoise().to_audio_segment(duration=duration_ms)

    # Imposta il volume del rumore proporzionalmente al valore di noise_level
    noise_gain = audio.dBFS - 20 * np.log10(1 / noise_level)
    noise = noise.apply_gain(noise_gain - noise.dBFS)

    # Combina l'audio originale con il rumore
    mixed_audio = audio.overlay(noise)

    return mixed_audio


def change_amplitude(audiopath, gain_in_dB):
    """
    Adjusts the amplitude of the audio.
    :param audio: AudioSegment object.
    :param gain_in_dB: Amount of gain to apply in dB. Positive values increase volume, negative values decrease it.
    :return: AudioSegment object with adjusted amplitude.
    """
    audio = AudioSegment.from_file(audiopath)

    return audio + gain_in_dB


def speed_up_audio(audiopath, speed_factor):
    """
    Accelerates the audio by the given speed factor. Equivalent to changing frequency of audio
    :param audio: AudioSegment object.
    :param speed_factor: Speed up factor (e.g., 2.0 to double the speed).
    :return: AudioSegment object with modified speed.
    """
    audio = AudioSegment.from_file(audiopath)

    return audio.speedup(playback_speed=speed_factor)


def distort(audiopath, threshold=0.6):
    audio = AudioSegment.from_file(audiopath)

    samples = audio.get_array_of_samples()

    # Applica una funzione non lineare a ciascun campione
    distorted_samples = [int(sample * threshold) if abs(sample) < threshold * audio.max_possible_amplitude else int(
        audio.max_possible_amplitude if sample > 0 else -audio.max_possible_amplitude) for sample in samples]

    # Converte la lista di campioni distorti in un array
    np_samples = np.array(distorted_samples, dtype=np.int16)

    # Crea un nuovo segmento audio dai campioni distorti
    distorted_audio = audio._spawn(np_samples.tobytes())

    return distorted_audio
