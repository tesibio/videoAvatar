# whisper_audio_extractor.py

import sounddevice as sd
from scipy.io.wavfile import write
import whisper
import os

# Ruta para guardar el archivo de audio temporalmente
AUDIO_PATH = os.path.join("..", "assets", "audio", "recorded_audio.wav")

def record_audio(duration=5, sample_rate=44100):
    """
    Graba el audio del micrófono durante un tiempo específico y lo guarda como archivo WAV.
    
    Args:
        duration (int): Duración de la grabación en segundos.
        sample_rate (int): Frecuencia de muestreo del audio.
    """
    print("Grabando...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2)
    sd.wait()  # Espera a que finalice la grabación
    write(AUDIO_PATH, sample_rate, audio_data)  # Guarda el audio en el directorio especificado
    print(f"Grabación completa. Archivo guardado en {AUDIO_PATH}")

def transcribe_audio():
    """
    Usa el modelo Whisper para transcribir el audio grabado y devuelve el texto.
    
    Returns:
        str: Texto transcrito del audio.
    """
    # Cargar el modelo de Whisper
    model = whisper.load_model("base")
    
    # Transcribir el audio
    print("Transcribiendo el audio...")
    result = model.transcribe(AUDIO_PATH)
    print("Transcripción completada.")
    return result["text"]

if __name__ == "__main__":
    # Paso 1: Grabar audio
    record_audio()

    # Paso 2: Transcribir audio
    texto = transcribe_audio()
    print("Texto extraído:", texto)
