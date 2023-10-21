from core.models import TranscriptionRequest

def parse_request(req_json: dict) -> TranscriptionRequest:
    if not req_json:
        return None
    
    audio_bytes = bytes(req_json.get('audio_bytes'), 'utf-8') # Covert string into bytes
    audio_format = req_json.get('audio_format')

    return TranscriptionRequest(audio_bytes, audio_format)