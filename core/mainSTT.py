import librosa
import torch
from transformers import (
    Wav2Vec2ForCTC,
    Wav2Vec2Processor,
)

model_name = "facebook/wav2vec2-large-xlsr-53-italian"
device = "cuda" if torch.cuda.is_available() else "cpu"

model = Wav2Vec2ForCTC.from_pretrained(model_name).to(device)
processor = Wav2Vec2Processor.from_pretrained(model_name)


def split(file_data: bytes, max_file_size: int) -> list[bytes]:
    res = []
    for i in range(0, len(file_data), max_file_size):
        res.append(file_data[i:i + max_file_size])
    return res


def transcribe(audio_filepath: str) -> str:
    audio_path = audio_filepath

    speech, sr = librosa.load(audio_path, sr=16000, mono=True)

    speech = speech[:(sr * 10)]

    features = processor(speech, sampling_rate=sr, return_tensors="pt", padding="longest")
    input_values = features.input_values.to(device)
    attention_mask = features.attention_mask.to(device)
    with torch.no_grad():
        logits = model(input_values, attention_mask=attention_mask).logits
    pred_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(pred_ids)

    return transcription


def main():
    transcribe('core/test.wav')


if __name__ == '__main__':
    main()
