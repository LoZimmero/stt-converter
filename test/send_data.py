import requests

filedata = open('./Prov.aac', 'rb').read()

res = requests.post('http://localhost:9999/api/stt', data=filedata).json()

print(res)