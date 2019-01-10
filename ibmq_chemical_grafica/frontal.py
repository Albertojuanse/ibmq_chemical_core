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
        # Se crea la ventana del sistema operativo y se configura
        # self.raiz.geometry("450x450")
        # self.raiz.resizable(width=False, height=False)
        # self.raiz.iconphoto(self.raiz, PhotoImage(file=iconos[0]))
        self.raiz = Tk()
        self.raiz.title("IBMQ Chemical")
        self.raiz.option_add("*Font", "Helvetica 12")
        self.raiz.option_add("-fullscreen", True)
        self.raiz.minsize(400, 300)

        # Se inicializan las variables
        self.molecula = {"driver": "PYSCF",
                         "configuracion":
                             {"properties": {"atom": "Li .0 .0 .0; H .0 .0 1.6",
                                             "unit": "Angstrom",
                                             "charge": 0,
                                             "spin": 0,
                                             "basis": "sto3g"
                                             }
                              }
                         }
        self.problema = {"general": {"tipo_de_mapeo": "parity"},
                         "COBYLA": {"max_eval": 200},
                         "UCCSD": {"profundidad": 1,
                                   "orbitales_activos_ocupados": [0],
                                   "orbitales_activos_no_ocupados": [0, 1],
                                   "numero_de_slices": 1
                                   }
                         }

        self.resultados = {"nombre": "",
                           "resultado": "",
                           "consola": []
                           }
        self.MOL_DRIVER = StringVar(self.raiz, value=self.molecula['driver'])
        self.MOL_ATOM = StringVar(self.raiz, value=self.molecula["configuracion"]["properties"]["atom"])
        self.MOL_UNIT = StringVar(self.raiz, value=self.molecula["configuracion"]["properties"]["unit"])
        self.MOL_CHARGE = StringVar(self.raiz, value=self.molecula["configuracion"]["properties"]["charge"])
        self.MOL_SPIN = StringVar(self.raiz, value=self.molecula["configuracion"]["properties"]["spin"])
        self.MOL_BASIS = StringVar(self.raiz, value=self.molecula["configuracion"]["properties"]["basis"])
        self.PRO_MAPEO = StringVar(self.raiz, value=self.problema["general"]["tipo_de_mapeo"])
        self.PRO_COBYLA_MAXEVAL = StringVar(self.raiz, value=self.problema["COBYLA"]["max_eval"])
        self.PRO_UCCSD_PROF = StringVar(self.raiz, value=self.problema["UCCSD"]["profundidad"])
        self.PRO_UCCSD_OAO = StringVar(self.raiz, value=self.problema["UCCSD"]["orbitales_activos_ocupados"])
        self.PRO_UCCSD_OANO = StringVar(self.raiz, value=self.problema["UCCSD"]["orbitales_activos_no_ocupados"])
        self.PRO_UCCSD_SLICES = StringVar(self.raiz, value=self.problema["UCCSD"]["numero_de_slices"])
        self.RES_NOM = StringVar(self.raiz, value=self.resultados["nombre"])
        self.RES_RES = StringVar(self.raiz, value=self.resultados["resultado"])
        self.RES_CON = StringVar(self.raiz, value=self.resultados["consola"])

        # Se cargan los iconos
        nombres_iconos = ["001.png",
                          "002.png",
                          "003.png",
                          "004.png",
                          "005.png",
                          ]
        self.iconos = interfazsistema.importar_imagenes(nombres_iconos)

        # Se crean los estilos
        fuente_normal = font.Font(weight="bold")
        fuente_negrita = font.Font(weight="bold")

        # Se definen los menús
        barramenu = Menu(self.raiz)
        self.raiz["menu"] = barramenu

        self.menu_opciones = Menu(barramenu)
        self.menu_ayuda = Menu(barramenu)
        barramenu.add_cascade(menu=self.menu_opciones, label="Opciones")
        barramenu.add_cascade(menu=self.menu_ayuda, label="Ayuda")

        self.menu_opciones.add_command(label="Cargar JSON", command=self.cargar_json,
                                       underline=0, accelerator="Alt+v",
                                       compound=LEFT)
        self.menu_opciones.add_separator()
        self.menu_opciones.add_command(label="Cerrar", command=self.raiz.destroy,
                                       underline=0, accelerator="Alt+a",
                                       compound=LEFT)

        self.menu_ayuda.add_command(label="Acerca de", command=self.ayuda,
                                    underline=0, accelerator="Alt+h",
                                    compound=LEFT)
        self.menu_opciones.add_separator()

        # Se define la barra de herramientas
        self.barraherrameintas = Frame(self.raiz, relief=RAISED, bd=2)
        self.boton = Button(self.barraherrameintas, image=PhotoImage(file=self.iconos[4]))

        # Se define la barra de estado
        self.barra_estado = Label(self.raiz, bd=1, relief=SUNKEN, anchor=W)
        self.variable_barra_estado = StringVar(self.barra_estado)
        self.variable_barra_estado.set("Seleccione una opción")
        self.barra_estado.pack(side=LEFT, fill=X)

        # Se definen los elementos de la ventana
        self.elementos = Frame(self.raiz, relief=FLAT, bd=2)
        self.elementos.pack(side=LEFT)
        self.etiq_bienvenida = Label(self.elementos, text="Bienvenido a IBMQ Chemical", font=fuente_negrita)
        self.etiq_info = Label(self.elementos, text="Elija una opción")

        self.MOL_DRIVER_ETIQU = Label(self.elementos, text="MOL_DRIVER")
        self.MOL_DRIVER_ETIQU.grid(row=0, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.MOL_DRIVER_ENTRY = ttk.Entry(self.elementos, textvariable=self.MOL_DRIVER, width=30)
        self.MOL_DRIVER_ENTRY.grid(row=0, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(0, weight=1)
        self.MOL_ATOM_ETIQU = Label(self.elementos, text="MOL_ATOM")
        self.MOL_ATOM_ETIQU.grid(row=1, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.MOL_ATOM_ENTRY = ttk.Entry(self.elementos, textvariable=self.MOL_ATOM, width=30)
        self.MOL_ATOM_ENTRY.grid(row=1, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(1, weight=1)
        self.MOL_UNIT_ETIQU = Label(self.elementos, text="MOL_UNIT")
        self.MOL_UNIT_ETIQU.grid(row=2, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.MOL_UNIT_ENTRY = ttk.Entry(self.elementos, textvariable=self.MOL_UNIT, width=30)
        self.MOL_UNIT_ENTRY.grid(row=2, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(2, weight=1)
        self.MOL_CHARGE_ETIQU = Label(self.elementos, text="MOL_CHARGE")
        self.MOL_CHARGE_ETIQU.grid(row=3, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.MOL_CHARGE_ENTRY = ttk.Entry(self.elementos, textvariable=self.MOL_CHARGE, width=30)
        self.MOL_CHARGE_ENTRY.grid(row=3, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(3, weight=1)
        self.MOL_SPIN_ETIQU = Label(self.elementos, text="MOL_SPIN")
        self.MOL_SPIN_ETIQU.grid(row=4, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.MOL_SPIN_ENTRY = ttk.Entry(self.elementos, textvariable=self.MOL_SPIN, width=30)
        self.MOL_SPIN_ENTRY.grid(row=4, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(4, weight=1)
        self.MOL_BASIS_ETIQU = Label(self.elementos, text="MOL_BASIS")
        self.MOL_BASIS_ETIQU.grid(row=5, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.MOL_BASIS_ENTRY = ttk.Entry(self.elementos, textvariable=self.MOL_BASIS, width=30)
        self.MOL_BASIS_ENTRY.grid(row=5, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(5, weight=1)
        self.PRO_MAPEO_ETIQU = Label(self.elementos, text="PRO_MAPEO")
        self.PRO_MAPEO_ETIQU.grid(row=6, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.PRO_MAPEO_ENTRY = ttk.Entry(self.elementos, textvariable=self.PRO_MAPEO, width=30)
        self.PRO_MAPEO_ENTRY.grid(row=6, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(6, weight=1)
        self.PRO_COBYLA_MAXEVAL_ETIQU = Label(self.elementos, text="PRO_COBYLA_MAXEVAL")
        self.PRO_COBYLA_MAXEVAL_ETIQU.grid(row=7, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.PRO_COBYLA_MAXEVAL_ENTRY = ttk.Entry(self.elementos, textvariable=self.PRO_COBYLA_MAXEVAL, width=30)
        self.PRO_COBYLA_MAXEVAL_ENTRY.grid(row=7, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(7, weight=1)
        self.PRO_UCCSD_PROF_ETIQU = Label(self.elementos, text="PRO_UCCSD_PROF")
        self.PRO_UCCSD_PROF_ETIQU.grid(row=8, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.PRO_UCCSD_PROF_ENTRY = ttk.Entry(self.elementos, textvariable=self.PRO_UCCSD_PROF, width=30)
        self.PRO_UCCSD_PROF_ENTRY.grid(row=8, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(8, weight=1)
        self.PRO_UCCSD_OAO_ETIQU = Label(self.elementos, text="PRO_UCCSD_OAO")
        self.PRO_UCCSD_OAO_ETIQU.grid(row=9, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.PRO_UCCSD_OAO_ENTRY = ttk.Entry(self.elementos, textvariable=self.PRO_UCCSD_OAO, width=30)
        self.PRO_UCCSD_OAO_ENTRY.grid(row=9, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(9, weight=1)
        self.PRO_UCCSD_OANO_ETIQU = Label(self.elementos, text="PRO_UCCSD_OANO")
        self.PRO_UCCSD_OANO_ETIQU.grid(row=10, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.PRO_UCCSD_OANO_ENTRY = ttk.Entry(self.elementos, textvariable=self.PRO_UCCSD_OANO, width=30)
        self.PRO_UCCSD_OANO_ENTRY.grid(row=10, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(10, weight=1)
        self.PRO_UCCSD_SLICES_ETIQU = Label(self.elementos, text="PRO_UCCSD_SLICES")
        self.PRO_UCCSD_SLICES_ETIQU.grid(row=11, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.PRO_UCCSD_SLICES_ENTRY = ttk.Entry(self.elementos, textvariable=self.PRO_UCCSD_SLICES, width=30)
        self.PRO_UCCSD_SLICES_ENTRY.grid(row=11, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(11, weight=1)
        self.RES_BOTON_DEFECTO = ttk.Button(self.elementos, text="Por defecto", command=self.valores_por_defecto)
        self.RES_BOTON_DEFECTO.grid(row=12, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.RES_BOTON_ENVIAR = ttk.Button(self.elementos, text="Enviar", command=self.ejecutar_ibmq_vqe)
        self.RES_BOTON_ENVIAR.grid(row=12, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(12, weight=1)
        self.RES_SEPAR = ttk.Separator(self.elementos, orient=HORIZONTAL)
        self.RES_SEPAR.grid(row=13, columnspan=2, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(13, weight=1)
        self.RES_NOM_ETIQU = Label(self.elementos, text="RES_NOM")
        self.RES_NOM_ETIQU.grid(row=14, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.RES_NOM_ENTRY = ttk.Entry(self.elementos, textvariable=self.RES_NOM, width=30)
        self.RES_NOM_ENTRY.grid(row=14, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(14, weight=1)
        self.RES_RES_ETIQU = Label(self.elementos, text="RES_RES")
        self.RES_RES_ETIQU.grid(row=15, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.RES_RES_ENTRY = ttk.Entry(self.elementos, textvariable=self.RES_RES, width=30)
        self.RES_RES_ENTRY.grid(row=15, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(15, weight=1)
        self.RES_CON_ETIQU = Label(self.elementos, text="RES_CON")
        self.RES_CON_ETIQU.grid(row=16, column=0, padx=5, pady=5, sticky=(N, S, E, W))
        self.RES_CON_ENTRY = ttk.Entry(self.elementos, textvariable=self.RES_CON, width=30)
        self.RES_CON_ENTRY.grid(row=16, column=1, padx=5, pady=5, sticky=(N, S, E, W))
        self.elementos.rowconfigure(16, weight=1)
        self.elementos.columnconfigure(0, weight=1)
        self.elementos.columnconfigure(1, weight=1)

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

    def abrir(self):
        self.dialogo = Toplevel()
        self.dialogo.title("Configuración")
        boton = ttk.Button(self.dialogo, text="Cerrar", command=self.dialogo.destroy)
        boton.pack(side=BOTTOM, padx=20, pady=20)
        self.dialogo.transient(master=self.raiz)
        self.dialogo.grab_set()
        self.raiz.wait_window(self.dialogo)

    def cargar_json(self):
        pass

    def valores_por_defecto(self):
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
        self.MOL_DRIVER.set(molecula['driver'])
        self.MOL_ATOM.set(molecula["configuracion"]["properties"]["atom"])
        self.MOL_UNIT.set(molecula["configuracion"]["properties"]["unit"])
        self.MOL_CHARGE.set(molecula["configuracion"]["properties"]["charge"])
        self.MOL_SPIN.set(molecula["configuracion"]["properties"]["spin"])
        self.MOL_BASIS.set(molecula["configuracion"]["properties"]["basis"])
        self.PRO_MAPEO.set(problema["general"]["tipo_de_mapeo"])
        self.PRO_COBYLA_MAXEVAL.set(problema["COBYLA"]["max_eval"])
        self.PRO_UCCSD_PROF.set(problema["UCCSD"]["profundidad"])
        self.PRO_UCCSD_OAO.set(problema["UCCSD"]["orbitales_activos_ocupados"])
        self.PRO_UCCSD_OANO.set(problema["UCCSD"]["orbitales_activos_no_ocupados"])
        self.PRO_UCCSD_SLICES.set(problema["UCCSD"]["numero_de_slices"])
        self.RES_NOM.set(resultados["nombre"])
        self.RES_RES.set(resultados["resultado"])
        self.RES_CON.set(resultados["consola"])

    def ejecutar_ibmq_vqe(self):
        self.molecula['driver'] = self.MOL_DRIVER.get()
        self.molecula["configuracion"]["properties"]["atom"] = self.MOL_ATOM.get()
        self.molecula["configuracion"]["properties"]["unit"] = self.MOL_UNIT.get()
        self.molecula["configuracion"]["properties"]["charge"] = int(self.MOL_CHARGE.get())
        self.molecula["configuracion"]["properties"]["spin"] = int(self.MOL_SPIN.get())
        self.molecula["configuracion"]["properties"]["basis"] = self.MOL_BASIS.get()
        self.problema["general"]["tipo_de_mapeo"] = self.PRO_MAPEO.get()
        self.problema["COBYLA"]["max_eval"] = int(self.PRO_COBYLA_MAXEVAL.get())
        self.problema["UCCSD"]["profundidad"] = int(self.PRO_UCCSD_PROF.get())

        valor_usuario = self.PRO_UCCSD_OAO.get()
        valor = []
        for elemento in valor_usuario:
            if not elemento == " " and not elemento == "(" and not elemento == ")" and not elemento == ",":
                valor.append(int(elemento))
        self.problema["UCCSD"]["orbitales_activos_ocupados"] = valor

        valor_usuario = self.PRO_UCCSD_OANO.get()
        valor = []
        for elemento in valor_usuario:
            if not elemento == " " and not elemento == "(" and not elemento == ")" and not elemento == ",":
                valor.append(int(elemento))
        self.problema["UCCSD"]["orbitales_activos_no_ocupados"] = valor

        self.problema["UCCSD"]["numero_de_slices"] = int(self.PRO_UCCSD_SLICES.get())
        self.RES_NOM.set(self.resultados["nombre"])
        self.RES_RES.set(self.resultados["resultado"])
        self.RES_CON.set(self.resultados["consola"])

        zaga.ejecutar_ibmq_vqe(self.molecula, self.problema, self)

    def mostrar_resultados(self, resultados):
        if not self.resultados["nombre"] == resultados["nombre"]:
            self.resultados = resultados
            self.RES_NOM.set(self.resultados["nombre"])
            self.RES_RES.set(self.resultados["resultado"])
            self.RES_CON.set(self.resultados["consola"])
        else:
            self.resultados = {"nombre": "Sin nombre",
                               "resultado": "Sin resultados",
                               "consola": []
                               }
            self.RES_NOM.set(self.resultados["nombre"])
            self.RES_RES.set(self.resultados["resultado"])
            self.RES_CON.set(self.resultados["consola"])

    def ejecutar_aleatorios(self):
        pass

    def ayuda(self):
        pass


def main():
    ventana = InterfazDeUsuario()
