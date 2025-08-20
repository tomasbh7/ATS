import PyPDF2
from PyPDF2 import PdfReader
import unicodedata

def normalizar(textoANormalizarxd):
    textoAMinuscula = textoANormalizarxd.lower()
    textoNormalizado = unicodedata.normalize('NFD', textoAMinuscula)
    textoSinTildes = ''.join(
        c for c in textoNormalizado
        if unicodedata.category(c) != 'Mn' or c == '̃'
    )
    return unicodedata.normalize("NFC", textoSinTildes)

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
    return normalizar(input("Ingrese el nombre de la vacante:"))

def vacante_habilidades():
    return normalizar(input("Ingrese las habilidades que solicita para la vacante:"))

def vacante_competencias():
    return normalizar(input("Ingrese las competencias que solicita para la vacante:"))

def vacante_palabras_clave():
    return normalizar(input("Ingrese las palabras clave que busca:"))

def vacante_estudios():
    return normalizar(input("Ingrese el nivel de estudio que busca:"))

def vacante_experiencia():
    return normalizar(input("Ingrese la experiencia que busca:"))

def vacante_idioma():
    return normalizar(input("Ingrese el idioma que busca la vacante:"))

def vacante_nivel_idioma():
    return normalizar(input("Ingrese el nivel de idioma que busca para la vacante:"))

def vacante_herramientas():
    return normalizar(input("Ingrese las herramientas que busca la vacante:"))

def vacante_extras():
    return normalizar(input("Ingresa cualquier dato extra que busque la vacante:"))

def vacante():
    datos = {
        "Habilidades": vacante_habilidades(),
        "Competencias": vacante_competencias(),
        "Palabras_clave": vacante_palabras_clave(), 
        "Estudios": vacante_estudios(),
        "Experiencia": vacante_experiencia(), 
        "Idioma": vacante_idioma(), 
        "Nivel del idioma": vacante_nivel_idioma(),
        "Herramientas": vacante_herramientas(), 
        "Extras" : vacante_extras()
    }
    return datos

def resultados_busqueda(datos_vacante, texto_pdf):
    print("\nCompatibilidad de la vacante con el postulante:\n")
    SiApareceList = []
    NoApareceList = []
    conteo ={}
    texto = normalizar(texto_pdf)
    for clave, valor in datos_vacante.items():
     cantidad = texto.count(valor)
     conteo[clave, valor] = cantidad
     if cantidad == 0:
      NoApareceList.append(valor)
     else:
      SiApareceList.append(valor)  
    return {
    "no_aparecen": NoApareceList,
    "si_aparecen": SiApareceList,
    "conteos": conteo
}

"""def puntaje(datos_vacante): #sistema de puntaje#
    print("\nCompatibilidad de la vacante con el postulante:\n")
    for clave, valor in datos_vacante.items():
        if valor.lower() in texto_pdf:
            #aquí metemos el sistema de puntaje en caso de q el dato necesario si esté en el cv#
        else:
            #aquí metemos el sistema de puntaje en caso de q el dato necesario no esté en el cv#
            /home/tomas/Descargas/CV_Montserrat_Guzmán.pdf
"""

info = vacante()
ruta = obter_ruta()
texto_pdf = leer_archivo(ruta)
resultados =  resultados_busqueda(info, texto_pdf)
print("Palabras que SI aparecen ",resultados["si_aparecen"])
print("Palabras que NO aparecen ",resultados["no_aparecen"])
