# interface.py

import gradio as gr
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import shutil
import os

# Rutas de video y audio con absolutas para evitar errores de acceso
AUDIO_COPY_PATH = os.path.abspath(os.path.join("..", "miwav2lipv6","assets", "audio", "grabacion_gradio.wav"))
#VIDEO_PATH = os.path.abspath("../miwav2lipv6/assets/video/data_video_sun_5s.mp4")
VIDEO_PATH = os.path.abspath("../miwav2lipv6/assets/video/data_video_sun.mp4")

# Verificar la existencia del video
if not os.path.exists(VIDEO_PATH):
    print(f"Advertencia: El archivo de video no se encontró en la ruta {VIDEO_PATH}")

# Función para grabar audio
def grabar_audio(duration=8, sample_rate=44100):
    print("Grabando...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Espera a que la grabación termine

    # Guardar archivo temporal de audio
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp_audio.name, sample_rate, audio_data)
    print("Grabación completada. Archivo temporal guardado en:", temp_audio.name)

    # Verificar y crear `assets/audio` si no existe
    os.makedirs(os.path.dirname(AUDIO_COPY_PATH), exist_ok=True)

    # Copiar a `assets/audio`
    shutil.copy(temp_audio.name, AUDIO_COPY_PATH)
    print(f"Copia de la grabación guardada en: {AUDIO_COPY_PATH}")

    return AUDIO_COPY_PATH

# Función principal para la interfaz de Gradio
def interfaz():
    with gr.Blocks() as demo:
        gr.Video(VIDEO_PATH, loop=True, autoplay=True, height=300, width=500)
        
        # Crear un botón de grabación
        with gr.Row():
            grabar_button = gr.Button("Iniciar Grabación")
        
        # Mostrar el audio grabado a la derecha
        output_audio = gr.Audio(label="Grabación de Audio", type="filepath")

        # Asignar la función al botón
        grabar_button.click(grabar_audio, outputs=output_audio)
    
    return demo

# Ejecuta la interfaz con la ruta absoluta en allowed_paths
if __name__ == "__main__":
    demo = interfaz()
    demo.launch(allowed_paths=[os.path.dirname(AUDIO_COPY_PATH)])

