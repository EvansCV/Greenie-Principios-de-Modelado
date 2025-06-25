import tkinter as tk
from tkinter import font

import config
#---------------------------------------------------------/
from config import COLOR_BACKGROUND, COLOR_BACKGROUND2, COLOR_SECUNDARIO, COLOR_PRINCIPAL
import Util.util_imagenes as util_imagenes
import Util.util_ventana as util_ventana
#---------------------------------------------------------/
from Forms.construction_Form import ConstructionForm
from Forms.ticket_Form import TicketForm


class Master_Form(tk.Tk):

    def __init__(self):
        super().__init__()
        self.etiquetas = None

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
        self.iconTickets = util_imagenes.leer_icon("./assets/ticketB.png")

        #---------------------------------------

        self.iconphoto(True, self.icono)
        self.config_window()
        self.paneles()
        self.controles_barra_superior()
        self.controles_menu_lateral()
        self.controles_cuerpo()
        self.controles_notificacion()

    def config_window(self):
        self.title("Greenie")
        w, h = 1500, 800
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


    def controles_barra_superior(self):
        font_awesome = font.Font(family='FontAwesome', size=12)
        self.buttonMenuLateral = tk.Button(self.barra_superior, image=self.iconMenu,
                                           font=font_awesome, command=self.toggle_panel_menu,
                                           bd=0, bg=COLOR_PRINCIPAL,
                                           fg="White")
        self.buttonMenuLateral.pack(side=tk.LEFT,padx=5,pady=10)

        self.buttonMenuNotificaciones = tk.Button(self.barra_superior, image=self.iconSNoti,
                                                  font=font_awesome,
                                                  bd=0, bg=COLOR_PRINCIPAL,
                                                  fg="White")
        self.buttonMenuNotificaciones.pack(side=tk.LEFT,padx=5,pady=10)

        self.labelEstado = tk.Label(self.barra_superior, text="Admin")
        self.labelEstado.config(fg="#fff", font=("roboto",15), bg=COLOR_PRINCIPAL,
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

        self.buttonRegistro = tk.Button(self.menu_lateral)
        self.buttonTickets = tk.Button(self.menu_lateral)


        buttons_info = [
            ("Registro", self.iconDash, self.buttonRegistro, self.en_construccion),
            ("Tickets", self.iconTickets, self.buttonTickets, self.abrir_panel_tickets),
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
        pass

    def abrir_panel_tickets(self):
        self.limpiar_panel(self.cuerpo_principal)
        TicketForm(self.cuerpo_principal)

    def en_construccion(self):
        self.limpiar_panel(self.cuerpo_principal)
        ConstructionForm(self.cuerpo_principal,self.construccion)

    def limpiar_panel(self, panel):
        self.etiquetas = None
        for widget in panel.winfo_children():
            widget.destroy()

    def ejecutar(self):
        self.mainloop()

    def cerrar(self):
        print("🛑 Cerrando aplicación...")
        self.destroy()




