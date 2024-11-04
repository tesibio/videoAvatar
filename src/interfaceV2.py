# interfaceV2.py

import gradio as gr
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import shutil
import os
import subprocess
from whisper_audio_transcriber import transcribe_audio, guardar_transcripcion

# Rutas de archivos (ajustadas según la estructura especificada)
AUDIO_COPY_PATH = os.path.abspath("assets/audio/grabacion_gradio.wav")
VIDEO_PATH = os.path.abspath("assets/video/data_video_sun_5s.mp4")
TRANSCRIPTION_TEXT_PATH = os.path.abspath("results/transcripcion.txt")
RESULT_VIDEO_PATH = os.path.abspath("results/result_voice.mp4")

# Función para grabar audio
def grabar_audio(duration=8, sample_rate=44100):
    print("Grabando...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()  # Espera a que la grabación termine

    # Guardar archivo temporal de audio
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp_audio.name, sample_rate, audio_data)
    print("Grabación completada. Archivo temporal guardado en:", temp_audio.name)

    # Crear el directorio si no existe y copiar el archivo de audio grabado
    os.makedirs(os.path.dirname(AUDIO_COPY_PATH), exist_ok=True)
    shutil.copy(temp_audio.name, AUDIO_COPY_PATH)
    print(f"Copia de la grabación guardada en: {AUDIO_COPY_PATH}")

    return AUDIO_COPY_PATH, "Grabación completada."

# Función para transcribir el audio con barra de progreso
def transcribir_con_progreso(audio_path):
    progreso = gr.Progress()
    progreso(0, "Iniciando transcripción...")  # Barra al 0%
    model_name = "openai/whisper-large"
    progreso(25, "Cargando el modelo Whisper...")  # Barra al 25%

    # Realiza la transcripción
    transcripcion = transcribe_audio(audio_path, model_name)
    progreso(75, "Guardando la transcripción...")  # Barra al 75%
    
    # Guarda la transcripción en results/transcripcion.txt
    guardar_transcripcion(transcripcion, filename="transcripcion.txt", directory="results")
    progreso(100, "Transcripción completada.")  # Barra al 100%
    
    return transcripcion

# Función para procesar video y audio usando run_inference.py
def procesar_video_audio():
    """
    Ejecuta run_inference.py para sincronizar el video y el audio y guardar el resultado en result_voice.mp4.
    """
    print("Iniciando procesamiento de video y audio...")
    # Ejecutar run_inference.py como un subproceso para procesar video y audio
    subprocess.run(["python", "run_inference.py"])
    print(f"Video procesado guardado en: {RESULT_VIDEO_PATH}")
    return RESULT_VIDEO_PATH

# Configuración de la interfaz de Gradio
def interfaz():
    with gr.Blocks() as demo:
        with gr.Row():
            # Columna izquierda para entradas
            with gr.Column():
                gr.Video(VIDEO_PATH, loop=True, autoplay=True, height=300, width=500)
                grabar_button = gr.Button("Iniciar Grabación de Audio")
                estado_grabacion = gr.Textbox(label="Estado de la Grabación", interactive=False)

            # Columna derecha para salidas
            with gr.Column():
                output_audio = gr.Audio(AUDIO_COPY_PATH, label="Audio Grabado", interactive=False)
                video_resultado = gr.Video(label="Video Procesado", interactive=False)
                texto_transcripcion = gr.Textbox(label="Texto Transcrito")
                progreso_transcripcion = gr.Textbox(label="Estado de Transcripción", interactive=False)

            # Flujo completo: grabación, transcripción y procesamiento de video
            def flujo_completo():
                # Grabar el audio
                _, mensaje_grabacion = grabar_audio()
                
                # Transcribir el audio con progreso
                transcripcion = transcribir_con_progreso(AUDIO_COPY_PATH)
                
                # Procesar video y audio grabado para sincronización de labios
                video_path = procesar_video_audio()
                
                return mensaje_grabacion, AUDIO_COPY_PATH, transcripcion, video_path

            grabar_button.click(
                flujo_completo, 
                outputs=[estado_grabacion, output_audio, texto_transcripcion, video_resultado]
            )

    return demo

# Ejecuta la interfaz
if __name__ == "__main__":
    demo = interfaz()
    demo.launch(allowed_paths=["assets", "results"])
