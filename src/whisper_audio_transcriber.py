# whisper_audio_transcriber.py

import os
from pathlib import Path
import requests
import librosa
from transformers import AutoProcessor, AutoModelForSpeechSeq2Seq, pipeline
from transformers.utils import logging
import soundfile as sf

# Definición de modelos
model_ids = {
    "Multilingual models": [
        "openai/whisper-large-v3-turbo",
        "openai/whisper-large-v3",
        "openai/whisper-large-v2",
        "openai/whisper-large",
        "openai/whisper-medium",
        "openai/whisper-small",
        "openai/whisper-base",
        "openai/whisper-tiny",
    ],
    "English-only models": [
        "distil-whisper/distil-large-v2",
        "distil-whisper/distil-large-v3",
        "distil-whisper/distil-medium.en",
        "distil-whisper/distil-small.en",
        "openai/whisper-medium.en",
        "openai/whisper-small.en",
        "openai/whisper-base.en",
        "openai/whisper-tiny.en",
    ],
}

def download_file(url, filename, directory="."):
    """
    Descarga un archivo desde una URL y lo guarda en el directorio especificado.
    """
    os.makedirs(directory, exist_ok=True)
    filepath = Path(directory) / filename
    response = requests.get(url)
    filepath.write_bytes(response.content)
    return filepath

def transcribe_audio(file_path, model_name):
    """
    Transcribe el audio utilizando un modelo de Whisper.
    
    Args:
        file_path (str): Ruta del archivo de audio.
        model_name (str): Nombre del modelo de Whisper.
        
    Returns:
        str: Transcripción del audio.
    """
    processor = AutoProcessor.from_pretrained(model_name)
    model = AutoModelForSpeechSeq2Seq.from_pretrained(model_name)
    
    # Crear pipeline para transcripción
    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        device="cpu",  # Cambiar a "cuda" si tienes una GPU disponible
    )
    
    # Cargar el archivo de audio
    audio_data, samplerate = librosa.load(file_path, sr=16000)
    
    # Transcribir el audio
    result = pipe(audio_data)
    return result["text"]

def guardar_transcripcion(texto, filename="transcripcion.txt", directory="../results"):
    """
    Guarda el texto transcrito en un archivo .txt en el directorio especificado.
    
    Args:
        texto (str): Texto transcrito que se desea guardar.
        filename (str): Nombre del archivo .txt.
        directory (str): Directorio donde se guardará el archivo.
    """
    os.makedirs(directory, exist_ok=True)  # Crea el directorio si no existe
    file_path = Path(directory) / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(texto)
    print(f"Transcripción guardada en: {file_path}")

def main():
    # Configuración de logging para errores únicamente
    logging.set_verbosity_error()
    
    # Ruta del archivo de audio
    audio_path = os.path.abspath("../miwav2lipv6/assets/audio/grabacion_gradio.wav")

    # Modelo seleccionado
    model_name = "openai/whisper-large"  # Cambia esto al modelo deseado

    # Transcribir el audio
    print(f"Transcribiendo el audio del archivo: {audio_path}")
    transcription = transcribe_audio(audio_path, model_name)
    print(f"Transcripción: {transcription}")

    # Guardar la transcripción en un archivo .txt
    guardar_transcripcion(transcription)

if __name__ == "__main__":
    main()
