import os

from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from pathlib import Path

#Cargar variables de entorno desde el archivo .env
# Ruta relativa al archivo .env en models/
project_root = Path(__file__).resolve().parent.parent  # Sube al nivel raíz del proyecto
env_path = project_root / "models" / ".env"           # Ruta completa al archivo .env
load_dotenv(dotenv_path=env_path)

#Configuracion de la clave de la api
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("No se encontro la clave de API")

OPENAI_KEY_VAL = api_key

llm = ChatOpenAI(
    openai_api_key = OPENAI_KEY_VAL,
    temperature = 0.7,
    model = "gpt-4"
)

#plantilla del prompt con el texto leido del archivo
template ="""
Eres un asistente de IA que orienta a los alumnos a ser mejores personas. Haz una haiku de 5 lineas sobre lo que te estan comentando. Da siempre la respuesta en Español
Texto:{texto}
Respuesta:
"""
prompt = PromptTemplate(
    input_variables = ["texto"],
    template = template
)

chain = LLMChain(
    llm = llm,
    prompt = prompt
)

#def save_summary_to_file(summary_text, filename = 'response.txt'):
def save_summary_to_file(summary_text, filename = 'C:/programacionEjercicios/miwav2lipv6/results/OpenAI_response.txt'):
    try:
        with open(filename,'w', encoding='utf-8') as file:
            file.write(summary_text)
        print(f"El resumen se ha guardado exitosamente en {filename}")
    except Exception as e:
        print(f"Ocurrio un error al guardar el resumen {e}")

def read_text_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read()
    except Exception as e:
        print(f"Error al leer el archivo {filename}: {e}")
        return ""    


#def main():
def moni(archivo):
    #texto_usuario = input("Ingresa un texto para resumir:")
    #texto_usuario = read_text_from_file("C:/programacionEjercicios/miwav2lipv6/results/transcripcion.txt")
    texto_usuario = read_text_from_file(archivo)
    resultado = chain.run(texto = texto_usuario)

    #Mostrar el resumen generado
    print("\nResumen generado:")
    print(resultado)
    save_summary_to_file(resultado)

    return resultado
#


if __name__ == "__main__":
    moni()

