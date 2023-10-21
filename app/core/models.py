class TranscriptionRequest:
    audio_bytes: bytes = None
    audio_format: str = None

    def __init__(self, audio_bytes: bytes, audio_format: str) -> None:
        self.audio_bytes = audio_bytes
        self.audio_format = audio_format