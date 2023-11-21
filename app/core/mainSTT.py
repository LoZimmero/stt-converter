import os

import torch
from transformers import pipeline

model_name = "openai/whisper-medium"
device = "cuda:0" if torch.cuda.is_available() else "cpu"


def transcribe(audio_filepath: str, MODEL: str = model_name) -> str:
    # Check if valid input
    if not audio_filepath or not MODEL or not os.path.exists(audio_filepath):
        return ""

    print(device)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=MODEL,
        chunk_length_s=30,
        device=device,
    )
    pipe.model.config.forced_decoder_ids = (pipe.tokenizer.get_decoder_prompt_ids(
        language="it", task="transcribe"
    ))
    print(audio_filepath)
    prediction = pipe(audio_filepath)
    print(prediction)
    return prediction["text"]


def main():
    transcribe('../tests/resources/trimmed_Elettronica 2019-03-04 pt 1.wav')


if __name__ == '__main__':
    main()
