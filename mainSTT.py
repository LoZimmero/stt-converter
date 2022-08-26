import tensorflow
import torchaudio
from datasets import load_dataset, load_metric
from transformers import (
    Wav2Vec2ForCTC,
    Wav2Vec2Processor,
)
import torch
import re
import sys
import librosa

def main():
    model_name = "facebook/wav2vec2-large-xlsr-53-italian"
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = Wav2Vec2ForCTC.from_pretrained(model_name).to(device)
    processor = Wav2Vec2Processor.from_pretrained(model_name)

    audio_path = 'Registrazione in corso.wav'

    speech, sr = librosa.load(audio_path, sr=16000, mono=True)

    speech = speech[:(sr * 10)]

    features = processor(speech, sampling_rate=sr, return_tensors="pt", padding="longest")
    input_values = features.input_values.to(device)
    attention_mask = features.attention_mask.to(device)
    with torch.no_grad():
        logits = model(input_values, attention_mask=attention_mask).logits
    pred_ids = torch.argmax(logits, dim=-1)
    transcription = processor.batch_decode(pred_ids)

    print(transcription)


if __name__ == '__main__':
    main()