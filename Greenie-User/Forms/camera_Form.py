import datetime
import os
import tkinter as tk

import cv2
from config import COLOR_BACKGROUND, COLOR_SECUNDARIO, COLOR_BACKGROUND2
from DB.Defaut_Values import default_Values
from DB.gestor_automatico import Gestor_automatico

class Camera_Form():

    def __init__(self, panel_principal):
        self.panel_central = tk.Frame(panel_principal)
        self.panel_central.pack(side=tk.BOTTOM, fill="both", expand=True)

        self.panel_sup = tk.Frame(panel_principal)
        self.panel_sup.pack(side=tk.BOTTOM,fill=tk.X, expand=False)

        self.lblCamera = tk.Label(self.panel_sup, text="Camara")
        self.lblCamera.config(fg="#222d33", font=("Roboto", 15), bg=COLOR_BACKGROUND)
        self.lblCamera.pack(side=tk.TOP, fill="both", expand=True)

        self.lblcam = tk.Label(self.panel_central, text="Captura de foto (min)")
        self.lblcam.config(fg=COLOR_SECUNDARIO, font=("Roboto", 10), bg=COLOR_BACKGROUND2)
        self.lblcam.pack(side=tk.TOP, fill="both", expand=False)

        self.default_Cam = tk.StringVar(self.panel_central)
        self.default_Cam.set(f"{default_Values().intervalo_Cam}")
        self.opcionesTemp = ["1","5","10","15","30","45","60","90","120"]
        self.menuTemp = tk.OptionMenu(self.panel_central,self.default_Cam, *self.opcionesTemp)
        self.menuTemp.config(background=COLOR_BACKGROUND2,width=10)
        self.menuTemp.pack(side=tk.TOP)

        self.buttomGuardar = tk.Button(self.panel_central, text= "Guardar")
        self.buttomGuardar.config(background=COLOR_BACKGROUND2,width=15,command=self.aplicar_Cambios)
        self.buttomGuardar.pack(side=tk.TOP)

        self.buttomfoto = tk.Button(self.panel_central, text= "Tomar foto")
        self.buttomfoto.config(background=COLOR_BACKGROUND2,width=15,command=self.generarFoto)
        self.buttomfoto.pack(side=tk.TOP)

        self.buttomtimelapse = tk.Button(self.panel_central, text= "Generar timelapse")
        self.buttomtimelapse.config(background=COLOR_BACKGROUND2,width=15,command=self.generarTimeLapse)
        self.buttomtimelapse.pack(side=tk.TOP)



    def aplicar_Cambios(self):
        default_Values().intervalo_Cam = int(self.default_Cam.get())
        default_Values().guardar_config()

    def generarFoto(self):
        gestor = Gestor_automatico()
        gestor.tomar_foto()

    def generarTimeLapse(self):
        # Ruta a la carpeta con imágenes
        carpeta_imagenes = default_Values().CARPETA_FOTOS
        carpeta_video_salida = default_Values().CARPETA_VIDEOS  # Carpeta de destino

        # Asegurar que exista la carpeta de salida
        os.makedirs(carpeta_video_salida, exist_ok=True)

        # Extensiones válidas
        extensiones_validas = [".jpg"]

        # Obtener lista ordenada de imágenes
        imagenes = sorted([
            os.path.join(carpeta_imagenes, archivo)
            for archivo in os.listdir(carpeta_imagenes)
            if os.path.splitext(archivo)[1].lower() in extensiones_validas
        ])

        # Verifica que haya imágenes
        if not imagenes:
            return

        # Leer la primera imagen para obtener tamaño
        frame = cv2.imread(imagenes[0])
        alto, ancho, _ = frame.shape

        # Obtener fecha y hora actual
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Ruta completa del archivo de salida con timestamp
        nombre_video = f"timelapse_{timestamp}.avi"
        ruta_video = os.path.join(carpeta_video_salida, nombre_video)

        # Crear el objeto VideoWriter
        salida = cv2.VideoWriter(ruta_video, cv2.VideoWriter_fourcc(*'XVID'), 10, (ancho, alto))

        # Agregar cada imagen al video
        for imagen_path in imagenes:
            img = cv2.imread(imagen_path)
            if img is None:
                continue
            img = cv2.resize(img, (ancho, alto))  # Asegura tamaño constante
            salida.write(img)

        # Liberar recursos
        salida.release()
