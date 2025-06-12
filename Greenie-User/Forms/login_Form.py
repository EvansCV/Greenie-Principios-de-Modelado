import json
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.font import BOLD
import Util.util_imagenes as util_imagenes
import Util.util_ventana as util_ventana
from Forms.master_form import Master_Form
from config import COLOR_BACKGROUND, COLOR_BACKGROUND2, COLOR_SECUNDARIO, COLOR_PRINCIPAL
from DB.Defaut_Values import default_Values
from Conection.arduinoThread import ArduinoThread
from DB.Parser import Parser

class Login_Form():

    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Greenie")
        w, h = 450, 600
        self.ventana.geometry("%dx%d+0+0" % (w, h))
        util_ventana.centrar_ventana(self.ventana, w, h)
        self.ventana.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.ventana.resizable(False, False)

        self.ruta = "./Shared_DB/DB_users.json"

        self.logo = util_imagenes.leer_imagen("./assets/icon1.png", (250, 90))
        self.icono = util_imagenes.leer_imagen("./assets/icon.png", (250, 90))
        self.ventana.iconphoto(True, self.icono)

        frame_logo = tk.Frame(self.ventana,bd=0,width=200,relief=tk.SOLID, padx=10, pady=5,bg=COLOR_BACKGROUND2)
        frame_logo.pack(side=tk.TOP,fill=tk.BOTH, expand=tk.YES)
        label = tk.Label(frame_logo,image = self.logo,bg=COLOR_BACKGROUND2)
        label.place(x=0, y=2, relwidth=1, relheight=1)

        frame_form = tk.Frame(self.ventana,bg=COLOR_PRINCIPAL,bd=0,relief=tk.SOLID)
        frame_form.pack(side=tk.BOTTOM, expand=tk.YES,fill=tk.BOTH)

        frame_form_top = tk.Frame(frame_form,height=50,bg=COLOR_PRINCIPAL,bd=0,relief=tk.SOLID)
        frame_form_top.pack(side=tk.TOP, fill=tk.Y)
        title = tk.Label(frame_form_top,text="Inicio de sesion",font=('Arial',30),
                         bg=COLOR_PRINCIPAL,fg=COLOR_SECUNDARIO,padx=50,pady=5)
        title.pack(expand=tk.YES,fill=tk.BOTH, pady=2)

        frame_form_fill = tk.Frame(frame_form,height=50,bd=0,relief=tk.SOLID,bg=COLOR_PRINCIPAL)
        frame_form_fill.pack(side=tk.BOTTOM, fill=tk.BOTH,expand=tk.YES)

        etiqueta_usuario = tk.Label(frame_form_fill,text="Usuario:",font=('Arial',14),fg=COLOR_SECUNDARIO,
                                    bg=COLOR_PRINCIPAL,anchor="n")
        etiqueta_usuario.pack(fill=tk.X,padx=5,pady=2)
        self.usuario= ttk.Entry(frame_form_fill,font=('Arial',14))
        self.usuario.pack(padx=5,pady=10)

        etiqueta_password = tk.Label(frame_form_fill,text="Password:",font=('Arial',14),
                                     fg=COLOR_SECUNDARIO,bg=COLOR_PRINCIPAL,anchor="n")
        etiqueta_password.pack(fill=tk.X,padx=5,pady=2)
        self.password = ttk.Entry(frame_form_fill,font=('Arial',14))
        self.password.pack(padx=5,pady=5)
        self.password.config(show="*")

        inicio = tk.Button(frame_form_fill,text="Entrar",font=('Arial',15,BOLD),bg=COLOR_BACKGROUND,
                           fg=COLOR_SECUNDARIO,bd=0,command=self.validar)
        inicio.pack(padx=5,pady=5)
        inicio.bind("<Return>",(lambda event: self.validar()))


    def validar(self):
        codigo_dispositivo = self.usuario.get()
        password = self.password.get()
        acceso = self.verificar_credenciales(codigo_dispositivo,password)
        if (acceso):
            self.ventana.destroy()
            self.default_Values = default_Values()
            self.default_Values.cargar_config()
            arduino_thread = ArduinoThread(puerto='COM3')
            arduino_thread.start()
            parser_thread = Parser(arduino_thread)
            parser_thread.start()
            self.default_Values.codigo = codigo_dispositivo
            app = Master_Form(arduino_thread,parser_thread)
            app.ejecutar()
        else:
            messagebox.showerror("Mensaje","Usuario o password incorrecto")

    def verificar_credenciales(self, codigo_dispositivo: str, password: str) -> bool:
        try:
            with open(self.ruta, "r") as f:
                data = json.load(f)
            if codigo_dispositivo in data:
                pIngresada = data[codigo_dispositivo]
                if password == pIngresada:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            print(f"[Error] al verificar credenciales: {e}")
            return False

    def ejecutar(self):
        self.ventana.mainloop()

    def cerrar(self):
        print("🛑 Cerrando aplicación...")
        self.ventana.destroy()