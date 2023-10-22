import torch
from transformers import pipeline

model_name = "openai/whisper-tiny"
device = "cuda:0" if torch.cuda.is_available() else "cpu"

def split(file_data: bytes, max_file_size: int) -> list:
    if not file_data or not max_file_size or max_file_size < 1:
        return []
    res = []
    for i in range(0, len(file_data), max_file_size):
        res.append(file_data[i:i + max_file_size])
    return res


def transcribe(audio_filepath: str, MODEL: str = model_name) -> str:

    # Check if valid input
    if not audio_filepath or not MODEL:
        return []

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
    transcribe('trimmed_Elettronica 2019-03-04 pt 1.wav')


if __name__ == '__main__':
    main()
