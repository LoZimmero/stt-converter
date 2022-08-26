import json
import re
import uuid
from flask import Flask, request, Response
import os

from core.mainSTT import transcribe

app = Flask(__name__)

@app.route('/api/stt', methods=['POST'])
def stt_controller():
    audio = request.data
    #print(audio)
    filename = str(uuid.uuid4())
    with open(f'data/{filename}', 'wb') as f:
        f.write(audio)
    
    res = None
    error_message = None
    try:
        res = transcribe(audio_filepath=f'data/{filename}')
        print(res)
    except:
        error_message = "ERROR: Failed to parse"
    finally:
        os.remove(f'data/{filename}')
        return Response(json.dumps({
            "status": "OK" if res else "KO",
            "data": res,
            "error-message": error_message
        }), status=200 if res else 500)

def main():
    app.run(
        host='localhost',
        port=9999,
        debug=True
    )

if (__name__=='__main__'):
    main()
