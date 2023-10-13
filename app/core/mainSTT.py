import librosa
import torch
import whisper
from pydub import silence, AudioSegment

from transformers import (
    Wav2Vec2ForCTC,
    Wav2Vec2Processor,
)

MODEL = "whisper"
whisper_size="medium"
already_chunked= True

model_name = "facebook/wav2vec2-large-xlsr-53-italian"
device = "cuda" if torch.cuda.is_available() else "cpu"

model = Wav2Vec2ForCTC.from_pretrained(model_name).to(device)
processor = Wav2Vec2Processor.from_pretrained(model_name)


def split(file_data: bytes, max_file_size: int) -> list:
    res = []
    for i in range(0, len(file_data), max_file_size):
        res.append(file_data[i:i + max_file_size])
    return res


def transcribe(audio_filepath: str) -> str:
    if (MODEL == "legacy"):
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
    elif(already_chunked==False):
        # Carica il modello Whisper
        model = whisper.load_model(whisper_size).to(device)

        # Carica il file audio
        print("Caricamento audio...")
        audio = AudioSegment.from_wav(audio_filepath)
        # Se l'audio è inferiore a 30 secondi, trascrivi direttamente
        if len(audio) < 30000:
            print("L'audio è inferiore a 30 secondi. Inizio trascrizione diretta...")
            result = model.transcribe(audio_filepath)
            return result["text"]

        # Definisci la durata target e la tolleranza in millisecondi
        target_duration = 30 * 1000
        tolerance = 5 * 1000

        # Definisci i parametri per la rilevazione del silenzio
        min_silence_len = 50
        # Calcola il livello di rumore di fondo medio
        background_noise_level = audio.dBFS

        # Utilizza questo livello (con un offset) come soglia di silenzio
        silence_thresh = background_noise_level + 5  # puoi sperimentare con differenti offset

        # Funzione per trovare il punto di divisione basato sul silenzio
        def find_split_point(segment, start, end):
            print(f"Ricerca silenzio per segmento da {start} a {end}...")
            potential_splits = silence.detect_silence(segment[start:end], min_silence_len=min_silence_len,
                                                      silence_thresh=silence_thresh)
            if potential_splits:
                # Utilizza il primo intervallo di silenzio trovato come punto di divisione
                return potential_splits[0][0] + start
            return None

        # Divide l'audio in segmenti basati sulla durata target e sul silenzio
        segments = []
        start = 0
        end = len(audio)

        while start < end:
            potential_end = start + target_duration
            split_point = find_split_point(audio, potential_end - tolerance, potential_end)

            if split_point:
                print(f"Dividere l'audio al punto {split_point}ms...")
                segments.append(audio[start:split_point])
                start = split_point
            else:
                print(f"Nessun silenzio trovato, divisione a {potential_end}ms...")
                segments.append(audio[start:potential_end])
                start = potential_end

        # Trascrivi ogni segmento e combina i risultati
        transcription = ""
        print("Inizio trascrizione...")

        for index, segment in enumerate(segments):

            print(f"Trascrizione del segmento {index + 1} di {len(segments)}...")

            # Salva il segmento in un file temporaneo
            temp_file = "temp_segment.wav"
            segment.export(temp_file, format="wav")

            # Trascrivi il segmento
            result = model.transcribe(temp_file, language="it")
            transcription += result["text"] + " "

        print("Trascrizione completata!")
        return transcription
    else:
        model = whisper.load_model(whisper_size).to(device)
        result = model.transcribe(audio_filepath,language="it")
        print(result['text'])
        return result["text"]

def main():
    transcribe('core/test.wav')


if __name__ == '__main__':
    main()
