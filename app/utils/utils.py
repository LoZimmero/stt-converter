from app.core.models import TranscriptionRequest

def parse_request(req_json: dict) -> TranscriptionRequest:
    if not req_json:
        return None
    
    audio_bytes = req_json.get('bytes')
    audio_format = req_json.get('format')

    return TranscriptionRequest(audio_bytes, audio_format)