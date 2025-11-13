import os
from tkinter import *

dir_base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
carpeta_img = os.path.join(dir_base, 'Estatico', 'Img')

def ajustar_tamano_ventana(window, ancho_porcentaje=0.8, alto_porcentaje=0.8):
    """
     Ajusta el tamaño de la ventana en función de un porcentaje de la resolución de la pantalla.

    Args:
        window (Tk): La ventana de la aplicación.
        ancho_porcentaje (float): El porcentaje del ancho de la pantalla que ocupará la ventana.
        alto_porcentaje (float): El porcentaje del alto de la pantalla que ocupará la ventana.
    """
    ancho_pantalla = window.winfo_screenwidth()
    alto_pantalla = window.winfo_screenheight()
    nuevo_ancho = int(ancho_pantalla * ancho_porcentaje)
    nuevo_alto = int(alto_pantalla * alto_porcentaje)
    window.geometry(f"{nuevo_ancho}x{nuevo_alto}")

def pantalla_principal(window):
    """
     Define la interfaz de la pantalla principal de la aplicación de consulta de clima, incluyendo la entrada de datos y los botones de navegación.

    Args:
        window (Tk): La ventana principal donde se colocarán los elementos.
    """
    for widget in window.winfo_children():
        widget.destroy()

    window.title("Consulta de clima")
    window.minsize(width=100, height=700)
    window.config(padx=20, pady=20)

    ajustar_tamano_ventana(window)

    lienzo = Canvas(window, width=200, height=200) 
    window.logoaeropuerto = PhotoImage(file=os.path.join(carpeta_img, 'logobt.png'))
    lienzo.create_image(100, 100, image=window.logoaeropuerto)
    lienzo.grid(column=0, row=0)

    titulo1 = Label(text="ATS", font=("Montserrat", 40, "bold"), fg="#011640") 
    titulo1.grid(column=1, row=0)

    titulo2 = Label(window, text="Introduzca los datos de entrada de la vacante", font=("Montserrat", 20, "bold"), fg="#3CA6A6")
    titulo2.grid(column=1, row=1, padx=50, pady=30, sticky="n")

    Pedir_datos = Label(window, text="Datos:", font=("Montserrat", 15, "bold"), fg="#026773")
    Pedir_datos.grid(column=0, row=2, pady=15)
    
    Datos_entrada = Entry(window, width=20, font=("Montserrat", 12))
    Datos_entrada.grid(column=1, row=2)

    mensaje_invalido = Label(window, text="", font=("Montserrat", 15), fg="red")
    mensaje_invalido.grid(column=0, row=3, columnspan=2)
