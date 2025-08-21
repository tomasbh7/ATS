import os
from tkinter import *
from PIL import Image, ImageTk

def pantalla_Datos(window):
    for widget in window.winfo_children():
        widget.destroy()
    
    window.title("Datos")

    window.geometry("1200x600")
    window.minsize(width=800, height=800)
    window.config(padx=20, pady=20)

    img = Image.open("Recursos/logobt.png")
    resized_img = img.resize((250, 200))
    img = ImageTk.PhotoImage(resized_img)
    window.logobt = img

    lienzo = Canvas(window, width=200, height=200)
    lienzo.create_image(0, 0, anchor=NW, image=window.logobt)
    lienzo.grid(column=0, row=0)

    titulo1 = Label(window, text="ATS", font=("Montserrat", 80, "bold"), fg="#3F0850")
    titulo1.grid(column=1, row=0, pady=20, sticky="w")

    titulo2 = Label(window, text="Rellene los siguientes datos", font=("Montserrat", 20, "bold"), fg="#3F0850",  background="#D4ADFC")
    titulo2.grid(column=0, row=1, columnspan=3, padx=150, pady=50, sticky="n")

    vacante = Label(window, text="Nombre de la vacante:", font=("Montserrat", 12, "bold"), fg="#3F0850", background="#D4ADFC")
    vacante.grid(column=0, row=2, padx=(0, 10), pady=15)
    entradaVacante = Entry(window, width=20, font=("Montserrat", 15))
    entradaVacante.grid(column=1, row=2)

    habilidades = Label(window, text="Ingrese las habilidades requeridas para la vacante:", font=("Montserrat", 12, "bold"), fg="#3F0850", background="#D4ADFC")
    habilidades.grid(column=0, row=3, padx=(0, 10), pady=15)
    habilidades_entrada = Entry(window, width=20, font=("Montserrat", 15))
    habilidades_entrada.grid(column=1, row=3)

    competencias = Label(window, text="Ingrese las competencias requeridas para la vacante:", font=("Montserrat", 12, "bold"), fg="#3F0850",  background="#D4ADFC")
    competencias.grid(column=0, row=5, padx=(0, 10), pady=15)
    competencias_entrada = Entry(window, width=20, font=("Montserrat", 15))
    competencias_entrada.grid(column=1, row=5)

    palabras_clave = Label(window, text="Ingrese las palabras clave que busca para la vacante:", font=("Montserrat", 12, "bold"), fg="#3F0850",  background="#D4ADFC")
    palabras_clave.grid(column=0, row=6, padx=(0, 10), pady=15)
    palabras_clave_entrada = Entry(window, width=20, font=("Montserrat", 15))
    palabras_clave_entrada.grid(column=1, row=6)

    estudios = Label(window, text="Ingrese el nivel de estudios que busca para la vacante:", font=("Montserrat", 12, "bold"), fg="#3F0850",  background="#D4ADFC")
    estudios.grid(column=0, row=7, padx=(0, 10), pady=15)
    estudios_entrada = Entry(window, width=20, font=("Montserrat", 15))
    estudios_entrada.grid(column=1, row=7)

    experiencia = Label(window, text="Ingrese la experiencia que busca para la vacante:", font=("Montserrat", 12, "bold"), fg="#3F0850",  background="#D4ADFC")
    experiencia.grid(column=0, row=8, padx=(0, 10), pady=15)
    experiencia_entrada = Entry(window, width=20, font=("Montserrat", 15))
    experiencia_entrada.grid(column=1, row=8)

    idioma = Label(window, text="Ingrese el idioma que busca para la vacante:", font=("Montserrat", 12, "bold"), fg="#3F0850",  background="#D4ADFC")
    idioma.grid(column=0, row=9, padx=(0, 10), pady=15)
    idioma_entrada = Entry(window, width=20, font=("Montserrat", 15))
    idioma_entrada.grid(column=1, row=9)

    herramientas = Label(window, text="Ingrese las herramientas que busca para la vacante:", font=("Montserrat", 12, "bold"), fg="#3F0850",  background="#D4ADFC")
    herramientas.grid(column=0, row=10, padx=(0, 10), pady=15)
    herramientas_entrada = Entry(window, width=20, font=("Montserrat", 15))
    herramientas_entrada.grid(column=1, row=10)

    datos_extra = Label(window, text="Ingrese cualquier dato extra que busque para la vacante:", font=("Montserrat", 12, "bold"), fg="#3F0850", background="#D4ADFC")
    datos_extra.grid(column=0, row=11, padx=(0, 10), pady=15)
    datos_extra_entrada = Entry(window, width=20, font=("Montserrat", 15))
    datos_extra_entrada.grid(column=1, row=11)

    mensaje_invalido = Label(window, text="", font=("Montserrat", 20), fg="red")
    mensaje_invalido.grid(column=0, row=12, columnspan=2)

    BotonSiguiente = PhotoImage(file="Recursos/next.png").subsample(2, 2)
    window.boton_siguiente_imagen = BotonSiguiente
    """siguiente = Button(window, image=BotonSiguiente, borderwidth=0, command=lambda: validar_ticket(window, Ticket_entrada, mensaje_invalido))
    siguiente.grid(column=1, row=7, pady=50)
    """

    BotonRegreso = PhotoImage(file="Recursos/back.png").subsample(2, 2)
    window.boton_regreso_imagen = BotonRegreso
    """regreso = Button(window, image=BotonRegreso, borderwidth=0, command=lambda: pantalla_principal(window))
    regreso.grid(column=0, row=7, pady=50)
    """

    window.mainloop()