import os
import pytest
from src.whisper_audio_extractor import record_audio, transcribe_audio, AUDIO_PATH

def test_record_audio():
    """
    Verifica que la función de grabación crea un archivo de audio con un tamaño válido.
    """
    # Ejecuta la grabación con una duración de prueba corta
    record_audio(duration=2)  # Graba por 2 segundos para el test
    
    # Comprueba si el archivo de audio existe
    assert os.path.exists(AUDIO_PATH), "El archivo de audio no fue creado."

    # Comprueba que el archivo no esté vacío
    assert os.path.getsize(AUDIO_PATH) > 0, "El archivo de audio está vacío."

def test_transcribe_audio():
    """
    Verifica que la función de transcripción devuelve texto.
    """
    # Ejecuta la transcripción del audio grabado
    transcription = transcribe_audio()
    
    # Asegura que se obtuvo texto
    assert isinstance(transcription, str) and len(transcription) > 0, "La transcripción está vacía o no es texto."

if __name__ == "__main__":
    pytest.main()
