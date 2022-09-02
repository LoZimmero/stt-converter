import json
import re
import uuid
from flask import Flask, request, Response
import os

from core.mainSTT import transcribe, split

app = Flask(__name__)

MAX_FILE_SIZE_MB = int(os.environ.get('MAX_FILE_SIZE_MB', default=5))

print("MAX_FILE_SIZE_MB:", MAX_FILE_SIZE_MB)


@app.route('/api/stt', methods=['POST'])
def stt_controller():
    audio = request.data

    audio_chunks = split(audio, MAX_FILE_SIZE_MB * 1024 * 1024)

    res = []
    error_message = None

    for audio in audio_chunks:
        filename = str(uuid.uuid4())
        with open(f'data/{filename}', 'wb') as f:
            f.write(audio)

        try:
            temp_res = transcribe(audio_filepath=f'data/{filename}')
            res.extend(temp_res)
        except:
            error_message = "ERROR: Failed to parse"
            break
        finally:
            os.remove(f'data/{filename}')

    return Response(json.dumps({
        "status": "OK" if res else "KO",
        "data": '\n\n'.join(res),
        "error-message": error_message
    }), status=200 if res else 500)


def main():
    app.run(
        host='localhost',
        port=9999,
        debug=True,
        load_dotenv=True
    )


if __name__ == '__main__':
    main()
