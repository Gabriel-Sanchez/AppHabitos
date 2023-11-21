from pomodoro import ventana_pomodoro, lee_habito
from habitos import logica_habitos
from calendario.calendario_habito import habito_calendario
import tkinter as tk
import json

import ctypes



from PIL import Image, ImageTk

# Crea una nueva ventana


def on_mousewheel(event):
    shift = (event.state & 0x1) != 0
    scroll = -1 if event.delta > 0 else 1
    if shift:
        canvas.xview_scroll(scroll, "units")
    else:
        canvas.yview_scroll(scroll, "units")



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

def enviar_seleccion():
    seleccionar_opcion(opciones[var.get()])
    ventana_pomodoro.ventana_pomodoro(opciones[var.get()])
    
def abrir_habito_calendario():
    habito_calendario(opciones[var.get()])

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
opciones = {item['nombre']: { 'id': item['id'], 'type': item['type']  }    for item in data}
print(opciones)

# Función para mostrar el ID cuando se presiona un botón
def mostrar_id(nombre):
    id_seleccionado = opciones[nombre]['id']
    print(opciones[nombre]['type'])
    print(f"Seleccionado: {nombre} (ID: {id_seleccionado})")
    
    if opciones[nombre]['type'] == 1:
        ventana_pomodoro.ventana_pomodoro(id_seleccionado)
    elif opciones[nombre]['type'] == 2:
        pass #otro tipo guardar directamente como hecho en el dia en un nuevo csv 
        
    
    
def abrir_calendario(nombre):
    id_seleccionado = opciones[nombre]['id']
    print(f"Seleccionado22: {nombre} (ID: {id_seleccionado})")
    habito_calendario(id_seleccionado)

root = tk.Tk()

image = Image.open('assets/icon/icon.jpg')

# Convierte la imagen a formato PhotoImage
photo = ImageTk.PhotoImage(image)

root.wm_iconphoto(True, photo)


# lista_habitos = tk.Frame(root, bg='white', relief='raised')
# lista_habitos.pack()


canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)

# Crea un frame dentro del canvas
lista_habitos = tk.Frame(canvas)

# Configura el canvas para que se desplace con la barra de desplazamiento
canvas.configure(yscrollcommand=scrollbar.set)

# Empaqueta el canvas y la barra de desplazamiento
canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Agrega el frame al canvas
canvas.create_window((0,0), window=lista_habitos, anchor="nw")
canvas.bind_all("<MouseWheel>", on_mousewheel)


# Actualiza el scrollregion después de que se haya dibujado el frame
lista_habitos.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))



i = 0
# Crear botones para cada opción en el diccionario
for nombre in opciones.keys():
    label_mover = tk.Label(lista_habitos, text=nombre, bg='#089aff', fg='white')
    label_mover.grid(row=i, column=0, sticky="w", padx=(100,20))
    
    boton = tk.Button(lista_habitos, text="\u23F0", command=lambda n=nombre: mostrar_id(n))
    boton.grid(row=i, column=1, sticky="w", padx=(50,1))
    
    boton_cal = tk.Button(lista_habitos, text="\u25B2", command=lambda n=nombre: abrir_calendario(n))
    boton_cal.grid(row=i, column=2, sticky="w", padx=(1,100))
    i = i + 1
    print(i)




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












root.mainloop()
