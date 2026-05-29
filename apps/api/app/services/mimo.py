import base64
import io
import math
import wave
from dataclasses import dataclass
from typing import Any

import httpx

from app.core.config import settings


@dataclass(frozen=True)
class TTSResult:
  audio: bytes
  mime_type: str
  duration_seconds: float


class MimoTTSClient:
  def synthesize(
    self,
    *,
    text: str,
    voice_name: str,
    style_prompt: str | None,
    audio_format: str,
  ) -> TTSResult:
    if settings.mimo_api_key == "dev-placeholder" or not settings.mimo_tts_url:
      return self._mock_wav(text)

    response = httpx.post(
      self._completion_url(),
      headers={
        "api-key": settings.mimo_api_key,
        "Content-Type": "application/json",
      },
      json=self._request_payload(
        text=text,
        voice_name=voice_name,
        style_prompt=style_prompt,
        audio_format=audio_format,
      ),
      timeout=90,
    )
    response.raise_for_status()
    payload = response.json()
    encoded_audio = self._extract_audio_base64(payload)
    if not encoded_audio:
      raise ValueError("MiMo response did not include base64 audio")

    mime_type = "audio/mpeg" if audio_format == "mp3" else "audio/wav"
    return TTSResult(
      audio=base64.b64decode(encoded_audio),
      mime_type=mime_type,
      duration_seconds=float(payload.get("duration_seconds") or max(1.0, len(text) / 80)),
    )

  def _completion_url(self) -> str:
    url = settings.mimo_tts_url.rstrip("/")
    if url.endswith("/v1"):
      return f"{url}/chat/completions"
    return url

  def _request_payload(
    self,
    *,
    text: str,
    voice_name: str,
    style_prompt: str | None,
    audio_format: str,
  ) -> dict[str, object]:
    messages: list[dict[str, str]] = []
    if style_prompt:
      messages.append({"role": "user", "content": style_prompt})
    messages.append({"role": "assistant", "content": text})

    return {
      "model": "mimo-v2.5-tts",
      "messages": messages,
      "audio": {
        "format": audio_format,
        "voice": voice_name,
      },
    }

  def _extract_audio_base64(self, payload: dict[str, Any]) -> str | None:
    choices = payload.get("choices")
    if isinstance(choices, list) and choices:
      first_choice = choices[0]
      if isinstance(first_choice, dict):
        message = first_choice.get("message")
        if isinstance(message, dict):
          audio = message.get("audio")
          if isinstance(audio, dict):
            data = audio.get("data")
            if isinstance(data, str):
              return data

    for key in ("audio_base64", "audio"):
      value = payload.get(key)
      if isinstance(value, str):
        return value

    return None

  def _mock_wav(self, text: str) -> TTSResult:
    duration_seconds = min(4.0, max(1.0, len(text) / 80))
    sample_rate = 22050
    frames = int(sample_rate * duration_seconds)
    buffer = io.BytesIO()

    with wave.open(buffer, "wb") as wav_file:
      wav_file.setnchannels(1)
      wav_file.setsampwidth(2)
      wav_file.setframerate(sample_rate)
      for index in range(frames):
        sample = int(8000 * math.sin(2 * math.pi * 220 * (index / sample_rate)))
        wav_file.writeframesraw(sample.to_bytes(2, "little", signed=True))

    return TTSResult(
      audio=buffer.getvalue(),
      mime_type="audio/wav",
      duration_seconds=duration_seconds,
    )
