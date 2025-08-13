import PyPDF2
from PyPDF2 import PdfReader

def obter_ruta():
    return input("Ingrese la ruta del archivo a escanear: ")

def leer_archivo(inputFile):
    texto = ""
    with open(inputFile, "rb") as pdf:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            texto += page.extract_text() + "\n"
    return texto.lower()

def vacante_nombre():
    return input("Ingrese el nombre de la vacante:")

def vacante_habilidades():
    return input("Ingrese las habilidades que solicita para la vacante:")

def vacante_palabras_clave():
    return input("Ingrese las palabras calve que busca:")

def vacante_estudios():
    return input("Ingrese el nivel de estudio que busca:")

def vacante_experiencia():
    return input("Ingrese la experiencia que busca:")

def vacante_idioma():
    return input("Ingrese el idioma que busca la vacante:")

def vacante_herramientas():
    return input("Ingrese las herramientas que busca la vacante:")

def vacante():
    datos = {
        "nombre": vacante_nombre(),
        "habilidades": vacante_habilidades(),
        "palabras_clave": vacante_palabras_clave(),
        "estudios": vacante_estudios(),
        "experiencia": vacante_experiencia(),
        "idioma": vacante_idioma(),
        "herramientas": vacante_herramientas()
    }
    return datos

def resultados_busqueda(datos_vacante, texto_pdf):
    print("\nCompatibilidad de la vacante con el postulante:\n")
    for clave, valor in datos_vacante.items():
        if valor.lower() in texto_pdf:
            print(f"{clave.capitalize()} encontrado: {valor}")
        else:
            print(f"{clave.capitalize()} NO encontrado: {valor}")


info = vacante()
ruta = obter_ruta()
texto_pdf = leer_archivo(ruta)
resultados_busqueda(info, texto_pdf)

