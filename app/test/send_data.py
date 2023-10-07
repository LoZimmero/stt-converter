import requests

filedata = open('../core/Recording 2023-10-07 19_15_40.mp3', 'rb').read()

res = requests.post('http://localhost:9999/api/stt', data=filedata).json()

print(res)