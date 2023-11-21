import pandas as pd
from datetime import datetime

def save_daily_habit(id_habito):
    hoy = datetime.now().date()
    df = pd.read_csv('registros/check_historial_habitos.csv')
    df['fecha_hora'] = pd.to_datetime(df['fecha_hora'])
    
    # if hoy not in df.loc[df['id_habito'] == id_habito, 'fecha_hora'].dt.date.values:
    #     nueva_fila = {'id_habito': id_habito, 'fecha_hora': hoy, 'hecho': 1}
    #     df = df.append(nueva_fila, ignore_index=True)
    
    if hoy not in df.loc[df['id_habito'] == id_habito, 'fecha_hora'].dt.date.values:
        nueva_fila = pd.DataFrame({'id_habito': [id_habito], 'fecha_hora': [hoy], 'hecho': [1]})
        df = pd.concat([df, nueva_fila], ignore_index=True)
        df.to_csv('registros/check_historial_habitos.csv', index=False)
    


def format_timedelta(td):
    #print(td)
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes}:{seconds}"


def guardar_datos(id_habito, df, campo, dato):
    hoy = datetime.now().date()
       
    df[campo] = pd.to_timedelta(df[campo])

    
    tiempo_habito = pd.to_timedelta(dato, unit='s')

   
    # df.loc[(df['fecha'].dt.date == hoy) & (df['id_habito'] == id_habito), 'duracion'] += tiempo_habito
    
    mask = (df['fecha'].dt.date == hoy) & (df['id_habito'] == id_habito)
    df.loc[mask, campo] = df.loc[mask, campo] + tiempo_habito


    
    df['duracion'] = df['duracion'].apply(format_timedelta)
    return df

def registrar_habito_descanso(id_habito, tiempo_habito_descanso):
    
    df = pd.read_csv('registros/historial_habitos.csv')

    df['fecha'] = pd.to_datetime(df['fecha'])

    hoy = datetime.now().date()

    df['duracion_descanso'] = pd.to_timedelta(df['duracion_descanso'])

    tiempo_habito_descanso = pd.to_timedelta(tiempo_habito_descanso, unit='s')

    mask = (df['fecha'].dt.date == hoy) & (df['id_habito'] == id_habito)
    df.loc[mask, 'duracion_descanso'] = df.loc[mask, 'duracion_descanso'] + tiempo_habito_descanso
    
    df['duracion_descanso'] = df['duracion_descanso'].apply(format_timedelta)

    if hoy not in df.loc[df['id_habito'] == id_habito, 'fecha'].dt.date.values:
        nueva_fila = {'id_habito': id_habito, 'fecha': hoy, 'duracion_descanso': tiempo_habito_descanso}
        df = df.append(nueva_fila, ignore_index=True)

    df.to_csv('registros/historial_habitos.csv', index=False)
    
    
def registrar_habito(id_habito, tiempo_habito):
    
    df = pd.read_csv('registros/historial_habitos.csv')

    df['fecha'] = pd.to_datetime(df['fecha'])

    hoy = datetime.now().date()

    df['duracion'] = pd.to_timedelta(df['duracion'])

    tiempo_habito = pd.to_timedelta(tiempo_habito, unit='s')

    mask = (df['fecha'].dt.date == hoy) & (df['id_habito'] == id_habito)
    df.loc[mask, 'duracion'] = df.loc[mask, 'duracion'] + tiempo_habito

    df['duracion'] = df['duracion'].apply(format_timedelta)


    if hoy not in df.loc[df['id_habito'] == id_habito, 'fecha'].dt.date.values:
        nueva_fila = {'id_habito': id_habito, 'fecha': hoy, 'duracion': tiempo_habito}
        df = df.append(nueva_fila, ignore_index=True)


    df.to_csv('registros/historial_habitos.csv', index=False)


    
def registrar_Inicio_habito(id_habito):
    

   
    df = pd.read_csv('registros/historial_habitos.csv')

 
    df['fecha'] = pd.to_datetime(df['fecha'])

   
    hoy = datetime.now().date()
    print(hoy)
    hora = datetime.now().time().strftime('%H:%M:%S')
    
    print(hora)

    
    # df['duracion'] = pd.to_numeric(df['duracion'])
    
    # if start_timer:
    #     df.loc[(df['fecha'].dt.date == hoy) & (df['id_habito'] == id_habito), 'start_timer'] = hora
    # elif end_timer:
    #     df.loc[(df['fecha'].dt.date == hoy) & (df['id_habito'] == id_habito), 'end_timer'] = hora


   



    
    if hoy not in df.loc[df['id_habito'] == id_habito, 'fecha'].dt.date.values:
        print(hora)
        nueva_fila = pd.DataFrame({'id_habito': [id_habito], 'fecha': [hoy], 'duracion': [0], 'start_timer': [hora], 'end_timer':[0],
                                   'duracion_descanso': [0]})
        df = pd.concat([df, nueva_fila], ignore_index=True)
        # nueva_fila = {'id_habito': id_habito, 'fecha': hoy, 'duracion': 0,  'start_timer': hora, 'end_timer':0}
        # df = df.append(nueva_fila, ignore_index=True)



    
    df.to_csv('registros/historial_habitos.csv', index=False)




def registrar_Fin_habito(id_habito):
    

    
    df = pd.read_csv('registros/historial_habitos.csv')

    
    df['fecha'] = pd.to_datetime(df['fecha'])

 
    hoy = datetime.now().date()
    hora = datetime.now().time().strftime('%H:%M:%S')

 
    # df['duracion'] = pd.to_numeric(df['duracion'])
    df.loc[(df['fecha'].dt.date == hoy) & (df['id_habito'] == id_habito), 'end_timer'] = hora
    
    # if start_timer:
    #     df.loc[(df['fecha'].dt.date == hoy) & (df['id_habito'] == id_habito), 'start_timer'] = hora
    # elif end_timer:
    #     df.loc[(df['fecha'].dt.date == hoy) & (df['id_habito'] == id_habito), 'end_timer'] = hora






   
    # if hoy not in df.loc[df['id_habito'] == id_habito, 'fecha'].dt.date.values:
    #     if start_timer:
    #         nueva_fila = {'id_habito': id_habito, 'fecha': hoy, 'duracion': 0,  'start_timer': hora, 'end_timer':0}
    #         df = df.append(nueva_fila, ignore_index=True)
    #     elif end_timer:
    #         df.loc[(df['fecha'].dt.date == hoy) & (df['id_habito'] == id_habito), 'end_timer'] = hora


  
    df.to_csv('registros/historial_habitos.csv', index=False)