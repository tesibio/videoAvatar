# audio_recorder.py

import sounddevice as sd
from scipy.io.wavfile import write
import os

# Ruta para guardar el archivo de audio en el directorio `assets/audio/`
AUDIO_PATH = os.path.join("..", "assets", "audio", "grabacion_8s.wav")

def listar_dispositivos():
    """
    Lista todos los dispositivos de audio disponibles en el sistema.
    """
    print("Dispositivos de audio disponibles:")
    dispositivos = sd.query_devices()
    for idx, dispositivo in enumerate(dispositivos):
        print(f"{idx}: {dispositivo['name']} - {'Entrada' if dispositivo['max_input_channels'] > 0 else 'Salida'}")
    print("\nSelecciona el índice del dispositivo de entrada que prefieras para grabar audio.")

def record_audio(duration=8, sample_rate=44100, device_index=None):
    """
    Graba el audio desde el micrófono durante un tiempo específico y lo guarda como archivo WAV.

    Args:
        duration (int): Duración de la grabación en segundos.
        sample_rate (int): Frecuencia de muestreo del audio.
        device_index (int): Índice del dispositivo de audio a utilizar.
    """
    print("Grabando...")

    # Iniciar la grabación con un canal
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, device=device_index)
    sd.wait()  # Espera a que la grabación termine

    # Guardar el archivo de audio
    write(AUDIO_PATH, sample_rate, audio_data)
    print(f"Grabación completada. Archivo guardado en: {AUDIO_PATH}")

if __name__ == "__main__":
    # Paso 1: Listar dispositivos de audio
    listar_dispositivos()
    
    # Aquí esperaremos tu selección del índice del dispositivo
    device_index = int(input("Introduce el índice del dispositivo de entrada que deseas utilizar: "))

    # Paso 2: Grabar audio con el dispositivo seleccionado
    record_audio(device_index=device_index)

