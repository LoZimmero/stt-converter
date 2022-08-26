import uuid
from flask import Flask, request

from core.mainSTT import transcribe

app = Flask(__name__)

@app.route('/api/stt', methods=['POST'])
def stt_controller():
    audio = request.data
    filename = uuid.uuid4().__str__
    with open(f'data/{filename}', 'wb') as f:
        f.write(audio)
    
    return transcribe(audio_filepath=filename)


def main():
    app.run(
        host='localhost',
        port=9999,
        debug=True
    )

if (__name__=='__main__'):
    main()
