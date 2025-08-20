from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from PantallaPedirDatos import pantalla_Datos

def ajustar_tamano_ventana(window, ancho_porcentaje=0.8, alto_porcentaje=0.8):
    ancho_pantalla = window.winfo_screenwidth()
    alto_pantalla = window.winfo_screenheight()
    nuevo_ancho = int(ancho_pantalla * ancho_porcentaje)
    nuevo_alto = int(alto_pantalla * alto_porcentaje)
    window.geometry(f"{nuevo_ancho}x{nuevo_alto}")

def pantalla_principal(window):
    for widget in window.winfo_children():
        widget.destroy()

    window.title("ATS")
    window.minsize(width=1200, height=500)
    window.config(padx=20, pady=20, background="#D4ADFC")

    ajustar_tamano_ventana(window)

    img = Image.open("Recursos/logobt.png")
    resized_img = img.resize((250, 200))
    img = ImageTk.PhotoImage(resized_img)

    window.logobt = Image.PhotoImage(img)

    lienzo = Canvas(window, width=200, height=200)
    lienzo.create_image(0, 0, anchor=NW, image=window.logobt)
    lienzo.grid(column=0, row=0)

    titulo1=Label(text="Selecciona la acción a realizar", font=("Montserrat", 30, "bold"), fg="#3F0850", background="#D4ADFC")
    titulo1.grid(column=1, row=0, columnspan=1, pady=(20, 20))

    boton_ats = Button(window, text="Simulador de ATS", font=("Montserrat", 20, "bold"), fg="#5C469C", background="#C197EB",
                          command=lambda: pantalla_Datos(window, pantalla_principal))
    boton_ats.grid(column=1, row=2, padx=30, pady=15)

window = Tk()
pantalla_principal(window)
window.mainloop()
