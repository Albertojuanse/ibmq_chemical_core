"""Este modulo implementa el front-end de la aplicación gráfica"""

# Conexiones por arquitectura
from ibmq_chemical_grafica import zaga
from ibmq_chemical_comun import interfazsistema

# Dependencias
from tkinter import *
from tkinter import ttk, font


class InterfazDeUsuario:
    """Esa clase ejecuta la ventana que sirve como interfaz gráfica del usuario"""

    def __init__(self):
        # Se inicializan las variables
        molecula = {"driver": "PYSCF",
                    "configuracion":
                        {"properties":
                            {"atom": "Li .0 .0 .0; H .0 .0 1.6",
                             "unit": "Angstrom",
                             "charge": 0,
                             "spin": 0,
                             "basis": "sto3g"}
                         }
                    }
        problema = {"general": {"tipo_de_mapeo": "parity"},
                    "COBYLA": {"max_eval": 200},
                    "UCCSD": {"profundidad": 1,
                              "orbitales_activos_ocupados": [0],
                              "orbitales_activos_no_ocupados": [0, 1],
                              "numero_de_slices": 1
                              }
                    }

        resultados = {"nombre": "",
                      "resultado": "",
                      "consola": []
                      }
        self.MOL_DRIVER = molecula["driver"]
        self.MOL_ATOM = molecula["configuracion"]["properties"]["atom"]
        self.MOL_UNIT = molecula["configuracion"]["properties"]["unit"]
        self.MOL_CHARGE = molecula["configuracion"]["properties"]["charge"]
        self.MOL_SPIN = molecula["configuracion"]["properties"]["spin"]
        self.MOL_BASIS = molecula["configuracion"]["properties"]["basis"]
        self.PRO_MAPEO = problema["general"]["tipo_de_mapeo"]
        self.PRO_COBYLA_MAXEVAL = problema["COBYLA"]["max_eval"]
        self.PRO_UCCSD_PROF = problema["UCCSD"]["profundidad"]
        self.PRO_UCCSD_OAO = problema["UCCSD"]["orbitales_activos_ocupados"]
        self.PRO_UCCSD_OANO = problema["UCCSD"]["orbitales_activos_no_ocupados"]
        self.PRO_UCCSD_SLICES = problema["UCCSD"]["numero_de_slices"]
        self.RES_NOM = resultados["nombre"]
        self.RES_RES = resultados["resultado"]
        self.RES_CON = resultados["consola"]
        self.variable_barra_estado = StringVar()
        self.variable_barra_estado.set("Seleccione una opción")

        # Se cargan los iconos
        nombres_iconos = ["a.png",
                          "b.png"
                          ]
        self.iconos = interfazsistema.importar_imagenes()

        # Se crea la ventana del sistema operativo y se configura
        # self.raiz.geometry("450x450")
        # self.raiz.resizable(width=False, height=False)
        # self.raiz.iconphoto(self.raiz, PhotoImage(file=iconos[0]))
        self.raiz = Tk()
        self.raiz.title("IBMQ Chemical")
        self.raiz.option_add("*Font", "Helvetica 12")
        self.raiz.option_add("-fullscreen", True)
        self.raiz.minsize(400, 300)

        # Se crean los estilos
        fuente_normal = font.Font(weight="bold")
        fuente_negrita = font.Font(weight="bold")

        # Se definen los menús
        barramenu = Menu(self.raiz)
        self.raiz["menu"] = barramenu

        self.menu_opciones = Menu(barramenu, tearoff=0)
        self.menu_ayuda = Menu(barramenu, tearoff=0)
        barramenu.add_cascade(menu=self.menu_opciones, label="Opciones")
        barramenu.add_cascade(menu=self.menu_ayuda, label="Ayuda")

        self.menu_opciones.add_command(label="VQE", command=self.ejecutar_vqe,
                                       underline=0, accelerator="Alt+v",
                                       image=PhotoImage(file=self.iconos[1]),
                                       compound=LEFT)
        self.menu_opciones.add_separator()
        self.menu_opciones.add_command(label="Aleatorios", command=self.ejecutar_aleatorios,
                                       underline=0, accelerator="Alt+a",
                                       image=PhotoImage(file=self.iconos[2]),
                                       compound=LEFT)

        self.menu_ayuda.add_command(label="Acerca de", command=self.ayuda,
                                       underline=0, accelerator="Alt+h",
                                       image=PhotoImage(file=self.iconos[3]),
                                       compound=LEFT)
        self.menu_opciones.add_separator()

        # Se define la barra de herramientas
        self.barraherrameintas = Frame(self.raiz, relief=RAISED, bd=2)
        self.boton = Button(self.barraherrameintas, image=PhotoImage(file=self.iconos[4]))

        # Se define la barra de estado
        self.barra_estado = Label(self.raiz, text=self.variable_barra_estado, bd=1, relief=SUNKEN, anchor=W)
        self.barra_estado.pack(side=BOTTOM, fill=X)

        # Se definen los elementos de la ventana
        self.etiq_bienvenida = Label(self.raiz, text="Bienvenido a IBMQ Chemical", font=fuente_negrita)
        self.etiq_info = Label(self.raiz, text="Elija una opción")
        self.ctexto1 = ttk.Entry(self.raiz, textvariable=self.variable1, width=30)
        self.ctexto2 = ttk.Entry(self.raiz, textvariable=self.variable2, width=30)
        self.separ1 = ttk.Separator(self.raiz, orient=HORIZONTAL)
        self.boton1 = ttk.Button(self.raiz, text="Aceptar", command=self.aceptar)
        self.boton2 = ttk.Button(self.raiz, text="Salir", command=self.abrir)

        # Se maqueta la ventana
        """
        self.etiq_bienvenida.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.etiq_info.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.ctexto1.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.ctexto2.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.separ1.pack(side=TOP, fill=BOTH, expand=True, padx=5, pady=5)
        self.boton1.pack(side=BOTTOM, fill=BOTH, expand=True, padx=5, pady=5)
        self.boton2.pack(side=BOTTOM, fill=BOTH, expand=True, padx=5, pady=5)
        """

        self.etiq_bienvenida.grid(row=0, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.etiq_info.grid(row=1, column=0, sticky=(N, S, E, W))
        self.ctexto1.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky=(E, W))
        self.ctexto2.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky=(E, W))
        self.separ1.grid(row=3, column=0, columnspan=3, sticky=(N, S, E, W))
        self.boton1.grid(row=4, column=1, padx=5, pady=5, sticky=E)
        self.boton2.grid(row=4, column=2, padx=5, pady=5, sticky=W)

        self.raiz.columnconfigure(0, weight=1)
        self.raiz.columnconfigure(1, weight=1)
        self.raiz.columnconfigure(2, weight=1)
        self.raiz.rowconfigure(0, weight=1)
        self.raiz.rowconfigure(1, weight=1)
        self.raiz.rowconfigure(4, weight=1)

        """
        self.marco_menu = self.generar_menu()
        self.marco_menu.pack(side=TOP)
        self.marco_principal = self.generar_interfaz_base()
        self.marco_principal.pack(side=LEFT)
        self.marco_principal_vqe = self.generar_interfaz_vqe()
        self.marco_principal_aleatorios = self.generar_interfaz_aleatorios()
        """
        # Se ejecuta la ventana
        self.raiz.mainloop()

    def aceptar(self):
        print(self.ctexto1.get() + self.ctexto2.get())

    def abrir(self):
        self.dialogo = Toplevel()
        self.dialogo.title("Configuración")
        boton = ttk.Button(self.dialogo, text="Cerrar", command=self.dialogo.destroy)
        boton.pack(side=BOTTOM, padx=20, pady=20)
        self.dialogo.transient(master=self.raiz)
        self.dialogo.grab_set()
        self.raiz.wait_window(self.dialogo)


    def generar_menu(self):
        marco_menu = Frame(self.raiz)
        barra_menus = Menu(marco_menu)

        menu_opciones = Menu(barra_menus, tearoff=0)
        menu_opciones.add_command(label="Aleatorios", command=self.)
        menu_opciones.add_command(label="VQE", command=self.)
        menu_opciones.add_separator()
        menu_opciones.add_command(label="Salir", command=self.raiz.quit())
        barra_menus.add_cascade(label="File", menu=barra_menus)

        #self.marco_menu.config(menu=barra_menus)
        #self.marco_menu.pack()

    def ejecutar_vqe(self):
        pass

    def ejecutar_aleatorios(self):
        pass

    def ayuda(self):
        pass


def main():
    ventana = InterfazDeUsuario()
