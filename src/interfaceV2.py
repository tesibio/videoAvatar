# interfaceV2.py

import gradio as gr
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import shutil
import os
import subprocess
from whisper_audio_transcriber import transcribe_audio, guardar_transcripcion

# Rutas de archivos (ajustadas según la estructura especificada en miwav2lipv6)
AUDIO_COPY_PATH = os.path.abspath("../miwav2lipv6/assets/audio/grabacion_gradio.wav")
VIDEO_PATH = os.path.abspath("../miwav2lipv6/assets/video/data_video_sun_5s.mp4")
TRANSCRIPTION_TEXT_PATH = os.path.abspath("../miwav2lipv6/results/transcripcion.txt")
RESULT_VIDEO_PATH = os.path.abspath("../miwav2lipv6/results/result_voice.mp4")

# Función para grabar audio de 8 segundos
def grabar_audio(duration=8, sample_rate=44100):
    print("Iniciando grabación...")

    # Configurar y comenzar la grabación con duración especificada
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    print(f"Grabación en curso por {duration} segundos...")
    
    # Esperar a que la grabación termine antes de avanzar
    sd.wait()
    print("Grabación completada.")

    # Guardar el archivo de audio en una ubicación temporal
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp_audio.name, sample_rate, audio_data)
    print("Archivo de audio guardado temporalmente en:", temp_audio.name)

    # Mover el archivo de audio a la carpeta de destino en assets/audio
    os.makedirs(os.path.dirname(AUDIO_COPY_PATH), exist_ok=True)
    shutil.copy(temp_audio.name, AUDIO_COPY_PATH)
    print(f"Copia de la grabación guardada en: {AUDIO_COPY_PATH}")

    return AUDIO_COPY_PATH, "Grabación completada."

# Función para transcribir el audio con Whisper
def transcribir_con_progreso(audio_path):
    """
    Transcribe el audio con Whisper y muestra una barra de progreso en Gradio.

    Args:
        audio_path (str): Ruta del archivo de audio a transcribir.
    """
    progreso = gr.Progress()
    progreso(0, "Iniciando transcripción...")  # Progreso al 0%
    model_name = "openai/whisper-large"
    progreso(25, "Cargando el modelo Whisper...")  # Progreso al 25%

    # Realizar la transcripción usando Whisper
    transcripcion = transcribe_audio(audio_path, model_name)
    progreso(75, "Guardando la transcripción...")  # Progreso al 75%

    # Guardar la transcripción en results/transcripcion.txt
    guardar_transcripcion(transcripcion, filename="transcripcion.txt", directory="../results")
    progreso(100, "Transcripción completada.")  # Progreso al 100%

    return transcripcion

# Función para procesar video y audio usando run_inference.py
def procesar_video_audio():
    """
    Ejecuta run_inference.py para sincronizar el video y el audio y guardar el resultado en result_voice.mp4.
    """
    print("Iniciando procesamiento de video y audio...")

    # Ruta correcta a run_inference.py
    run_inference_path = os.path.abspath("../miwav2lipv6/src/run_inference.py")

    # Ejecutar run_inference.py como un subproceso
    result = subprocess.run(
        ["python", run_inference_path],
        capture_output=True,
        text=True
    )

    # Mostrar cualquier salida o error de run_inference.py en la consola
    if result.stdout:
        print("Salida:", result.stdout)
    if result.stderr:
        print("Errores:", result.stderr)

    # Verificar que el video de salida se haya generado correctamente
    if os.path.exists(RESULT_VIDEO_PATH):
        print(f"Video procesado guardado en: {RESULT_VIDEO_PATH}")
        return RESULT_VIDEO_PATH
    else:
        print("Error: No se generó el archivo de video en 'results/result_voice.mp4'")
        return None

# Configuración de la interfaz de Gradio
def interfaz():
    """
    Configura la interfaz de Gradio, que incluye botones de grabación y reproducción de audio y video.
    """
    with gr.Blocks() as demo:
        with gr.Row():
            # Columna izquierda para entradas
            with gr.Column():
                # Mostrar el video en bucle
                gr.Video(VIDEO_PATH, loop=True, autoplay=True, height=300, width=500)
                grabar_button = gr.Button("Iniciar Grabación de Audio")
                estado_grabacion = gr.Textbox(label="Estado de la Grabación", interactive=False)

            # Columna derecha para salidas
            with gr.Column():
                # Mostrar el audio grabado y la transcripción
                output_audio = gr.Audio(AUDIO_COPY_PATH, label="Audio Grabado", interactive=False)
                video_resultado = gr.Video(label="Video Procesado", interactive=False)
                texto_transcripcion = gr.Textbox(label="Texto Transcrito")
                progreso_transcripcion = gr.Textbox(label="Estado de Transcripción", interactive=False)

            # Flujo completo: grabación, transcripción y procesamiento de video
            def flujo_completo():
                # Paso 1: Grabar el audio
                _, mensaje_grabacion = grabar_audio()

                # Paso 2: Transcribir el audio
                transcripcion = transcribir_con_progreso(AUDIO_COPY_PATH)

                # Paso 3: Procesar el video y sincronizar con el audio grabado
                video_path = procesar_video_audio()

                # Devolver los resultados a la interfaz de Gradio
                if video_path:
                    return mensaje_grabacion, AUDIO_COPY_PATH, transcripcion, video_path
                else:
                    return mensaje_grabacion, AUDIO_COPY_PATH, transcripcion, "Error: No se generó el video."

            # Configurar el botón de grabación para ejecutar flujo_completo
            grabar_button.click(
                flujo_completo,
                outputs=[estado_grabacion, output_audio, texto_transcripcion, video_resultado]
            )

    return demo

# Paso 6: Ejecutar la interfaz de Gradio
if __name__ == "__main__":
    demo = interfaz()
    demo.launch(allowed_paths=["../assets", "../results"])
