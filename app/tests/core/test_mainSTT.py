import os
import tempfile

import pytest
from Levenshtein import ratio

from app.core.mainSTT import transcribe
from app.utils.utils import apply_noise, change_amplitude, speed_up_audio, distort


def compute_similarity(reference, transcription):
    return ratio(reference, transcription)


def load_reference(reference_file):
    with open(reference_file, 'r') as file:
        return file.read().strip()


@pytest.mark.parametrize(
    "audio_modifier, para",
    [(apply_noise, 0.1),
     (change_amplitude, 1.4),
     (speed_up_audio, 1.3),
     (distort, 0.2)]
)
def test_transcription_similarity(audio_modifier, para):
    original_audio = ('./app/tests/resources/trimmed_Elettronica 2019-03-04 pt 1.wav')
    reference_transcription = load_reference('./app/tests/resources/reference_transcription.txt')

    # Use a temporary directory to save the modified audio
    with tempfile.TemporaryDirectory() as tmpdirname:
        # Define the temporary WAV file path
        temp_audio_path = os.path.join(tmpdirname, "modified_audio.wav")
        modified_audio = audio_modifier(original_audio, para)

        # Assuming `modified_audio` is a waveform, save it to the temporary WAV file.
        # Depending on your implementation, you might need a function here to save the waveform to WAV.
        modified_audio.export(temp_audio_path, format="wav")

        prediction = transcribe(temp_audio_path)
        similarity = compute_similarity(reference_transcription, prediction)

        assert similarity >= 0.7, f"Failed with method {audio_modifier.__name__}. Similarity: {similarity}"

    # Temporary directory and all its contents are automatically deleted at this point
