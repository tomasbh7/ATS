import PyPDF2
from PyPDF2 import PdfReader
import unicodedata
inputFile = "/home/ayumu/Downloads/CV_Montserrat_Guzmán.pdf"
pdf = open(inputFile, "rb")
pdf_reader = PyPDF2.PdfReader(pdf)
page = pdf_reader.pages[0]
texto = (page.extract_text())

def normalizar(textoANormalizarxd):
    textoAMinuscula = textoANormalizarxd.lower()
    textoNormalizado = unicodedata.normalize('NFD', textoAMinuscula)
    textoSinTildes = ''.join(
        c for c in textoNormalizado
        if unicodedata.category(c) != 'Mn' or c == '̃'
    )
    return unicodedata.normalize("NFC", textoSinTildes)

def buscar_palabras(textoAtrabajar, palabras_a_buscar):
  SiApareceList = []
  NoApareceList = []
  conteo ={}
  texto = normalizar(textoAtrabajar)
  for palabra in palabras_a_buscar:
    cantidad = texto.count(palabra)
    conteo[palabra] = cantidad
    if cantidad == 0:
        NoApareceList.append(palabra)
    else:
        SiApareceList.append(palabra)  
  return {
    "no_aparecen": NoApareceList,
    "si_aparecen": SiApareceList,
    "conteos": conteo
}

palabras_a_buscar = []
num_palabras = int(input("Ingrese la cantidad de palabras a buscar: "))
for i in range(num_palabras):
  palabra = normalizar(input(f"Ingrese la palabra {i+1}: "))
  palabras_a_buscar.append(palabra)

resultado = buscar_palabras(texto, palabras_a_buscar)
print("Palabras que SÍ aparecen:", resultado["si_aparecen"])
print("Palabras que NO aparecen:", resultado["no_aparecen"])



