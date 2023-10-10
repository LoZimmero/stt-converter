import os

import requests
import whisper
from pydub import AudioSegment

filedata = open('../core/trimmed_Elettronica 2019-03-04 pt 1.wav', 'rb').read()

res = requests.post('http://localhost:9999/api/stt', data=filedata).json()

print(res)

'''
test command line
import subprocess

# Carica il file AAC
audio = AudioSegment.from_file(path, format="aac")

# Estrai i primi tre minuti (180000 millisecondi)
three_minutes = 1 * 60 * 1000  # 3 minuti in millisecondi
audio = audio[1 * 60 * 1000: 2 * 60 * 1000]

# Salva come WAV in un file temporaneo
temp_path = "temp.wav"
audio.export(temp_path, format="wav")
print(f"File converted and saved to {temp_path}")

# Definisci il comando come una lista di stringhe
comando = f"whisper {temp_path} --language it --model medium --task transcribe "

# Esegui il comando
processo = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE,  text=True, encoding='utf-8')

# Ottenere l'output e l'errore (se presente)
output = processo.stdout
errore = processo.stderr

# Stampa l'output e l'errore
print(f'Output: {output}')
print(f'Errore: {errore}')
os.remove(temp_path)
'''