import json
import socket
import uuid
from flask import Flask, request, Response
import os

from app.core.mainSTT import transcribe
from zeroconf import ServiceInfo, Zeroconf


def create_app():
    app = Flask(__name__)
    MAX_FILE_SIZE_MB = int(os.environ.get('MAX_FILE_SIZE_MB', default=5))
    print("MAX_FILE_SIZE_MB:", MAX_FILE_SIZE_MB)

    @app.route('/api/stt', methods=['POST'])
    def stt_controller():
        if 'audio' not in request.files:
            return Response(json.dumps({
                "status": "KO",
                "data": None,
                "error-message": "No audio file provided."
            }), status=400)

        audio_file = request.files['audio']
        audio = audio_file.read()

        # Check for the 'format' field and save its value in the 'audio_format' variable if it's not None
        audio_format = request.form.get('format', None)

        if len(audio) > MAX_FILE_SIZE_MB * 1024 * 1024:
            return Response(json.dumps({
                "status": "KO",
                "data": None,
                "error-message": "File size exceeds the maximum limit."
            }), status=400)

        # Assuming you want to save the file, though it's not necessary
        filename = str(uuid.uuid4()) + ".wav"
        os.makedirs('data', exist_ok=True)
        with open(f'data/{filename}', 'wb') as f:
            f.write(audio)

        try:
            # If you want to use the 'audio_format' variable in your 'transcribe' function, you can pass it as an argument here.
            res = transcribe(audio_filepath=f'data/{filename}')
        except Exception as e:
            error_message = e.__str__()
            return Response(json.dumps({
                "status": "KO",
                "data": None,
                "error-message": error_message
            }), status=500)

        # Cleanup (remove the file after processing)
        os.remove(f'data/{filename}')

        return Response(json.dumps({
            "status": "OK",
            "data": res,
            "error-message": None
        }), status=200)

    @app.route("/", methods=["GET"])
    def index() -> Response:
        return Response("<h1>Welcome!</h1><h2>API is at endpoint <b>/api/stt</b></h2>", status=200)

    return app





def register_mdns_service():
    info = ServiceInfo(
        "_http._tcp.local.",
        "MyFlaskApp._http._tcp.local.",
        addresses=[socket.inet_aton("0.0.0.0")],
        port=9999,
        properties={'path': '/'},
        server="MyFlaskApp.local.",
    )

    zeroconf = Zeroconf()
    print("Registration of a service...")
    zeroconf.register_service(info)
    return zeroconf


def main():
    zeroconf_instance = register_mdns_service()

    app = create_app()
    app.run(
        host='0.0.0.0',
        port=9999,
        debug=False,
        load_dotenv=True
    )

    zeroconf_instance.close()


if __name__ == '__main__':
    main()
