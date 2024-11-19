# interfaceV2.py

import gradio as gr
import sounddevice as sd
from scipy.io.wavfile import write
import tempfile
import shutil
import os
import subprocess
import sys
from whisper_audio_transcriber import transcribe_audio, guardar_transcripcion

# Paths to files (adjusted as per your specified structure)
AUDIO_RECORD_PATH = os.path.abspath("C:/programacionEjercicios/miwav2lipv6/assets/audio/grabacion_gradio.wav")
#VIDEO_PATH = os.path.abspath("C:/programacionEjercicios/miwav2lipv6/assets/video/data_video_sun_5s.mp4")
VIDEO_PATH = os.path.abspath("C:/programacionEjercicios/miwav2lipv6/assets/video/data_video_sun.mp4")
TRANSCRIPTION_TEXT_PATH = os.path.abspath("C:/programacionEjercicios/miwav2lipv6/results/transcripcion.txt")
RESULT_AUDIO_TEMP_PATH = os.path.abspath( "C:/programacionEjercicios/miwav2lipv6/results/audiov2.wav")
RESULT_AUDIO_FINAL_PATH = os.path.abspath("C:/programacionEjercicios/miwav2lipv6/assets/audio/audio.wav")
RESULT_VIDEO_PATH = os.path.abspath("C:/programacionEjercicios/miwav2lipv6/results/result_voice.mp4")
TEXT_TO_SPEECH_PATH = os.path.abspath("C:/programacionEjercicios/miwav2lipv6/src/text_to_speech.py")

