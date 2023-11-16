from pomodoro import ventana_pomodoro, lee_habito
from habitos import logica_habitos
from calendario.calendario_habito import habito_calendario
import tkinter as tk
import json



def abrir_otra_ventana():
    ventana_pomodoro.ventana_pomodoro(2)
    

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

# Crear diccionario de opciones con nombres como claves e IDs como valores
opciones = {item['nombre']: item['id'] for item in data}

# Crear ventana de Tkinter
root = tk.Tk()

# Crear variable de control para el menú desplegable
var = tk.StringVar(root)

# Crear menú desplegable
opciones_menu = tk.OptionMenu(root, var, *opciones.keys())
opciones_menu.pack()

# Crear botón para enviar selección
boton = tk.Button(root, text="Enviar", command=enviar_seleccion)
boton2 = tk.Button(root, text="calendar", command=abrir_habito_calendario)
boton.pack()
boton2.pack()

root.mainloop()
