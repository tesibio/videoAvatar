import sys
from pathlib import Path

# Añade `src` a `sys.path` para que Python encuentre el módulo `utils`
sys.path.append(str(Path(__file__).resolve().parent))

# Importa la función desde utils/notebook_utils.py
from utils.notebook_utils import download_file
from ov_wav2lip_helper import download_and_convert_models


OV_FACE_DETECTION_MODEL_PATH = Path("../miwav2lipv6/models/face_detection.xml")
OV_WAV2LIP_MODEL_PATH = Path("../miwav2lipv6/models/wav2lip.xml")


download_and_convert_models(OV_FACE_DETECTION_MODEL_PATH, OV_WAV2LIP_MODEL_PATH)
