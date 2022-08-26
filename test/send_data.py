import requests

filedata = open('../core/test.wav', 'rb').read()

res = requests.post('http://localhost:9999/api/stt', data=filedata).json()

print(res)