# Istruzioni per l'uso

## aggiungo qua le cose in più per whisper
pip install git+https://github.com/openai/whisper.git 
installare ffmpeg (e aggiungerlo al path, se pycharm era già avviato, riavviare pycharm)
assicurarsi che ffmpeg sia visibile dal terminale di pycharm (scrivere ffmpeg basta, se esce qualcosa allora ok)
installare pydub(pip)



## 1. Installare dipendenze necessarie

E' possibile installare tutte le dipendenze necessarie con il seguente comando:

```
pip install -r requirements.txt
```

L'importante è installare **Flask** oltre le dipendenze per il stt

## 2. Lanciare il server

Basta eseguire il file *server.py*

## 3. Lanciare il test

Basta eseguire il file *test/send_data.py"*