from pomodoro import ventana_pomodoro, lee_habito
from habitos import logica_habitos, edit_habitos
from calendario.calendario_habito import habito_calendario, habito_calendario_check
from registros.CRUD_registros import save_daily_habit, verify_daily_habit, verify_daily_habit_pomodoro
import tkinter as tk
import json

import ctypes



from PIL import Image, ImageTk
    # Crea una nueva ventana
def ventana_main():

    def on_mousewheel(event):
        shift = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        if shift:
            canvas.xview_scroll(scroll, "units")
        else:
            canvas.yview_scroll(scroll, "units")
    def on_mousewheel_scroll_hecho(event):
        shift = (event.state & 0x1) != 0
        scroll = -1 if event.delta > 0 else 1
        if shift:
            canvas3.xview_scroll(scroll, "units")
        else:
            canvas3.yview_scroll(scroll, "units")



    # Función para ocultar botones de minimizar y cerrar
    def ocultar_botones():
        # Obtener el identificador de la ventana principal
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        # Ocultar botones de minimizar y cerrar
        style = ctypes.windll.user32.GetWindowLongW(hwnd, -16)
        ctypes.windll.user32.SetWindowLongW(hwnd, -16, style & ~0xC00000)


    topmost = False
    def mantener_en_primero():
        global topmost
        topmost = not topmost
        
        root.attributes("-topmost", topmost)
        root.lift()
        
        


    def abrir_otra_ventana():
        ventana_pomodoro.ventana_pomodoro(2)
        

    def center_window(root, width=300, height=200):
        # Obtiene las dimensiones de la pantalla
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calcula la posición del centro
        center_x = (screen_width // 2) - (width // 2)
        center_y = (screen_height // 2) - (height // 2)

        # Centra la ventana
        root.geometry(f'{width}x{height}+{center_x}+{center_y}')

    def seleccionar_opcion(id):
        print(f"Opción seleccionada: {id}")

    # def enviar_seleccion():
    #     seleccionar_opcion(opciones[var.get()])
    #     ventana_pomodoro.ventana_pomodoro(opciones[var.get()])
        
    # def abrir_habito_calendario():
    #     habito_calendario(opciones[var.get()])

    # Leer opciones de archivo JSON
    with open('habitos/lista_habitos.json', 'r') as f:
        data = json.load(f)

    # # Crear diccionario de opciones con nombres como claves e IDs como valores
    # opciones = {item['nombre']: item['id'] for item in data}

    # # Crear ventana de Tkinter
    # root = tk.Tk()

    # # Crear variable de control para el menú desplegable
    # var = tk.StringVar(root)

    # # Crear menú desplegable
    # opciones_menu = tk.OptionMenu(root, var, *opciones.keys())
    # opciones_menu.pack()


    # Crear diccionario de opciones con nombres como claves e IDs como valores
    opciones = {item['nombre']: { 'id': item['id'], 'type': item['type'], 'orden_n': item['orden_n'] }    for item in data}
    # print(opciones)
    # Sort the data based on 'orden_n'
    sorted_data = sorted(data, key=lambda item: item['orden_n'])

    # Now, create your dictionary
    opciones = {item['nombre']: {'id': item['id'], 'type': item['type'], 'orden_n': item['orden_n']} for item in sorted_data}


    # Función para mostrar el ID cuando se presiona un botón
    def mostrar_id(nombre):
        id_seleccionado = opciones[nombre]['id']
        print(opciones[nombre]['type'])
        print(f"Seleccionado: {nombre} (ID: {id_seleccionado})")
        
        if opciones[nombre]['type'] == 1:
            root.destroy()
            ventana_pomodoro.ventana_pomodoro(id_seleccionado)
        elif opciones[nombre]['type'] == 2:
            save_daily_habit(id_seleccionado)
            actualiza_listas()
            #otro tipo guardar directamente como hecho en el dia en un nuevo csv 
            
        
        
    def abrir_calendario(nombre):
        id_seleccionado = opciones[nombre]['id']
        print(f"Seleccionado22: {nombre} (ID: {id_seleccionado})")
        if opciones[nombre]['type'] == 1:
            habito_calendario(id_seleccionado)
        elif opciones[nombre]['type'] == 2:
            habito_calendario_check(id_seleccionado)
    
    def abrir_editar_habito_pom(nombre):
        id_seleccionado = opciones[nombre]['id']
        edit_habitos.editar_habito(id_seleccionado)

    root = tk.Tk()

    # image = Image.open('assets/icon/icon.jpg')

    # # Convierte la imagen a formato PhotoImage
    # photo = ImageTk.PhotoImage(image)

    # root.wm_iconphoto(True, photo)
    
    # image = Image.open('assets/icon/icon.jpg')
    # photo = ImageTk.PhotoImage(image)
    # # Guarda una referencia a la imagen en el objeto de la ventana
    # root.icon_photo = photo
    # root.wm_iconphoto(True, root.icon_photo)


    # lista_habitos = tk.Frame(root, bg='white', relief='raised')
    # lista_habitos.pack()


    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

    # Crea un frame dentro del canvas
    lista_habitos = tk.Frame(canvas)

    # Configura el canvas para que se desplace con la barra de desplazamiento
    canvas.configure(yscrollcommand=scrollbar.set)

    # Empaqueta el canvas y la barra de desplazamiento
    # canvas.pack(side="left", fill="both", expand=True)
    # scrollbar.pack(side="right", fill="y")
    
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")
    

    # Agrega el frame al canvas
    canvas.create_window((0,0), window=lista_habitos, anchor="nw")
    canvas.bind_all("<MouseWheel>", on_mousewheel)


    # Actualiza el scrollregion después de que se haya dibujado el frame
    lista_habitos.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))









    def toggle():
        if frame.winfo_viewable():
            # frame.grid_remove()
            canvas3.grid_remove()
            # frame.pack_forget()
   
            scrollbar3.grid_remove()
        else:
            canvas3.grid(row=2, column=0, sticky="nsew")
            scrollbar3.grid(row=2, column=1, sticky="ns")
            # Redibuja el Frame en el Canvas
            # canvas2.create_window((0, 0), window=frame, anchor="nw")
            # frame.update_idletasks()
            # canvas2.config(scrollregion=canvas2.bbox("all"))
            # # frame.grid(row=2, column=0 , sticky="nsew" ) 
            # canvas2.grid(row=2, column=0, sticky="nsew")
            # scrollbar2.grid(row=2, column=1, sticky="ns")
            # frame.update_idletasks()
            # canvas2.config(scrollregion=canvas2.bbox("all"))

            # frame.pack()

    # Crea un frame
    
    
   
    # canvas2 = tk.Canvas(root)
    # scrollbar2 = tk.Scrollbar(root, orient="vertical", command=canvas2.yview)
    # canvas2.configure(yscrollcommand=scrollbar2.set)
    # # frame2 = tk.Frame(canvas2)
    # canvas2.create_window((0, 0), window=frame, anchor="nw")
    
    
    
    # frame.bind("<Configure>", lambda e: canvas2.configure(scrollregion=canvas2.bbox("all")))
    
    
    
    canvas3 = tk.Canvas(root)
    scrollbar3 = tk.Scrollbar(root, orient="vertical", command=canvas3.yview)

    # lista_habitos = tk.Frame(canvas3)
    frame = tk.Frame(canvas3)

    canvas3.configure(yscrollcommand=scrollbar3.set)
    
    canvas3.grid(row=2, column=0, sticky="nsew")
    scrollbar3.grid(row=2, column=1, sticky="ns")

    canvas3.create_window((0,0), window=frame, anchor="nw")
    # canvas3.bind_all("<MouseWheel>", on_mousewheel_scroll_hecho)

    frame.bind("<Configure>", lambda e: canvas3.configure(scrollregion=canvas3.bbox("all")))
    
    
    
    
    

    # Crea algunos widgets en el frame
    # for i in range(10):
    #     # tk.Label(frame, text="Label %s" % i).grid(row=i)
    #     tk.Label(frame, text="Label %s" % i).pack()

    # Crea un botón que muestre u oculte el frame
    button = tk.Button(root, text="hechos", command=toggle)
    # button.grid()
    # button.pack()
    button.grid(row=1, column=0 )



    labels = []
    botones = []
    botones_cal = []
    botones_edit = []






    i = 0
    # Crear botones para cada opción en el diccionario
    for i, nombre in enumerate(opciones.keys()):
        if opciones[nombre]['type'] == 1:
            color = "#089aff"
            icono = "\u23F0"
            hecho_diario = verify_daily_habit_pomodoro(opciones[nombre]['id'])
            
            
        elif opciones[nombre]['type'] == 2:
            color = "#73c977"
            icono = "\u2714"
            hecho_diario = verify_daily_habit(opciones[nombre]['id'])
            
        
        label_mover = tk.Label(lista_habitos, text=nombre, bg=color, fg='white')
        boton = tk.Button(lista_habitos, text=icono, command=lambda n=nombre: mostrar_id(n))
        boton_cal = tk.Button(lista_habitos, text="\U0001F4CA", command=lambda n=nombre: abrir_calendario(n))
        boton_edit = tk.Button(lista_habitos, text="\u270E", command=lambda n=nombre: abrir_editar_habito_pom(n))
        
        label_mover.grid(row=i, column=0, sticky="w", padx=(100,20))
        boton.grid(row=i, column=1, sticky="w", padx=(50,1))
        boton_cal.grid(row=i, column=2, sticky="w", padx=(1,1))
        boton_edit.grid(row=i, column=3, sticky="w", padx=(1,2))
        
        labels.append(label_mover)
        botones.append(boton)
        botones_cal.append(boton_cal)
        botones_edit.append(boton_edit)
        
        
        # i = i + 1
        
    def actualiza_listas():
        for i, nombre in enumerate(opciones.keys()):
            if opciones[nombre]['type'] == 1:
                hecho_diario = verify_daily_habit_pomodoro(opciones[nombre]['id'])
            elif opciones[nombre]['type'] == 2:
                hecho_diario = verify_daily_habit(opciones[nombre]['id'])
                
            if hecho_diario:
                label_mover = tk.Label(frame, text=nombre, bg=color, fg='white')
                label_mover.grid(row=i, column=0, sticky="w", padx=(100,20))
                
                boton = tk.Button(frame, text="\u23F0", command=lambda n=nombre: mostrar_id(n))
                boton.grid(row=i, column=1, sticky="w", padx=(50,1))
                
                boton_cal = tk.Button(frame, text="\U0001F4CA", command=lambda n=nombre: abrir_calendario(n))
                boton_cal.grid(row=i, column=2, sticky="w", padx=(1,5))
                
                boton_edit = tk.Button(frame, text="\u270E", command=lambda n=nombre: abrir_editar_habito_pom(n))
                boton_edit.grid(row=i, column=3, sticky="w", padx=(1,5))
                
                
                
                labels[i].grid_remove()
                botones[i].grid_remove()
                botones_cal[i].grid_remove()
                botones_edit[i].grid_remove()
        
    actualiza_listas()
            
    #     if hecho_diario:
    #         label_mover = tk.Label(frame, text=nombre, bg=color, fg='white')
    #         label_mover.grid(row=i, column=0, sticky="w", padx=(100,20))
            
    #         boton = tk.Button(frame, text="\u23F0", command=lambda n=nombre: mostrar_id(n))
    #         boton.grid(row=i, column=1, sticky="w", padx=(50,1))
            
    #         boton_cal = tk.Button(frame, text="\u25B2", command=lambda n=nombre: abrir_calendario(n))
    #         boton_cal.grid(row=i, column=2, sticky="w", padx=(1,100))


    # for i, nombre in enumerate(opciones.keys()):
    #     if opciones[nombre]['type'] == 1:
    #         hecho_diario = verify_daily_habit_pomodoro(opciones[nombre]['id'])
    #     elif opciones[nombre]['type'] == 2:
    #         hecho_diario = verify_daily_habit(opciones[nombre]['id'])
            
    #     if not hecho_diario:
    #         labels[i].grid(row=i, column=0, sticky="w", padx=(100,20))
    #         botones[i].grid(row=i, column=1, sticky="w", padx=(50,1))
    #         botones_cal[i].grid(row=i, column=2, sticky="w", padx=(1,100))
    #     else:
    #         labels[i].grid_remove()
    #         botones[i].grid_remove()
    #         botones_cal[i].grid_remove()
            
    #     if hecho_diario:
    #         label_mover = tk.Label(frame, text=nombre, bg=color, fg='white')
    #         label_mover.grid(row=i, column=0, sticky="w", padx=(100,20))
            
    #         boton = tk.Button(frame, text="\u23F0", command=lambda n=nombre: mostrar_id(n))
    #         boton.grid(row=i, column=1, sticky="w", padx=(50,1))
            
    #         boton_cal = tk.Button(frame, text="\u25B2", command=lambda n=nombre: abrir_calendario(n))
    #         boton_cal.grid(row=i, column=2, sticky="w", padx=(1,100))


        




    # # Crear botón para enviar selección
    # boton = tk.Button(root, text="Enviar", command=enviar_seleccion)
    # boton2 = tk.Button(root, text="calendar", command=abrir_habito_calendario)
    # boton.pack()
    # boton2.pack()

    # btn_mantener = tk.Button(root, text="Mantener en Primero", command=mantener_en_primero)
    # btn_mantener.pack(pady=20)

    center_window(root, 500, 400)



    # # Obtener el ancho y alto de la pantalla
    # ancho_pantalla = root.winfo_screenwidth()
    # alto_pantalla = root.winfo_screenheight()

    # # Definir las dimensiones de la ventana
    # ancho_ventana = 300
    # alto_ventana = 200

    # # Calcular la posición para la esquina inferior derecha
    # posicion_x = ancho_pantalla - ancho_ventana
    # posicion_y = alto_pantalla - alto_ventana

    # # Establecer la geometría de la ventana
    # root.geometry(f"{ancho_ventana}x{alto_ventana}+{posicion_x}+{posicion_y}")





    # # Eliminar bordes y barra superior
    # root.overrideredirect(True)

    # # Definir las dimensiones de la ventana
    # ancho_ventana = 400
    # alto_ventana = 300

    # # Establecer la geometría de la ventana
    # root.geometry(f"{ancho_ventana}x{alto_ventana}")

    # # Función para cerrar la ventana
    # def cerrar_ventana():
    #     root.destroy()

    # # Botón para cerrar la ventana
    # btn_cerrar = tk.Button(root, text="Cerrar", command=cerrar_ventana)
    # btn_cerrar.pack()









    # import tkinter as tk

    # def start_move(event):
    #     root.startX = event.x
    #     root.startY = event.y

    # def stop_move(event):
    #     root.startX = None
    #     root.startY = None

    # def do_move(event):
    #     dx = event.x - root.startX
    #     dy = event.y - root.startY
    #     x = root.winfo_x() + dx
    #     y = root.winfo_y() + dy
    #     root.geometry(f"+{x}+{y}")


    # root.overrideredirect(True)  # Elimina la barra de título

    # # Crea un marco en la parte superior para mover la ventana
    # move_frame = tk.Frame(root, height=20, bg="blue")
    # move_frame.pack(fill=tk.X)

    # move_frame.bind("<ButtonPress-1>", start_move)
    # move_frame.bind("<ButtonRelease-1>", stop_move)
    # move_frame.bind("<B1-Motion>", do_move)

    # content_frame = tk.Frame(root, bg="white")
    # content_frame.pack(fill=tk.BOTH, expand=True)

    # label = tk.Label(content_frame, text="Haz clic y arrastra la parte azul para mover")
    # label.pack()

    # # Función para cerrar la ventana
    # def cerrar_ventana():
    #     root.destroy()

    # # Botón para cerrar la ventana
    # btn_cerrar = tk.Button(root, text="Cerrar", command=cerrar_ventana)
    # btn_cerrar.pack()



    def load_data():
        with open('habitos/lista_habitos.json', 'r') as f:
            return json.load(f)

    def save_data(data):
        with open('habitos/lista_habitos.json', 'w') as f:
            json.dump(data, f, indent=4)

    def add_data():
        # Crear una nueva ventana
        new_window = tk.Toplevel(root)
        
        # Cargar los datos
        data = load_data()
        
        # Calcular el próximo ID
        next_id = max(item['id'] for item in data) + 1
        
        # Especificar los campos permitidos
        allowed_fields = ['nombre', 'work_time', 'short_break', 'count', 'type', 'orden_n']
        
        # Crear campos de entrada solo para las claves permitidas
        entries = {}
        for key in allowed_fields:
            tk.Label(new_window, text=key).pack()
            entries[key] = tk.Entry(new_window)
            entries[key].pack()
        
        # Función para agregar los datos ingresados a la lista de datos
        def submit():
            new_entry = {'id': next_id}
            for key, entry in entries.items():
                value = entry.get()
                # Convertir a int si es posible, de lo contrario dejar como texto
                try:
                    value = int(value)
                except ValueError:
                    pass
                new_entry[key] = value
            data.append(new_entry)
            save_data(data)  # Guardar los datos en el archivo .json
            new_window.destroy()
        
        # Botón para enviar los datos
        tk.Button(new_window, text="Submit", command=submit).pack()






    root.mainloop()



if __name__ == "__main__":
    ventana_main()