import json
# from habitos.logica_habitos import opcion

# Lee el archivo JSON
with open('habitos/lista_habitos.json') as f:
    data = json.load(f)





# Filtrar por el campo "id"
# id_buscado = opcion

def get_times_pomodoro(opcion):
    # Buscar el elemento con el ID específico
    id_buscado = opcion  
    resultado = next((element for element in data if element["id"] == id_buscado), None)

    if resultado:
        work_time = resultado["work_time"]
        short_break = resultado["short_break"]
        count = resultado["count"]
        id = resultado["id"]
        print(work_time)
        return work_time, short_break, count, id
        work_time_input.set(resultado["work_time"])
        # print(f"Para el ID {id_buscado}, el 'work_time' es {work_time} y el 'short_break' es {short_break}")
    else:
        return 0
        # print(f"No se encontró el ID {id_buscado} en los datos proporcionados.")