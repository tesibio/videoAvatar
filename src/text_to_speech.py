# text_to_speech.py

from gtts import gTTS
import os

# Rutas de los archivos
TRANSCRIPTION_TEXT_PATH = "C:/programacionEjercicios/miwav2lipv6/results/transcripcion.txt"
OUTPUT_AUDIO_PATH = "C:/programacionEjercicios/miwav2lipv6/assets/audio/audio.wav"

def generar_audio_desde_texto():
    """
    Convierte el texto en `transcripcion.txt` a un archivo de audio en español (`audio.wav`).
    """
    try:
        # Verificar si el archivo de transcripción existe
        if not os.path.exists(TRANSCRIPTION_TEXT_PATH):
            print("Error: No se encontró el archivo de transcripción.")
            return

        # Leer el contenido de transcripcion.txt
        with open(TRANSCRIPTION_TEXT_PATH, "r", encoding="utf-8") as file:
            texto = file.read()

        # Generar el audio en español usando gTTS
        tts = gTTS(text=texto, lang='es', slow=False)
        tts.save(OUTPUT_AUDIO_PATH)

        print(f"Audio generado correctamente en: {OUTPUT_AUDIO_PATH}")

    except Exception as e:
        print(f"Error al generar el audio: {e}")

if __name__ == "__main__":
    generar_audio_desde_texto()

