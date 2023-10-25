# Istruzioni per l'uso

## Intallare ffmpeg sulla macchina che esegue il server
installare ffmpeg e aggiungerlo al path, se pycharm era già avviato riavviare pycharm
assicurarsi che ffmpeg sia visibile dal terminale di pycharm (scrivere ffmpeg basta, se esce qualcosa allora ok)



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

## 4. Tests e come eseguirli
Nella cartella *app/tests* possiamo inserire test unitari e di integrazione. <br>
Per poterli eseguire, bisogna avere installati i moduli *pytest* e *pytest-cov* (per avere la coverage).<br>
Il comando da utilizzare è:
```
pytest --cov --cov-report=html:coverage_re
```
**Nota**: E' importante eseguire il comando a livello di root del progetto, ovvero dalla cartella stt, poiché i test usano path relativi per recuperare i files necessari all'esecuzione.