# Function to record 8-second audio
def grabar_audio(duration=8, sample_rate=44100):
    print("Starting recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    print(f"Recording in progress for {duration} seconds...")
    sd.wait()
    print("Recording completed.")

    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(temp_audio.name, sample_rate, audio_data)
    print("Audio temporarily saved at:", temp_audio.name)
    temp_audio.close()  # Asegúrate de cerrarlo antes de usarlo
    os.makedirs(os.path.dirname(AUDIO_RECORD_PATH), exist_ok=True)
    shutil.copy(temp_audio.name, AUDIO_RECORD_PATH)
    print(f"Recording copied to: {AUDIO_RECORD_PATH}")

    return AUDIO_RECORD_PATH, "Recording completed."

# Function to transcribe audio with Whisper
def transcribir_con_progreso(audio_path):
    progreso = gr.Progress()
    progreso(0, "Starting transcription...")
    model_name = "openai/whisper-large"
    progreso(25, "Loading Whisper model...")

    transcripcion = transcribe_audio(audio_path, model_name)
    progreso(75, "Saving transcription...")
    guardar_transcripcion(transcripcion, filename=TRANSCRIPTION_TEXT_PATH)
    progreso(100, "Transcription completed.")
    if not os.path.exists(TRANSCRIPTION_TEXT_PATH):
        raise FileNotFoundError(f"El archivo {TRANSCRIPTION_TEXT_PATH} no se generó.")

    return transcripcion

# Function to convert text to audio using text_to_speech.py
def generar_audio_desde_texto():
    print("Generating audio from text...")
    result = subprocess.run(
        [sys.executable, TEXT_TO_SPEECH_PATH],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"Error ejecutando text_to_speech.py: {result.stderr}")
    if result.stdout:
        print("Output:", result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

    if os.path.exists(RESULT_AUDIO_TEMP_PATH):
        print(f"Temporary audio generated at: {RESULT_AUDIO_TEMP_PATH}")
        
        os.makedirs(os.path.dirname(RESULT_AUDIO_FINAL_PATH), exist_ok=True)
        shutil.copy(RESULT_AUDIO_TEMP_PATH, RESULT_AUDIO_FINAL_PATH)
        print(f"Final audio copied to: {RESULT_AUDIO_FINAL_PATH}")

        return RESULT_AUDIO_FINAL_PATH
    else:
        print(f"Error: Audio file was not generated in {RESULT_AUDIO_FINAL_PATH} ")
        return None

# Function to process video and audio using run_inference.py with the generated audio file
def procesar_video_audio():
    print("Starting video and audio processing...")
    run_inference_path = os.path.abspath("C:/programacionEjercicios/miwav2lipv6/src/run_inference.py")

    result = subprocess.run(
        [sys.executable, run_inference_path, "--audio", RESULT_AUDIO_FINAL_PATH, "--video", VIDEO_PATH],
        capture_output=True,
        text=True
    )

    if result.stdout:
        print("Output:", result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)

    if os.path.exists(RESULT_VIDEO_PATH):
        print(f"Processed video saved at: {RESULT_VIDEO_PATH}")
        return RESULT_VIDEO_PATH
    else:
        print("Error: Video file was not generated at 'results/result_voice.mp4'")
        return None

# Gradio Interface Configuration
def interfaz():
    with gr.Blocks() as demo:
        with gr.Row():
            with gr.Column():
                gr.Video(VIDEO_PATH, loop=True, autoplay=True, height=300, width=500)
                grabar_button = gr.Button("Start Audio Recording")
                estado_grabacion = gr.Textbox(label="Recording Status", interactive=False)

            with gr.Column():
                output_audio = gr.Audio(AUDIO_RECORD_PATH, label="Recorded Audio", interactive=False)
                output_audio_speech = gr.Audio(RESULT_AUDIO_FINAL_PATH, label="Generated Audio from Text", interactive=False)
                video_resultado = gr.Video(label="Processed Video", interactive=False)
                texto_transcripcion = gr.Textbox(label="Transcribed Text")
                progreso_transcripcion = gr.Textbox(label="Transcription Status", interactive=False)

            # Full flow: recording, transcription, text-to-speech, and video processing
            """
            def flujo_completo():
                _, mensaje_grabacion = grabar_audio()
                transcripcion = transcribir_con_progreso(AUDIO_RECORD_PATH)
                audio_generado = generar_audio_desde_texto()
                video_path = procesar_video_audio()

                # Ensure function always returns 5 outputs for Gradio, even in error cases
                if video_path and audio_generado:
                    return mensaje_grabacion, AUDIO_RECORD_PATH, transcripcion, audio_generado, video_path
                else:
                    return mensaje_grabacion, AUDIO_RECORD_PATH, transcripcion, audio_generado or "Audio generation failed", video_path or "Video generation failed"
            """
            def flujo_completo():
                try:
                    print("Inicio del flujo completo...")
                    # Grabar audio
                    audio_path, mensaje_grabacion = grabar_audio()
                    print("Audio grabado en:", audio_path)
                    # Transcribir audio
                    transcripcion = transcribir_con_progreso(audio_path)
                    print("Transcripción completada:", transcripcion)
                    # Generar audio desde texto
                    audio_generado = generar_audio_desde_texto()
                    print("Audio generado:", audio_generado)
                    # Procesar video y audio
                    video_path = procesar_video_audio()
                    print("Video procesado en:", video_path)
                    # Devolver resultados si todo fue exitoso
                    return mensaje_grabacion, audio_path, transcripcion, audio_generado, video_path
                except Exception as e:
                    # Imprime el error en la terminal y regresa mensajes de error a la interfaz
                    print("Error detectado en flujo completo:", str(e))
                    return (
                        "Error durante el flujo completo",
                        None,  # Audio grabado
                        f"Error: {str(e)}",  # Transcripción
                        None,  # Audio generado
                        None   # Video procesado
                            )

            grabar_button.click(
                flujo_completo,
                outputs=[estado_grabacion, output_audio, texto_transcripcion, output_audio_speech, video_resultado]
            )

    return demo

if __name__ == "__main__":
    demo = interfaz()
    demo.launch(allowed_paths=["C:/programacionEjercicios/miwav2lipv6/assets", "C:/programacionEjercicios/miwav2lipv6/results"])
