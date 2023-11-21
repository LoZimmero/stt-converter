class TranscriptionRequest:
    audio_bytes: bytes = None
    audio_format: str = None

    def __init__(self, audio_bytes: bytes, audio_format: str) -> None:
        self.audio_bytes = audio_bytes
        self.audio_format = audio_format

    def __str__(self) -> str:
        return f"'audio_bytes': {self.audio_bytes}, 'audio_format': {self.audio_format}"