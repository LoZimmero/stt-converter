import requests

filedata = open('../core/trimmed_Elettronica 2019-03-04 pt 1.wav', 'rb').read()

res = requests.post('http://localhost:9999/api/stt', data=filedata).json()

print(res)