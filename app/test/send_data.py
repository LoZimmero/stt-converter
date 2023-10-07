import requests

filedata = open('../core/Recording 2023-10-07 17_51_02.wav', 'rb').read()

res = requests.post('http://localhost:9999/api/stt', data=filedata).json()

print(res)