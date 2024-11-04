# 2024/03/11 setup.py

import os
import subprocess
import sys
import requests    

from pathlib import Path

# Definición de las carpetas del proyecto
PROJECT_DIRECTORIES = [
    "assets",
    "assets/audio",
    "assets/video",
    "checkpoints",
    "models",
    "src",
    "src/utils",
    "tests",
    "results"
]

# URLs de las utilidades de OpenVINO Notebooks
OPENVINO_UTILS = {
    "notebook_utils.py": "https://raw.githubusercontent.com/openvinotoolkit/openvino_notebooks/latest/utils/notebook_utils.py",
    "pip_helper.py": "https://raw.githubusercontent.com/openvinotoolkit/openvino_notebooks/latest/utils/pip_helper.py"
}

# URLs de los archivos de ayuda de Wav2Lip
WAV2LIP_HELPERS = {
    "gradio_helper.py": "https://raw.githubusercontent.com/openvinotoolkit/openvino_notebooks/latest/notebooks/wav2lip/gradio_helper.py",
    "ov_inference.py": "https://raw.githubusercontent.com/openvinotoolkit/openvino_notebooks/latest/notebooks/wav2lip/ov_inference.py",
    "ov_wav2lip_helper.py": "https://raw.githubusercontent.com/openvinotoolkit/openvino_notebooks/latest/notebooks/wav2lip/ov_wav2lip_helper.py"
}

WAV2LIP_HELPERS_DIR = Path("src")
OPENVINO_UTILS_DIR = Path("src/utils")

# URLs de los archivos de ejemplo de entrada
EXAMPLE_FILES = {
    "audio_example": {
        "filename": "data_audio_sun_5s.wav",
        "url": "https://github.com/sammysun0711/openvino_aigc_samples/blob/main/Wav2Lip/data_audio_sun_5s.wav?raw=true",
        "folder": "assets/audio"
    },
    "video_example": {
        "filename": "data_video_sun_5s.mp4",
        "url": "https://github.com/sammysun0711/openvino_aigc_samples/blob/main/Wav2Lip/data_video_sun_5s.mp4?raw=true",
        "folder": "assets/video"
    }
}

# Función para crear la estructura general del proyecto
def create_project_structure():
    """
    Crea la estructura de las carpetas del proyecto
    """
    for directory in PROJECT_DIRECTORIES:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            print(f"Carpeta '{directory}' creada.")
        else:
            print(f"Carpeta '{directory}' ya existe.")

# Función para crear el entorno virtual
def create_virtual_environment():
    """
    Crea el entorno virtual si no existe.
    """
    env_path = Path("env")
    if not env_path.exists():
        print("Creando el entorno virtual...")
        subprocess.check_call([sys.executable, "-m", "venv", "env"])
        print(f"Entorno virtual creado en '{env_path}'.")
    else:
        print(f"El entorno virtual '{env_path}' ya existe.")

