from pomodoro import ventana_pomodoro, lee_habito
from habitos import logica_habitos, edit_habitos
from calendario.calendario_habito import habito_calendario, habito_calendario_check
from registros.CRUD_registros import save_daily_habit, verify_daily_habit, verify_daily_habit_pomodoro
import tkinter as tk
import json

import ctypes



# from PIL import Image, ImageTk
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
        

    def center_window(root, width=500, height=200):
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

    
    def ordenar_lista():
        global opciones
        with open('habitos/lista_habitos.json', 'r') as f:
            data = json.load(f)
        opciones = {item['nombre']: { 'id': item['id'], 'type': item['type'], 'orden_n': item['orden_n'] }    for item in data}
        sorted_data = sorted(data, key=lambda item: item['orden_n'])

        # Now, create your dictionary
        opciones = {item['nombre']: {'id': item['id'], 'type': item['type'], 'orden_n': item['orden_n']} for item in sorted_data}
        
    ordenar_lista()


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

    canvas = tk.Canvas(root)
    scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

    # Crea un frame dentro del canvas
    lista_habitos = tk.Frame(canvas)

    # Configura el canvas para que se desplace con la barra de desplazamiento
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.config(width=800)

    
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

    
    
    
    canvas3 = tk.Canvas(root)
    scrollbar3 = tk.Scrollbar(root, orient="vertical", command=canvas3.yview)


    frame = tk.Frame(canvas3)

    canvas3.configure(yscrollcommand=scrollbar3.set)
    canvas3.config(width=800)
    
    canvas3.grid(row=2, column=0, sticky="nsew")
    scrollbar3.grid(row=2, column=1, sticky="ns")

    canvas3.create_window((0,0), window=frame, anchor="nw")
 

    frame.bind("<Configure>", lambda e: canvas3.configure(scrollregion=canvas3.bbox("all")))
    

    
    frame_botones = tk.Frame(root)
    frame_botones.grid(row=1, column=0 )
    button = tk.Button(frame_botones, text="hechos", command=toggle)

    button.grid(row=1, column=0 )


    def limpiar():
        for widget in lista_habitos.winfo_children():
            widget.destroy()

    labels = []
    botones = []
    botones_cal = []
    botones_edit = []



    def llenar_lista():
        
        global opciones

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
            
            label_mover.grid(row=i, column=0,sticky='ew', ipadx=35, padx=(100,20))
            boton.grid(row=i, column=1, sticky="w", padx=(1,1))
            boton_cal.grid(row=i, column=2, sticky="w", padx=(1,1))
            boton_edit.grid(row=i, column=3, sticky="w", padx=(1,2))
            
            labels.append(label_mover)
            botones.append(boton)
            botones_cal.append(boton_cal)
            botones_edit.append(boton_edit)
        
        
        # i = i + 1
    llenar_lista()
        
    def actualiza_listas():
        for i, nombre in enumerate(opciones.keys()):
            if opciones[nombre]['type'] == 1:
                color = "#089aff"
                icono = "\u23F0"
                hecho_diario = verify_daily_habit_pomodoro(opciones[nombre]['id'])
            elif opciones[nombre]['type'] == 2:
                color = "#73c977"
                icono = "\u2714"
                hecho_diario = verify_daily_habit(opciones[nombre]['id'])
                
            if hecho_diario:
                label_mover = tk.Label(frame, text=nombre, bg=color, fg='white')
                label_mover.grid(row=i, column=0,sticky='ew', ipadx=35, padx=(100,20))
                
                boton = tk.Button(frame, text="\u23F0", command=lambda n=nombre: mostrar_id(n))
                boton.grid(row=i, column=1, sticky="w", padx=(1,1))
                
                boton_cal = tk.Button(frame, text="\U0001F4CA", command=lambda n=nombre: abrir_calendario(n))
                boton_cal.grid(row=i, column=2, sticky="w", padx=(1,1))
                
                boton_edit = tk.Button(frame, text="\u270E", command=lambda n=nombre: abrir_editar_habito_pom(n))
                boton_edit.grid(row=i, column=3, sticky="w", padx=(1,2))
                
                
                
                labels[i].grid_remove()
                botones[i].grid_remove()
                botones_cal[i].grid_remove()
                botones_edit[i].grid_remove()
        
    actualiza_listas()
            

    center_window(root, 600, 400)


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
        next_orden_n = max(item['orden_n'] for item in data) + 1
        
        # Especificar los campos permitidos
        allowed_fields = ['nombre', 'work_time', 'short_break', 'count', 'type']
        
        # Crear campos de entrada solo para las claves permitidas
        entries = {}
        for key in allowed_fields:
            tk.Label(new_window, text=key).pack()
            entries[key] = tk.Entry(new_window)
            entries[key].pack()
        
        # Función para agregar los datos ingresados a la lista de datos
        def submit():
            new_entry = {'id': next_id, 'orden_n': next_orden_n}
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


    # Botón para abrir la ventana de agregar datos
    tk.Button(frame_botones, text="Agregar", command=add_data).grid(row=1, column=1 )



 
        # Crear una nueva ventana si no existe
    def show_data():
        global new_window
        # Crear una nueva ventana si no existe
        if 'new_window' not in globals() or not new_window.winfo_exists():
            new_window = tk.Toplevel(root)
        
        # Limpiar la ventana
        for widget in new_window.winfo_children():
            widget.destroy()
            
        # for widget in root.winfo_children():
        #     widget.destroy()
        
        # Cargar los datos y ordenarlos por 'orden_n'
        data = sorted(load_data(), key=lambda x: x['orden_n'])
        
        # Función para mover un elemento hacia arriba o hacia abajo
        def move(i, direction):
            # Intercambiar 'orden_n' con el elemento de arriba/abajo
            data[i]['orden_n'], data[i + direction]['orden_n'] = data[i + direction]['orden_n'], data[i]['orden_n']
            # Guardar los datos
            save_data(data)
            # Recargar la ventana
            show_data()
            limpiar()
            ordenar_lista()
            llenar_lista()
        
        # Mostrar todos los elementos
        for i, item in enumerate(data):
            tk.Label(new_window, text=item['nombre']).grid(row=i,column=2)
            # Botón para mover el elemento hacia arriba (si no es el primero)
            if i > 0:
                tk.Button(new_window, text="↑", command=lambda i=i: move(i, -1)).grid(row=i,column=0)
            # Botón para mover el elemento hacia abajo (si no es el último)
            if i < len(data) - 1:
                tk.Button(new_window, text="↓", command=lambda i=i: move(i, 1)).grid(row=i,column=1)
    
    def actualizar_v():
        limpiar()
        ordenar_lista()
        llenar_lista()

    tk.Button(frame_botones, text="Ordenar", command=show_data).grid(row=1, column=2 )
    tk.Button(frame_botones, text="Actualizar", command=actualizar_v).grid(row=1, column=3 )
    
    root.iconbitmap('assets/icon/icon.ico')

    root.mainloop()



if __name__ == "__main__":
    ventana_main()
    
    # import matplotlib.pyplot as plt
    # import pandas as pd
    
    # df = pd.read_csv('registros/historial_habitos.csv')

    # df['fecha'] = pd.to_datetime(df['fecha'])

    # # Convertir 'duracion' a timedelta
    # df['duracion'] = pd.to_timedelta(df['duracion'])

    # # Crear un subgráfico para cada id de hábito
    # fig, axs = plt.subplots(df['id_habito'].nunique(), 1, sharex=True, figsize=(10, 10))

    # for ax, (id_habito, df_id) in zip(axs, df.groupby('id_habito')):
    #     ax.plot(df_id['fecha'], df_id['duracion'], label=f'ID Hábito {id_habito}')
    #     ax.set_ylabel('Duración')
    #     ax.legend()

    # axs[-1].set_xlabel('Fecha')

    # plt.tight_layout()
    # plt.show()