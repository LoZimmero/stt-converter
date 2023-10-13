import json
import re
import uuid
from flask import Flask, request, Response
import os

from app.core.mainSTT import transcribe, split

def create_app():
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

        string_result = ''.join(res)
        return Response(json.dumps({
            "status": "OK" if res else "KO",
            # old code "data": '\n\n'.join(res),
            "data": string_result,
            "error-message": error_message
        }), status=200 if res else 500)

    @app.route("/", methods=["GET"])
    def index() -> Response:
        return Response("<h1>Welcome!</h1><h2>API is at edpoint <b>/api/stt</b></h2>", status=200)

    return app

def main():
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=9999,
        debug=False,
        load_dotenv=True
    )


if __name__ == '__main__':
    main()
