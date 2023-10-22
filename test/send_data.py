import json
import os
import time

import numpy as np
import requests
from pydub import AudioSegment
from pydub.generators import WhiteNoise

def apply_noise(audio, noise_level):
    # Calcola la durata dell'audio in millisecondi
    duration_ms = len(audio)

    # Crea un generatore di rumore bianco della stessa durata dell'audio
    noise = WhiteNoise().to_audio_segment(duration=duration_ms)

    # Imposta il volume del rumore proporzionalmente al valore di noise_level
    noise_gain = audio.dBFS - 20 * np.log10(1/noise_level)
    noise = noise.apply_gain(noise_gain - noise.dBFS)

    # Combina l'audio originale con il rumore
    mixed_audio = audio.overlay(noise)

    return mixed_audio



def change_amplitude(audio, gain_in_dB):
    """
    Adjusts the amplitude of the audio.
    :param audio: AudioSegment object.
    :param gain_in_dB: Amount of gain to apply in dB. Positive values increase volume, negative values decrease it.
    :return: AudioSegment object with adjusted amplitude.
    """
    return audio + gain_in_dB

def speed_up_audio(audio, speed_factor):
    """
    Accelerates the audio by the given speed factor. Equivalent to changing frequency of audio
    :param audio: AudioSegment object.
    :param speed_factor: Speed up factor (e.g., 2.0 to double the speed).
    :return: AudioSegment object with modified speed.
    """
    return audio.speedup(playback_speed=speed_factor)

def distort(audio_segment, threshold=0.6):
    samples = audio_segment.get_array_of_samples()

    # Applica una funzione non lineare a ciascun campione
    distorted_samples = [int(sample * threshold) if abs(sample) < threshold * audio_segment.max_possible_amplitude else int(audio_segment.max_possible_amplitude if sample > 0 else -audio_segment.max_possible_amplitude) for sample in samples]

    # Converte la lista di campioni distorti in un array
    np_samples = np.array(distorted_samples, dtype=np.int16)

    # Crea un nuovo segmento audio dai campioni distorti
    distorted_audio = audio_segment._spawn(np_samples.tobytes())

    return distorted_audio

# Carica il file audio
audio = AudioSegment.from_file("../app/core/trimmed_Elettronica 2019-03-04 pt 1.wav")

# Ottieni il livello sonoro in dB
loudness = audio.dBFS
print(f"Loudness: {loudness} dB")

# Applica trasformazioni all'audio
noisy_audio = apply_noise(audio, 0.0000001)
# noisy_audio = speed_up_audio(noisy_audio, 1.5)
# noisy_audio = change_amplitude(noisy_audio, 500)
# noisy_audio = distort(noisy_audio, 0.2)

# Esporta l'audio modificato
exported_filename = "noisy_audio.mp3"
noisy_audio.export(exported_filename, format="mp3")

# Invia l'audio a un server locale per la trasformazione in testo (STT)
with open(exported_filename, 'rb') as f:
    files = {'audio': f}
    start_time = time.time()
    res = requests.post('http://localhost:9999/api/stt', files=files).json()
    end_time = time.time()

elapsed_time = (end_time - start_time) * 1000  # Converti in millisecondi

print(res)
print(f"Tempo impiegato: {elapsed_time:.2f} ms")
os.remove(exported_filename)