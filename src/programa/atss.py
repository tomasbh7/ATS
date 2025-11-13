import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import PyPDF2
from PyPDF2 import PdfReader
import unicodedata
import pickle
import os
from datetime import datetime
import re

# Configurar apariencia
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def normalizar(texto):
    if texto is None:
        return ""
    texto_minuscula = texto.lower()
    texto_normalizado = unicodedata.normalize('NFD', texto_minuscula)
    texto_sin_tildes = ''.join(
        c for c in texto_normalizado
        if unicodedata.category(c) != 'Mn'
    )
    return unicodedata.normalize("NFC", texto_sin_tildes)

class AlmacenamientoATS:
    def __init__(self, archivo_datos="ats_data.data"):
        self.archivo_datos = archivo_datos
        self.datos = self.cargar_datos()
    
    def cargar_datos(self):
        if os.path.exists(self.archivo_datos):
            try:
                with open(self.archivo_datos, 'rb') as f:
                    return pickle.load(f)
            except:
                return {"vacantes": {}, "cvs": {}}
        return {"vacantes": {}, "cvs": {}}
    
    def guardar_datos(self):
        with open(self.archivo_datos, 'wb') as f:
            pickle.dump(self.datos, f)
    
    def agregar_vacante(self, nombre, datos_vacante):
        self.datos["vacantes"][nombre] = {
            'datos': datos_vacante,
            'cvs_asociados': [],
            'fecha_creacion': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.guardar_datos()
    
    def agregar_cv(self, nombre_cv, texto_cv, ruta_archivo, vacante_asociada=None):
        self.datos["cvs"][nombre_cv] = {
            'texto': texto_cv,
            'ruta': ruta_archivo,
            'vacante_asociada': vacante_asociada,
            'fecha_agregado': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        if vacante_asociada and vacante_asociada in self.datos["vacantes"]:
            if nombre_cv not in self.datos["vacantes"][vacante_asociada]['cvs_asociados']:
                self.datos["vacantes"][vacante_asociada]['cvs_asociados'].append(nombre_cv)
        
        self.guardar_datos()
    
    def listar_vacantes(self):
        return list(self.datos["vacantes"].keys())
    
    def listar_cvs(self, vacante=None):
        if vacante and vacante in self.datos["vacantes"]:
            return self.datos["vacantes"][vacante]['cvs_asociados']
        return list(self.datos["cvs"].keys())
    
    def obtener_vacante(self, nombre):
        return self.datos["vacantes"].get(nombre)
    
    def obtener_cv(self, nombre):
        return self.datos["cvs"].get(nombre)
    
    def asociar_cv_vacante(self, nombre_cv, nombre_vacante):
        if nombre_cv in self.datos["cvs"] and nombre_vacante in self.datos["vacantes"]:
            if nombre_cv not in self.datos["vacantes"][nombre_vacante]['cvs_asociados']:
                self.datos["vacantes"][nombre_vacante]['cvs_asociados'].append(nombre_cv)
                self.datos["cvs"][nombre_cv]['vacante_asociada'] = nombre_vacante
                self.guardar_datos()
                return True
        return False

def leer_archivo_pdf(inputFile):
    texto = ""
    try:
        with open(inputFile, "rb") as pdf:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                texto += page.extract_text() + "\n"
        return texto.lower()
    except Exception as e:
        print(f"Error leyendo PDF: {e}")
        return ""

def comparar_niveles_idioma(nivel_vacante, nivel_cv):
    niveles = {
        "principiante": 1,
        "intermedio": 2,
        "avanzado": 3
    }
    nivel_v = niveles.get(nivel_vacante.lower(), 0)
    nivel_c = niveles.get(nivel_cv.lower(), 0)
    return nivel_c >= nivel_v

def comparar_estudios(estudio_vacante, estudio_cv):
    niveles_educativos = {
        "licenciatura": 1,
        "maestria": 2,
        "master": 2,
        "doctorado": 3,
        "phd": 3
    }
    
    patron_semestre = r'(\d+)(?:°|º|o|°|\.?)\s*semestre'
    semestre_vacante = re.search(patron_semestre, estudio_vacante)
    semestre_cv = re.search(patron_semestre, estudio_cv)
    
    if semestre_vacante and semestre_cv:
        sem_v = int(semestre_vacante.group(1))
        sem_c = int(semestre_cv.group(1))
        return sem_c >= sem_v
    elif semestre_vacante and not semestre_cv:
        for nivel, valor in niveles_educativos.items():
            if nivel in estudio_cv.lower() and valor >= 2:
                return True
        return False
    
    valor_v = 0
    valor_c = 0
    
    for nivel, valor in niveles_educativos.items():
        if nivel in estudio_vacante.lower():
            valor_v = valor
            break
    
    for nivel, valor in niveles_educativos.items():
        if nivel in estudio_cv.lower():
            valor_c = valor
            break
    
    if valor_v == 0 and "licenciatura" in estudio_vacante.lower():
        valor_v = 1
    if valor_c == 0 and "licenciatura" in estudio_cv.lower():
        valor_c = 1
    
    return valor_c >= valor_v

class ATSApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Sistema ATS - Tracking de Postulantes")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        
        self.almacenamiento = AlmacenamientoATS()
        
        self.crear_interfaz()
        
    def crear_interfaz(self):
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.tab_vacantes = self.tabview.add("Vacantes")
        self.tab_cvs = self.tabview.add("CVs")
        self.tab_evaluacion = self.tabview.add("Evaluacion")
        self.tab_resultados = self.tabview.add("Resultados")
        
        self.crear_tab_vacantes()
        self.crear_tab_cvs()
        self.crear_tab_evaluacion()
        self.crear_tab_resultados()
    
    def validar_solo_numeros(self, text):
        """Valida que solo se ingresen números"""
        if text == "":
            return True
        try:
            int(text)
            return True
        except ValueError:
            return False
    
    def actualizar_campo_semestre(self, choice=None):
        """Muestra u oculta el campo de semestre según la selección"""
        if self.estudios_var.get() == "licenciatura":
            self.entry_semestre.pack(side="left", padx=5)
            self.label_semestre.pack(side="left", padx=5)
        else:
            self.entry_semestre.pack_forget()
            self.label_semestre.pack_forget()
            self.entry_semestre.delete(0, tk.END)
    
    def crear_tab_vacantes(self):
        main_frame = ctk.CTkFrame(self.tab_vacantes)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_label = ctk.CTkLabel(main_frame, text="Gestion de Vacantes", 
                                 font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)
        
        form_frame = ctk.CTkScrollableFrame(main_frame)
        form_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        campos = [
            ("Nombre de la vacante:", "entry_nombre", "Ej: Reclutador"),
            ("Habilidades:", "entry_habilidades", "Ej: capacitacion, planeacion, entrevista"),
            ("Competencias:", "entry_competencias", "Ej: trabajo en equipo, adaptabilidad"),
            ("Palabras clave:", "entry_palabras_clave", "capacitacion, trabajo en equipo"),
            ("Experiencia:", "entry_experiencia", "Ej: entrevista, reclutamiento"),
            ("Herramientas:", "entry_herramientas", "Ej: Office, outlook, whatsapp"),
            ("Extras:", "entry_extras", "Ej: presencial")
        ]
        
        self.campos_vacante = {}
        for texto, key, placeholder in campos:
            frame = ctk.CTkFrame(form_frame)
            frame.pack(fill="x", padx=10, pady=5)
            
            label = ctk.CTkLabel(frame, text=texto, width=150)
            label.pack(side="left", padx=5)
            
            entry = ctk.CTkEntry(frame, placeholder_text=placeholder)
            entry.pack(side="left", fill="x", expand=True, padx=5)
            
            self.campos_vacante[key] = entry
        
        estudios_frame = ctk.CTkFrame(form_frame)
        estudios_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(estudios_frame, text="Estudios:", width=150).pack(side="left", padx=5)
        
        self.estudios_var = ctk.StringVar(value="licenciatura")
        estudios_opciones = ["licenciatura", "maestria", "doctorado"]
        self.combo_estudios = ctk.CTkComboBox(estudios_frame, values=estudios_opciones,
                                            variable=self.estudios_var,
                                            command=self.actualizar_campo_semestre)
        self.combo_estudios.pack(side="left", padx=5)
        
        # Registrar validación para solo números
        vcmd = (self.register(self.validar_solo_numeros), '%P')
        self.entry_semestre = ctk.CTkEntry(estudios_frame, 
                                          placeholder_text="Ej: 5 (solo número)",
                                          validate="key", 
                                          validatecommand=vcmd,
                                          width=80)
        
        self.label_semestre = ctk.CTkLabel(estudios_frame, text="semestre")
        
        idioma_frame = ctk.CTkFrame(form_frame)
        idioma_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(idioma_frame, text="Idioma:", width=150).pack(side="left", padx=5)
        self.entry_idioma = ctk.CTkEntry(idioma_frame, placeholder_text="Ej: ingles")
        self.entry_idioma.pack(side="left", padx=5)
        
        ctk.CTkLabel(idioma_frame, text="Nivel:").pack(side="left", padx=5)
        self.nivel_idioma_var = ctk.StringVar(value="intermedio")
        nivel_opciones = ["principiante", "intermedio", "avanzado"]
        self.combo_nivel_idioma = ctk.CTkComboBox(idioma_frame, values=nivel_opciones,
                                                variable=self.nivel_idioma_var)
        self.combo_nivel_idioma.pack(side="left", padx=5)
        
        button_frame = ctk.CTkFrame(form_frame)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        btn_crear = ctk.CTkButton(button_frame, text="Crear Vacante", 
                                command=self.crear_vacante)
        btn_crear.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(button_frame, text="Limpiar Campos", 
                                  command=self.limpiar_campos_vacante)
        btn_limpiar.pack(side="left", padx=5)
        
        lista_frame = ctk.CTkFrame(main_frame)
        lista_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        label_lista = ctk.CTkLabel(lista_frame, text="Vacantes Existentes",
                                 font=ctk.CTkFont(weight="bold"))
        label_lista.pack(pady=5)
        
        self.lista_vacantes = tk.Listbox(lista_frame, height=8)
        self.lista_vacantes.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.actualizar_lista_vacantes()
    
    def crear_tab_cvs(self):
        main_frame = ctk.CTkFrame(self.tab_cvs)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_label = ctk.CTkLabel(main_frame, text="Gestion de CVs", 
                                 font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)
        
        upload_frame = ctk.CTkFrame(main_frame)
        upload_frame.pack(fill="x", padx=20, pady=10)
        
        file_frame = ctk.CTkFrame(upload_frame)
        file_frame.pack(fill="x", padx=10, pady=5)
        
        self.label_archivo = ctk.CTkLabel(file_frame, text="No se selecciono archivo")
        self.label_archivo.pack(side="left", padx=5)
        
        btn_seleccionar = ctk.CTkButton(file_frame, text="Seleccionar PDF", 
                                      command=self.seleccionar_archivo)
        btn_seleccionar.pack(side="right", padx=5)
        
        name_frame = ctk.CTkFrame(upload_frame)
        name_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(name_frame, text="Nombre del CV:").pack(side="left", padx=5)
        self.entry_nombre_cv = ctk.CTkEntry(name_frame, placeholder_text="Ej: CV Tomas Barrera")
        self.entry_nombre_cv.pack(side="left", fill="x", expand=True, padx=5)
        
        vacante_frame = ctk.CTkFrame(upload_frame)
        vacante_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(vacante_frame, text="Asociar a vacante:").pack(side="left", padx=5)
        
        self.combo_vacantes_cv = ctk.CTkComboBox(vacante_frame, 
                                               values=self.almacenamiento.listar_vacantes())
        self.combo_vacantes_cv.pack(side="left", fill="x", expand=True, padx=5)
        
        btn_subir = ctk.CTkButton(upload_frame, text="Subir CV", 
                                command=self.subir_cv)
        btn_subir.pack(pady=10)
        
        asociar_frame = ctk.CTkFrame(main_frame)
        asociar_frame.pack(fill="x", padx=20, pady=10)
        
        btn_asociar = ctk.CTkButton(asociar_frame, text="Asociar CV Existente a Vacante", 
                                  command=self.asociar_cv_vacante)
        btn_asociar.pack(pady=5)
        
        lista_frame = ctk.CTkFrame(main_frame)
        lista_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(lista_frame, text="CVs Existentes", 
                   font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.tree_cvs = ttk.Treeview(lista_frame, columns=("Vacante", "Fecha"), show="headings")
        self.tree_cvs.heading("#0", text="Nombre CV")
        self.tree_cvs.heading("Vacante", text="Vacante Asociada")
        self.tree_cvs.heading("Fecha", text="Fecha de Subida")
        self.tree_cvs.column("#0", width=200)
        self.tree_cvs.column("Vacante", width=150)
        self.tree_cvs.column("Fecha", width=150)
        
        self.tree_cvs.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.actualizar_lista_cvs()
    
    def crear_tab_evaluacion(self):
        main_frame = ctk.CTkFrame(self.tab_evaluacion)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_label = ctk.CTkLabel(main_frame, text="Evaluacion de Compatibilidad", 
                                 font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)
        
        vacante_frame = ctk.CTkFrame(main_frame)
        vacante_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(vacante_frame, text="Seleccionar Vacante:").pack(side="left", padx=5)
        
        self.combo_vacante_eval = ctk.CTkComboBox(vacante_frame,
                                                values=self.almacenamiento.listar_vacantes(),
                                                command=self.actualizar_cvs_evaluacion)
        self.combo_vacante_eval.pack(side="left", fill="x", expand=True, padx=5)
        
        cvs_frame = ctk.CTkFrame(main_frame)
        cvs_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(cvs_frame, text="CVs para Evaluar:").pack(anchor="w", padx=10, pady=5)
        
        self.frame_lista_cvs = ctk.CTkScrollableFrame(cvs_frame, height=200)
        self.frame_lista_cvs.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.cvs_seleccionados = {}
        
        btn_evaluar = ctk.CTkButton(main_frame, text="Evaluar CVs Seleccionados", 
                                  command=self.evaluar_cvs_seleccionados,
                                  font=ctk.CTkFont(weight="bold"))
        btn_evaluar.pack(pady=10)
    
    def crear_tab_resultados(self):
        main_frame = ctk.CTkFrame(self.tab_resultados)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        title_label = ctk.CTkLabel(main_frame, text="Resultados de Evaluacion", 
                                 font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=10)
        
        ranking_frame = ctk.CTkFrame(main_frame)
        ranking_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(ranking_frame, text="Ranking de Candidatos", 
                   font=ctk.CTkFont(size=16, weight="bold")).pack(pady=10)
        
        self.tree_ranking = ttk.Treeview(ranking_frame, 
                                       columns=("Puntaje", "Cumplidos", "Faltantes"), 
                                       show="headings")
        self.tree_ranking.heading("#0", text="Candidato")
        self.tree_ranking.heading("Puntaje", text="Puntaje %")
        self.tree_ranking.heading("Cumplidos", text="Criterios Cumplidos")
        self.tree_ranking.heading("Faltantes", text="Criterios Faltantes")
        self.tree_ranking.column("#0", width=200)
        self.tree_ranking.column("Puntaje", width=100)
        self.tree_ranking.column("Cumplidos", width=150)
        self.tree_ranking.column("Faltantes", width=150)
        
        self.tree_ranking.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tree_ranking.bind("<<TreeviewSelect>>", self.mostrar_detalles_seleccionado)
        
        detalles_frame = ctk.CTkFrame(main_frame)
        detalles_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(detalles_frame, text="Detalles del Candidato Seleccionado",
                   font=ctk.CTkFont(weight="bold")).pack(pady=5)
        
        self.text_detalles = ctk.CTkTextbox(detalles_frame, height=150)
        self.text_detalles.pack(fill="x", padx=10, pady=10)
    
    def crear_vacante(self):
        nombre = self.campos_vacante["entry_nombre"].get().strip()
        if not nombre:
            messagebox.showerror("Error", "El nombre de la vacante es obligatorio")
            return
        
        estudios = self.estudios_var.get()
        if estudios == "licenciatura" and self.entry_semestre.get().strip():
            semestre_num = self.entry_semestre.get().strip()
            if semestre_num:
                if semestre_num == "1":
                    estudios = "1er semestre"
                elif semestre_num == "2":
                    estudios = "2do semestre" 
                elif semestre_num == "3":
                    estudios = "3er semestre"
                else:
                    estudios = f"{semestre_num}to semestre"
        
        datos_vacante = {
            "Habilidades": normalizar(self.campos_vacante["entry_habilidades"].get()),
            "Competencias": normalizar(self.campos_vacante["entry_competencias"].get()),
            "Palabras_clave": normalizar(self.campos_vacante["entry_palabras_clave"].get()),
            "Estudios": estudios,
            "Experiencia": normalizar(self.campos_vacante["entry_experiencia"].get()),
            "Idioma": normalizar(self.entry_idioma.get()),
            "Nivel del idioma": self.nivel_idioma_var.get(),
            "Herramientas": normalizar(self.campos_vacante["entry_herramientas"].get()),
            "Extras": normalizar(self.campos_vacante["entry_extras"].get())
        }
        
        self.almacenamiento.agregar_vacante(nombre, datos_vacante)
        messagebox.showinfo("Exito", f"Vacante '{nombre}' creada exitosamente")
        
        self.actualizar_lista_vacantes()
        self.combo_vacantes_cv.configure(values=self.almacenamiento.listar_vacantes())
        self.combo_vacante_eval.configure(values=self.almacenamiento.listar_vacantes())
        self.limpiar_campos_vacante()
    
    def seleccionar_archivo(self):
        filename = filedialog.askopenfilename(
            title="Seleccionar archivo PDF",
            filetypes=[("PDF files", "*.pdf")]
        )
        if filename:
            self.label_archivo.configure(text=os.path.basename(filename))
            self.archivo_seleccionado = filename
    
    def subir_cv(self):
        if not hasattr(self, 'archivo_seleccionado') or not self.archivo_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un archivo PDF")
            return
        
        nombre_cv = self.entry_nombre_cv.get().strip()
        if not nombre_cv:
            messagebox.showerror("Error", "El nombre del CV es obligatorio")
            return
        
        texto_cv = leer_archivo_pdf(self.archivo_seleccionado)
        if not texto_cv:
            messagebox.showerror("Error", "No se pudo leer el archivo PDF")
            return
        
        vacante_asociada = self.combo_vacantes_cv.get()
        if vacante_asociada == "":
            vacante_asociada = None
        
        self.almacenamiento.agregar_cv(nombre_cv, texto_cv, self.archivo_seleccionado, vacante_asociada)
        messagebox.showinfo("Exito", f"CV '{nombre_cv}' subido exitosamente")
        
        self.actualizar_lista_cvs()
        self.entry_nombre_cv.delete(0, tk.END)
        self.label_archivo.configure(text="No se selecciono archivo")
        delattr(self, 'archivo_seleccionado')
    
    def asociar_cv_vacante(self):
        if not self.tree_cvs.selection():
            messagebox.showerror("Error", "Seleccione un CV de la lista")
            return
        
        item = self.tree_cvs.selection()[0]
        nombre_cv = self.tree_cvs.item(item, "text")
        
        vacantes = self.almacenamiento.listar_vacantes()
        if not vacantes:
            messagebox.showerror("Error", "No hay vacantes disponibles")
            return
        
        dialog = ctk.CTkInputDialog(text="Seleccione la vacante:", title="Asociar CV")
        vacante_seleccionada = dialog.get_input()
        
        if vacante_seleccionada and vacante_seleccionada in vacantes:
            if self.almacenamiento.asociar_cv_vacante(nombre_cv, vacante_seleccionada):
                messagebox.showinfo("Exito", f"CV asociado a '{vacante_seleccionada}'")
                self.actualizar_lista_cvs()
    
    def actualizar_lista_vacantes(self):
        self.lista_vacantes.delete(0, tk.END)
        vacantes = self.almacenamiento.listar_vacantes()
        for vacante in vacantes:
            self.lista_vacantes.insert(tk.END, vacante)
    
    def actualizar_lista_cvs(self):
        for item in self.tree_cvs.get_children():
            self.tree_cvs.delete(item)
        
        cvs = self.almacenamiento.listar_cvs()
        for nombre_cv in cvs:
            cv_data = self.almacenamiento.obtener_cv(nombre_cv)
            vacante = cv_data.get('vacante_asociada', 'Ninguna')
            fecha = cv_data.get('fecha_agregado', '')
            self.tree_cvs.insert("", tk.END, text=nombre_cv, values=(vacante, fecha))
    
    def actualizar_cvs_evaluacion(self, event=None):
        for widget in self.frame_lista_cvs.winfo_children():
            widget.destroy()
        
        self.cvs_seleccionados = {}
        
        vacante_seleccionada = self.combo_vacante_eval.get()
        if not vacante_seleccionada:
            return
        
        cvs = self.almacenamiento.listar_cvs(vacante_seleccionada)
        if not cvs:
            cvs = self.almacenamiento.listar_cvs()
        
        for nombre_cv in cvs:
            frame = ctk.CTkFrame(self.frame_lista_cvs)
            frame.pack(fill="x", padx=5, pady=2)
            
            var = tk.BooleanVar()
            chk = ctk.CTkCheckBox(frame, text=nombre_cv, variable=var)
            chk.pack(side="left", padx=5, pady=2)
            
            self.cvs_seleccionados[nombre_cv] = var
    
    def evaluar_cvs_seleccionados(self):
        vacante_nombre = self.combo_vacante_eval.get()
        if not vacante_nombre:
            messagebox.showerror("Error", "Seleccione una vacante")
            return
        
        cvs_a_evaluar = [nombre for nombre, var in self.cvs_seleccionados.items() if var.get()]
        if not cvs_a_evaluar:
            messagebox.showerror("Error", "Seleccione al menos un CV")
            return
        
        vacante_data = self.almacenamiento.obtener_vacante(vacante_nombre)
        if not vacante_data:
            messagebox.showerror("Error", "No se encontraron datos de la vacante")
            return
        
        resultados = []
        for nombre_cv in cvs_a_evaluar:
            cv_data = self.almacenamiento.obtener_cv(nombre_cv)
            if cv_data:
                resultado = self.evaluar_cv_individual(vacante_data, cv_data)
                resultados.append({
                    'nombre_cv': nombre_cv,
                    'resultado': resultado,
                    'puntaje': resultado['puntaje']
                })
        
        resultados.sort(key=lambda x: x['puntaje'], reverse=True)
        self.mostrar_resultados(resultados, vacante_nombre)
        
        self.tabview.set("Resultados")
    
    def evaluar_cv_individual(self, vacante_data, cv_data):
        datos_vacante = vacante_data['datos']
        texto_cv = cv_data['texto']
        
        SiApareceList = []
        NoApareceList = []
        texto = normalizar(texto_cv)
        
        for clave, valor in datos_vacante.items():
            if valor.strip():
                if clave in ["Habilidades", "Competencias", "Palabras_clave", "Herramientas"]:
                    elementos = [elem.strip() for elem in valor.split(',') if elem.strip()]
                    elementos_encontrados = []
                    elementos_no_encontrados = []
                    
                    for elemento in elementos:
                        if elemento in texto:
                            elementos_encontrados.append(elemento)
                        else:
                            elementos_no_encontrados.append(elemento)
                    
                    if elementos_encontrados:
                        SiApareceList.append(f"{clave}: {', '.join(elementos_encontrados)}")
                    if elementos_no_encontrados:
                        NoApareceList.append(f"{clave}: {', '.join(elementos_no_encontrados)}")
                
                elif clave == "Nivel del idioma" and datos_vacante["Idioma"].strip():
                    idioma_vacante = datos_vacante["Idioma"]
                    if idioma_vacante in texto:
                        niveles_posibles = ["principiante", "intermedio", "avanzado"]
                        nivel_encontrado = None
                        for nivel in niveles_posibles:
                            if nivel in texto:
                                nivel_encontrado = nivel
                                break
                        
                        if nivel_encontrado and comparar_niveles_idioma(valor, nivel_encontrado):
                            SiApareceList.append(f"{clave}: {valor} -> CV tiene {nivel_encontrado}")
                        else:
                            NoApareceList.append(f"{clave}: {valor} (nivel insuficiente)")
                    else:
                        NoApareceList.append(f"{clave}: {valor} (idioma no encontrado)")
                
                elif clave == "Estudios":
                    estudio_encontrado = False
                    niveles_buscar = ["licenciatura", "maestria", "master", "doctorado", "phd", "semestre"]
                    
                    for nivel in niveles_buscar:
                        if nivel in texto:
                            estudio_encontrado = True
                            break
                    
                    if not estudio_encontrado:
                        patron_semestre = r'(\d+)(?:°|º|o|°|\.?)\s*semestre'
                        if re.search(patron_semestre, texto):
                            estudio_encontrado = True
                    
                    if estudio_encontrado and comparar_estudios(valor, texto):
                        SiApareceList.append(f"{clave}: {valor} -> CV cumple requisito")
                    else:
                        NoApareceList.append(f"{clave}: {valor} (no cumple requisito)")
                
                else:
                    if valor in texto:
                        SiApareceList.append(f"{clave}: {valor}")
                    else:
                        NoApareceList.append(f"{clave}: {valor}")
        
        total_elementos = 0
        elementos_encontrados = 0
        
        for clave, valor in datos_vacante.items():
            if valor.strip():
                if clave in ["Habilidades", "Competencias", "Palabras_clave", "Herramientas"]:
                    elementos = [elem.strip() for elem in valor.split(',') if elem.strip()]
                    total_elementos += len(elementos)
                    for elemento in elementos:
                        if elemento in texto:
                            elementos_encontrados += 1
                else:
                    total_elementos += 1
                    if any(f"{clave}: {valor}" in criterio for criterio in SiApareceList):
                        elementos_encontrados += 1
        
        if total_elementos == 0:
            puntaje = 0
        else:
            puntaje = (elementos_encontrados / total_elementos) * 100
        
        return {
            "no_aparecen": NoApareceList,
            "si_aparecen": SiApareceList,
            "puntaje": puntaje
        }
    
    def mostrar_resultados(self, resultados, vacante_nombre):
        for item in self.tree_ranking.get_children():
            self.tree_ranking.delete(item)
        
        self.resultados_actuales = resultados
        
        for i, resultado in enumerate(resultados, 1):
            self.tree_ranking.insert("", tk.END, text=resultado['nombre_cv'],
                                   values=(f"{resultado['puntaje']:.2f}%",
                                           len(resultado['resultado']['si_aparecen']),
                                           len(resultado['resultado']['no_aparecen'])))
    
    def mostrar_detalles_seleccionado(self, event):
        selection = self.tree_ranking.selection()
        if not selection:
            return
        
        item = selection[0]
        nombre_cv = self.tree_ranking.item(item, "text")
        
        resultado = None
        for res in self.resultados_actuales:
            if res['nombre_cv'] == nombre_cv:
                resultado = res
                break
        
        if resultado:
            texto = f"CV: {nombre_cv}\n"
            texto += f"Puntaje: {resultado['puntaje']:.2f}%\n\n"
            
            texto += "CRITERIOS CUMPLIDOS:\n"
            for criterio in resultado['resultado']['si_aparecen']:
                texto += f"✓ {criterio}\n"
            
            texto += "\nCRITERIOS NO CUMPLIDOS:\n"
            for criterio in resultado['resultado']['no_aparecen']:
                texto += f"✗ {criterio}\n"
            
            self.text_detalles.delete("1.0", tk.END)
            self.text_detalles.insert("1.0", texto)
    
    def limpiar_campos_vacante(self):
        for entry in self.campos_vacante.values():
            entry.delete(0, tk.END)
        self.entry_idioma.delete(0, tk.END)
        self.entry_semestre.delete(0, tk.END)
        self.estudios_var.set("licenciatura")
        self.nivel_idioma_var.set("intermedio")
        self.actualizar_campo_semestre()

if __name__ == "__main__":
    app = ATSApp()
    app.mainloop()