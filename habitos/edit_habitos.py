import json
from tkinter import *
import main

# Primero, lee el archivo JSON
with open('habitos/lista_habitos.json', 'r') as f:
    data = json.load(f)

def convert_to_number(value):
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

def get_obj_by_id(id):
    for obj in data:
        if obj['id'] == id:
            return obj
    return None

def create_edit_window(obj):
    window = Tk()
    window.title("Editar objeto")

    entries = {}
    for key in obj:
        label = Label(window, text=key)
        label.pack()
        entry = Entry(window)
        entry.insert(0, obj[key])
        entry.pack()
        entries[key] = entry

    def save_changes():
        for key in obj:
            obj[key] = convert_to_number(entries[key].get())
        save_json()
        window.destroy()

    save_button = Button(window, text="Guardar", command=save_changes)
    save_button.pack()

    window.mainloop()

def save_json():
    with open('habitos/lista_habitos.json', 'w') as f:
        json.dump(data, f)

def editar_habito(id_habito):
    obj = get_obj_by_id(id_habito)
    if obj is not None:
        create_edit_window(obj)