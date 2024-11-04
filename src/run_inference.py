import os
from ov_inference import ov_inference
import soundfile as sf
import cv2

def verificar_archivos(video_path, audio_path):
    """
    Verifica que los archivos de video y audio existen y son legibles.

    Args:
        video_path (str): Ruta del archivo de video.
        audio_path (str): Ruta del archivo de audio.

    Returns:
        bool: True si ambos archivos son legibles, False en caso contrario.
    """
    # Verificar el archivo de video
    if not os.path.exists(video_path):
        print(f"Error: El archivo de video no existe en la ruta {video_path}")
        return False
    else:
        # Intentar abrir el video
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: No se puede abrir el archivo de video en {video_path}")
            return False
        else:
            print(f"Archivo de video {video_path} está accesible.")
        cap.release()

    # Verificar el archivo de audio
    if not os.path.exists(audio_path):
        print(f"Error: El archivo de audio no existe en la ruta {audio_path}")
        return False
    else:
        try:
            # Intentar abrir el archivo de audio
            with sf.SoundFile(audio_path) as audio_file:
                print(f"Archivo de audio {audio_path} está accesible.")
        except Exception as e:
            print(f"Error al leer el archivo de audio: {e}")
            return False

    return True

# Rutas de archivos
video_path = os.path.abspath("../miwav2lipv6/assets/video/data_video_sun_5s.mp4")
#audio_path = os.path.abspath("../miwav2lipv6/assets/audio/grabacion_gradio.wav")
audio_path = os.path.abspath("../miwav2lipv6/assets/audio/audio.wav")
face_detection_path = os.path.abspath("../miwav2lipv6/models/face_detection.xml")
wav2lip_path = os.path.abspath("../miwav2lipv6/models/wav2lip.xml")
outfile = os.path.abspath("../miwav2lipv6/results/result_voice.mp4")

# Verificar archivos antes de llamar a ov_inference
if verificar_archivos(video_path, audio_path):
    ov_inference(
        video_path,
        audio_path,
        face_detection_path=face_detection_path,
        wav2lip_path=wav2lip_path,
        inference_device="CPU",
        outfile=outfile,
        resize_factor = 2,
    )
else:
    print("No se pudo proceder con la inferencia debido a problemas con los archivos.")