# Función que activa y define pip y python
def activate_virtual_environment():
    """
    Activa el entorno virtual y devuelve las rutas de pip y python.
    """
    if os.name == 'nt':  # Windows
        python_path = str(Path("env") / "Scripts" / "python.exe")
        pip_path = str(Path("env") / "Scripts" / "pip.exe")
    else:  # Unix/MacOS
        python_path = str(Path("env") / "bin" / "python")
        pip_path = str(Path("env") / "bin" / "pip")

    # Actualizar pip a la última versión en el entorno virtual usando python -m pip
    try:
        subprocess.check_call([python_path, "-m", "pip", "install", "--upgrade", "pip"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("pip actualizado a la última versión.")
    except subprocess.CalledProcessError:
        print("Error al actualizar pip.")
    try:
        subprocess.check_call([pip_path, "install", "tqdm"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Error al instalar tqdm.")

    return python_path, pip_path

# Funcion para instalar las dependencias desde requirements.txt con barra de progreso
def install_requirements(pip_path):
    """
    Instala las dependencias de requirements.txt con una barra de progreso.
    """
    print("Instalando dependencias...")
    # Instalar tqdm en el entorno virtual si no está instalado
    try:
        subprocess.check_call([pip_path, "install", "tqdm"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Error al instalar tqdm.")

    from tqdm import tqdm  # Importar tqdm para la barra de progreso    

    # Leer requirements.txt y mostrar barra de progreso
    requirements_path = Path("requirements.txt")
    if not requirements_path.exists():
        print("Archivo requirements.txt no encontrado.")
        return

    with open(requirements_path, "r") as f:
        dependencies = f.read().splitlines()

    # Instalar cada dependencia con barra de progreso
    for dependency in tqdm(dependencies, desc="Instalando dependencias", unit="paquete"):
        try:
            subprocess.check_call([pip_path, "install", dependency], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            print(f"\nError al instalar {dependency}.")
    
    print("Todas las dependencias fueron instaladas correctamente.")

# Funcion para descargar los archivos de utilidades de OpenVINO Notebooks
def download_openvino_utils(pip_path):
    """
    Descarga los archivos de utilidades de OpenVINO Notebooks en src/utils si no existen.
    """
    # Crear la carpeta de utilidades si no existe
    OPENVINO_UTILS_DIR.mkdir(parents=True, exist_ok=True)

    # Instalar requests en el entorno virtual si no está instalado
    try:
        subprocess.check_call([pip_path, "install", "requests"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Error al instalar requests.")

        # Instalar tqdm en el entorno virtual si no está instalado
    try:
        subprocess.check_call([pip_path, "install", "tqdm"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Error al instalar tqdm.")

    from tqdm import tqdm  # Importar tqdm para la barra de progreso    

    for filename, url in tqdm(OPENVINO_UTILS.items(), desc="Descargando utilidades de OpenVINO", unit="archivo"):
        file_path = OPENVINO_UTILS_DIR / filename
        if not file_path.exists():
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)
            else:
                print(f"Error al descargar {filename} desde {url}")

# Función para descargar los archivos de ayuda específicos de Wav2Lip
def download_wav2lip_helpers(pip_path):
    """
    Descarga los archivos de ayuda específicos de Wav2Lip si no existen.
    """
    WAV2LIP_HELPERS_DIR.mkdir(parents=True, exist_ok=True)  # Crea `src` si no existe

    # Instalar requests en el entorno virtual si no está instalado
    try:
        subprocess.check_call([pip_path, "install", "requests"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Error al instalar requests.")
        
    try:
        subprocess.check_call([pip_path, "install", "tqdm"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Error al instalar tqdm.")

    from tqdm import tqdm  # Importar tqdm para la barra de progreso       
    for filename, url in tqdm(WAV2LIP_HELPERS.items(), desc="Descargando ayudas de Wav2Lip", unit="archivo"):
        file_path = WAV2LIP_HELPERS_DIR / filename
        if not file_path.exists():
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)

# Función para descargar los archivos de ejemplo de entrada (audio y video)
def download_example_files():
    """
    Descarga los archivos de ejemplo de entrada (audio y video) en sus carpetas correspondientes.
    """
    # Instalar requests en el entorno virtual si no está instalado
    try:
        subprocess.check_call([pip_path, "install", "requests"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Error al instalar requests.")
    
    try:
        subprocess.check_call([pip_path, "install", "tqdm"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Error al instalar tqdm.")

    from tqdm import tqdm  # Importar tqdm para la barra de progreso         

    for example_name, example_info in tqdm(EXAMPLE_FILES.items(), desc="Descargando archivos de ejemplo", unit="archivo"):
        folder_path = Path(example_info["folder"])
        file_path = folder_path / example_info["filename"]

        # Crear la carpeta si no existe
        folder_path.mkdir(parents=True, exist_ok=True)

        # Descargar el archivo si no existe
        if not file_path.exists():
            response = requests.get(example_info["url"])
            if response.status_code == 200:
                with open(file_path, "wb") as f:
                    f.write(response.content)

def clone_wav2lip_repo():
    """
    Clona el repositorio oficial de Wav2Lip, ocultando el progreso mediante tqdm.
    """
    repo_url = "https://github.com/Rudrabha/Wav2Lip"
    clone_path = "src/Wav2Lip"

    try:
        subprocess.check_call([pip_path, "install", "requests"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Error al instalar requests.")
    
    try:
        subprocess.check_call([pip_path, "install", "tqdm"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Error al instalar tqdm.")

    from tqdm import tqdm  # Importar tqdm para la barra de progreso        
    
    # Verifica si el repositorio ya existe para evitar clonarlo nuevamente
    if os.path.exists(clone_path):
        print(f"El repositorio '{clone_path}' ya existe.")
        return

    # Inicia el proceso de clonación con tqdm para ocultar el progreso
    print("Clonando el repositorio de Wav2Lip...")
    with tqdm(total=100, desc="Clonación en progreso", ncols=100, bar_format="{l_bar}{bar}") as pbar:
        # Ejecuta el comando de clonación
        exit_code = subprocess.call(["git", "clone", repo_url, clone_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        if exit_code != 0:
            raise Exception("Error: La clonación del repositorio ha fallado.")
        else:
            pbar.update(100)
            print("Repositorio clonado exitosamente en 'Wav2Lip'.")


if __name__ == "__main__":
    create_project_structure()
    create_virtual_environment()
    python_path, pip_path = activate_virtual_environment()
    
    download_openvino_utils(pip_path)
    download_wav2lip_helpers(pip_path)
    download_example_files()
    install_requirements(pip_path)
    clone_wav2lip_repo()














