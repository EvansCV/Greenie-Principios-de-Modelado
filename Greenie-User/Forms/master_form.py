import tkinter as tk
from tkinter import font

import config
#---------------------------------------------------------/
from config import COLOR_BACKGROUND, COLOR_BACKGROUND2, COLOR_SECUNDARIO, COLOR_PRINCIPAL
import Util.util_imagenes as util_imagenes
import Util.util_ventana as util_ventana
from DB.Defaut_Values import default_Values
#---------------------------------------------------------/
from Forms.dashboard_Form import DashboardForm
from Forms.info_form import InfoForm
from Forms.construction_Form import ConstructionForm
from Forms.graphic_Form import GraphicForm
from Forms.active_Form import Active_Form
from Forms.ticket_Form import TicketForm


class Master_Form(tk.Tk):
    def __init__(self,arduino_worker,parser_worker, usuario_actual):
        super().__init__()
        self.arduino = arduino_worker
        self.parser = parser_worker
        self.etiquetas = None
        self.usuario_actual = usuario_actual


        #//Bloque de imagenes e iconos
        self.logo = util_imagenes.leer_imagen("./assets/icon1.png", (250, 90))
        self.iconTitle = util_imagenes.leer_imagen("./assets/icon1.png", (150, 30))
        self.icono = util_imagenes.leer_imagen("./assets/icon.png", (250, 90))
        self.construccion = util_imagenes.leer_imagen("./assets/construccion.png", (200, 200))

        #iconos del menu
        self.iconMenu = util_imagenes.leer_icon("./assets/menu.png")
        self.iconDash = util_imagenes.leer_icon("./assets/datosB.png")
        self.iconConfi = util_imagenes.leer_icon("./assets/confiB.png")
        self.iconActuadores = util_imagenes.leer_icon("./assets/actuadoresB.png")
        self.iconGrafica = util_imagenes.leer_icon("./assets/graficasB.png")
        self.iconCam = util_imagenes.leer_icon("./assets/camB.png")
        self.iconCNoti = util_imagenes.leer_icon("./assets/Cnoti.png")
        self.iconSNoti = util_imagenes.leer_icon("./assets/Snoti.png")
        self.iconTickets = util_imagenes.leer_icon("./assets/icon.png")

        #---------------------------------------

        self.iconphoto(True, self.icono)
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.controles_cuerpo()
        self.controles_notificacion()
        self.notificaciones.destroy()


    def config_window(self):
        self.title("Greenie")
        w, h = 450, 600
        self.geometry("%dx%d+0+0" % (w, h))
        util_ventana.centrar_ventana(self,w,h)
        self.protocol("WM_DELETE_WINDOW", self.cerrar)
        self.resizable(False, False)

    def paneles(self):
        self.barra_superior = tk.Frame(self, bg=COLOR_PRINCIPAL,height=50)
        self.barra_superior.pack(side=tk.TOP, fill="both", expand=False)

        self.menu_lateral = tk.Frame(self, bg=COLOR_SECUNDARIO,width=80)
        self.menu_lateral.pack(side=tk.LEFT, fill="both", expand=False)
        self.menu_lateral.pack_forget()

        self.cuerpo_principal = tk.Frame(self, bg=COLOR_BACKGROUND2, width=200)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill="both", expand=True)

        self.notificaciones = tk.Frame(self.cuerpo_principal, bg=COLOR_SECUNDARIO, height=100)
        self.notificaciones.pack(side=tk.TOP, fill="both")


    def controles_barra_superior(self):
        font_awesome = font.Font(family='FontAwesome', size=12)
        self.buttonMenuLateral = tk.Button(self.barra_superior, image=self.iconMenu,
                                           font=font_awesome, command=self.toggle_panel_menu,
                                           bd=0, bg=COLOR_PRINCIPAL,
                                           fg="White")
        self.buttonMenuLateral.pack(side=tk.LEFT,padx=5,pady=10)

        self.buttonMenuNotificaciones = tk.Button(self.barra_superior, image=self.iconSNoti,
                                                  font=font_awesome, command=self.toggle_panel_Notificaciones,
                                                  bd=0, bg=COLOR_PRINCIPAL,
                                                  fg="White")
        self.buttonMenuNotificaciones.pack(side=tk.LEFT,padx=5,pady=10)

        self.labelEstado = tk.Label(self.barra_superior, text="Estado...")
        self.labelEstado.config(fg="#fff", font=("roboto",12), bg=COLOR_PRINCIPAL,
                                pady=1, width=15)
        self.labelEstado.pack(side=tk.RIGHT)

    def controles_cuerpo(self):
        label = tk.Label(self.cuerpo_principal, image=self.logo,
                         bg=COLOR_BACKGROUND2)
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def controles_menu_lateral(self):
        ancho_menu = 150
        alto_menu = 30
        font_awesome = font.Font(family='FontAwesome', size=12)

        self.labelCodigo = tk.Label(self.menu_lateral, text=default_Values.codigo)
        self.labelCodigo.config(fg="#fff", font=("roboto", 15),bg=COLOR_SECUNDARIO,
                                pady=1,justify=tk.LEFT)
        self.labelCodigo.pack(side=tk.BOTTOM,fill=tk.X)

        self.buttonDashBoard = tk.Button(self.menu_lateral)
        self.buttonActivadores = tk.Button(self.menu_lateral)
        self.buttonConfiguracion = tk.Button(self.menu_lateral)
        self.buttonGraficas = tk.Button(self.menu_lateral)
        self.buttonCam = tk.Button(self.menu_lateral)

        buttons_info = [
            ("Dashboard", self.iconDash, self.buttonDashBoard,self.abril_panel_dashboard),
            ("Graficas", self.iconGrafica, self.buttonGraficas,self.abrir_panel_graficas),
            ("Activadores", self.iconActuadores, self.buttonActivadores, self.abrir_panel_activadores),
            ("Cam", self.iconCam, self.buttonCam,self.en_construccion),
            ("Configuracion", self.iconConfi, self.buttonConfiguracion,self.en_construccion),
            ("Tickets", self.iconTickets, tk.Button(self.menu_lateral), self.abrir_panel_tickets),

        ]

        for text, icon, button, comando in buttons_info:
            self.configurar_boton_menu(button, text, icon, font_awesome,ancho_menu, alto_menu, comando)

    def configurar_boton_menu(self, button, text, icon, font_awesome,ancho_menu, alto_menu, comando):
        button.config(text=f"{  text }", anchor="w", font=font_awesome,
                      bd=0, bg=COLOR_SECUNDARIO, fg="White", width=ancho_menu,height=alto_menu, command=comando,
                      image= icon, compound=tk.LEFT,padx=5)
        button.pack(side=tk.TOP)
        self.bind_hover_events(button)

    def bind_hover_events(self, button):
        button.bind("<Enter>", lambda event: self.on_enter(event, button))
        button.bind("<Leave>", lambda event: self.on_leave(event, button))

    def on_enter(self, event, button):
        button.config(bg=COLOR_PRINCIPAL, fg="White")

    def on_leave(self, event, button):
        button.config(bg=COLOR_SECUNDARIO, fg="White")

    def toggle_panel_menu(self):
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill="y")

    def controles_notificacion(self):
        self.labelNotificacion = tk.Label(self.notificaciones, text="Notificaciones")
        self.labelNotificacion.config(fg="#fff", font=("roboto", 12), bg=COLOR_SECUNDARIO,
                                pady=1, width=15)
        self.labelNotificacion.pack(side=tk.TOP, fill=tk.X)

        self.labelNotiAbono = tk.Label(self.notificaciones, text="Recuerda abonar la tierra")
        self.labelNotiAbono.config(fg="#fff", font=("roboto", 12), bg=COLOR_SECUNDARIO,relief=tk.RIDGE,
                                pady=1, width=15,)
        self.labelNotiAbono.pack(side=tk.TOP, fill=tk.X)

        if default_Values.notificacion_abono:
            self.labelNotiAbono.pack(side=tk.TOP, fill=tk.X)
            self.buttonMenuNotificaciones.config(image=self.iconCNoti)
        else:
            self.labelNotiAbono.pack_forget()

    def toggle_panel_Notificaciones(self):
        if self.notificaciones.winfo_exists():
            self.notificaciones.destroy()
        else:
            self.notificaciones = tk.Frame(self.cuerpo_principal, bg=COLOR_SECUNDARIO, height=100)
            self.notificaciones.pack(side=tk.TOP, fill="both")
            self.controles_notificacion()

    def abril_panel_dashboard(self):
        self.limpiar_panel(self.cuerpo_principal)
        self.etiquetas = DashboardForm(self.cuerpo_principal)

    def abril_panel_info(self):
        InfoForm()

    def abrir_panel_graficas(self):
        self.limpiar_panel(self.cuerpo_principal)
        GraphicForm(self.cuerpo_principal)

    def abrir_panel_activadores(self):
        self.limpiar_panel(self.cuerpo_principal)
        Active_Form(self.cuerpo_principal,self.arduino)

    def abrir_panel_config(self):
        self.limpiar_panel(self.cuerpo_principal)

    def abrir_panel_tickets(self):
        self.limpiar_panel(self.cuerpo_principal)
        TicketForm(
            self.cuerpo_principal,
            id_usuario=self.usuario_actual["id"],
            nombre=self.usuario_actual["nombre"],
            telefono=self.usuario_actual["telefono"],
            direccion=self.usuario_actual["direccion"]
        )

    def en_construccion(self):
        self.limpiar_panel(self.cuerpo_principal)
        ConstructionForm(self.cuerpo_principal,self.construccion)

    def limpiar_panel(self, panel):
        self.etiquetas = None
        for widget in panel.winfo_children():
            widget.destroy()

    def actualizar_datos(self):
        estado = self.arduino.obtener_estado()
        datos = self.arduino.obtener_datos()
        if estado == False:
            self.labelEstado.config(text= self.arduino.labelEstado)
        else:
            self.labelEstado.config(text=self.arduino.labelEstado)
            if self.etiquetas != None:
                if datos:
                    temp = datos.get("temperatura", "--")
                    self.etiquetas.lblTempData.config(text=f"{temp} °C")

                    humA = datos.get("humedadAmbiente", "--")
                    self.etiquetas.lblHumAData.config(text=f"{humA} %")

                    luzA = datos.get("luzAmbiente", "--")
                    self.etiquetas.lblLuzData.config(text=f"{luzA} %")

                    humS = datos.get("humedadSuelo", "--")
                    self.etiquetas.lblHumSData.config(text=f"{humS} %")

                    aguaP = datos.get("aguaPotable", "--")
                    self.etiquetas.lblAPData.config(text=f"{aguaP} %")

                    aguaD = datos.get("aguaDrenada", "--")
                    self.etiquetas.lblADData.config(text=f"{aguaD} %")

                    luces = datos.get("luces", "--")
                    if luces:
                        self.etiquetas.lblLucesData.config(text="Activas")
                    else:
                        self.etiquetas.lblLucesData.config(text="Inactivas")
                    vent = datos.get("ventilador", "--")
                    if vent:
                        self.etiquetas.lblVentData.config(text="Activo")
                    else:
                        self.etiquetas.lblVentData.config(text="Inactivo")

                    tapa = datos.get("tapaSuperior", "--")
                    if tapa:
                        self.etiquetas.lblTapaData.config(text="Abierto")
                        default_Values.compuerta = tapa
                    else:
                        self.etiquetas.lblTapaData.config(text="Cerrada")
                        default_Values.compuerta = tapa

        self.after(1000, self.actualizar_datos)


    def ejecutar(self):
        self.actualizar_datos()
        self.mainloop()

    def cerrar(self):
        print("🛑 Cerrando aplicación...")
        self.arduino.detener()
        self.parser.detener()
        self.destroy()





