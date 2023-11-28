Questo server si occupa del servizio di trascrizione per l'applicazione https://github.com/S-Federico/Sbobinator9000 , va utilizzato connettendo sia server che client alla stessa rete.

# Istruzioni per l'uso

## Intallare ffmpeg sulla macchina che esegue il server
installare ffmpeg e aggiungerlo al path

## 1. Installare dipendenze necessarie

E' possibile installare tutte le dipendenze necessarie con il seguente comando:

```
pip install -r requirements.txt
```

## 2. Avviare il server

Basta eseguire il file *server.py*

## 3. Tests e come eseguirli
Nella cartella *app/tests* possiamo inserire test unitari e di integrazione. <br>
Per poterli eseguire, bisogna avere installati i moduli *pytest* e *pytest-cov* (per avere la coverage).<br>
Il comando da utilizzare è:
```
pytest --cov --cov-report=html:coverage_re
```
**Nota**: E' importante eseguire il comando a livello di root del progetto, ovvero dalla cartella stt, poiché i test usano path relativi per recuperare i files necessari all'esecuzione.
