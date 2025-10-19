from pathlib import Path
from openai import OpenAI
client = OpenAI()

speech_file_path = Path(__file__).parent / "speech.mp3"
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input="Olá! Mas que belo dia! O que posso fazer por você hoje?"
)

response.stream_to_file(speech_file_path)
