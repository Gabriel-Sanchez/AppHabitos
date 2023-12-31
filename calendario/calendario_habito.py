import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# import matplotlib.colors as colors
from matplotlib.colors import ListedColormap
import json


    
def center_figure(fig):
    # Obtiene el administrador de la figura
    manager = plt.get_current_fig_manager()

    # Obtiene las dimensiones de la pantalla
    screen_width = manager.window.winfo_screenwidth()
    screen_height = manager.window.winfo_screenheight()

    # Obtiene las dimensiones de la figura
    fig_width, fig_height = fig.get_size_inches() * fig.dpi

    # Calcula la posición del centro
    center_x = (screen_width // 2) - (fig_width // 2)
    center_y = (screen_height // 2) - (fig_height // 2)

    # Centra la figura
    manager.window.geometry('+%d+%d' % (center_x, center_y))
    




DAYS = ['Sun.', 'Mon.', 'Tues.', 'Wed.', 'Thurs.', 'Fri.', 'Sat.']
MONTHS = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']

def date_heatmap(series, start=None, end=None, mean=False, ax=None, fig=None, data=None, campo_data_extra=None , **kwargs):
    dates = series.index.floor('D')
    group = series.groupby(dates)
    series = group.mean() if mean else group.sum()

    start = pd.to_datetime(start or series.index.min())
    end = pd.to_datetime(end or series.index.max())
    end += np.timedelta64(1, 'D')

    start_sun = start - np.timedelta64((start.dayofweek + 1) % 7, 'D')
    end_sun = end + np.timedelta64(7 - end.dayofweek - 1, 'D')

    num_weeks = (end_sun - start_sun).days // 7
    heatmap = np.full((7, num_weeks), np.nan)
    ticks = {}
    for week in range(num_weeks):
        for day in range(7):
            date = start_sun + np.timedelta64(7 * week + day, 'D')
            if date.day == 1:
                ticks[week] = MONTHS[date.month - 1]
            if date.dayofyear == 1:
                ticks[week] += f'\n{date.year}'
            if date in series.index:
                heatmap[day, week] = series[date]

    y = np.arange(8) - 0.5
    x = np.arange(num_weeks + 1) - 0.5

    ax = ax or plt.gca()

    cmap = plt.cm.Greens
    newcolors = cmap(np.linspace(0.2, 1, 128))
    white = np.array([1, 1, 1, 1])
    newcolors[:1, :] = white
    newcmp = ListedColormap(newcolors)

    kwargs.pop('cmap', None)
    mesh = ax.pcolormesh(x, y, heatmap, edgecolor='black', cmap=newcmp, vmin=0, **kwargs)
    ax.invert_yaxis()
    
    ax.set_xticks(list(ticks.keys()))
    ax.set_xticklabels(list(ticks.values()))
    ax.set_yticks(np.arange(7))
    ax.set_yticklabels(DAYS)

    plt.sca(ax)
    plt.sci(mesh)

    annot = ax.annotate("", xy=(0,0), xytext=(10,10),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(i, j, value, date, extra_data):
        annot.xy = (j,i)
        hours = int(value // 60)
        minutes = int(value % 60)
        seconds = int((value*60) % 60)
        datetime_str = f"{date.strftime('%Y-%m-%d')} {hours:02d}:{minutes:02d}:{seconds:02d}"
        # text = f"{datetime_str}: {hours} horas {minutes} minutos {seconds} segundos, {extra_data}"
        text = f"{datetime_str}\n{extra_data}"
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(1)

    def hover(event):
        if event.inaxes == ax:
            col = int(event.xdata+0.5)
            row = int(event.ydata+0.5)
            date = start_sun + np.timedelta64(7 * col + row, 'D')
            value = heatmap[row, col]
            extra_data = data.loc[date, campo_data_extra]  
            update_annot(row, col, value, date, extra_data)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if annot.get_visible():
                annot.set_visible(False)
                fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    return ax


def habito_calendario(id_habito_especifico):
    with open('habitos/lista_habitos.json', 'r') as f:
        data_habito = json.load(f)

    # Filtrar los datos por id usando una comprensión de lista
    filtered_data = [item for item in data_habito if item['id'] == id_habito_especifico]
    filtered_data = filtered_data[0]
    
    
    data = pd.read_csv('registros/historial_habitos.csv')
    
    data = data.loc[data['id_habito'] == id_habito_especifico]

    data['fecha'] = pd.to_datetime(data['fecha'])

    data['duracion'] = pd.to_timedelta(data['duracion'])
    # data['duracion'] = data['duracion'].dt.components['minutes'] + data['duracion'].dt.components['seconds'] / 60
    data['duracion'] = data['duracion'].dt.components['hours'] * 60 + data['duracion'].dt.components['minutes'] + data['duracion'].dt.components['seconds'] / 60


    data.set_index('fecha', inplace=True)

    idx = pd.date_range(start='1/1/2023', end='12/31/2023')
    data = data.reindex(idx, fill_value=np.nan)
    # fig, ax = plt.subplots(figsize=(16, 2))
    fig, (ax, ax2) = plt.subplots(2, figsize=(10, 6))
 
  
    ax2 = grafico_lineas(id_habito_especifico, ax2, fig)
 
    
    date_heatmap(data['duracion'], cmap='YlOrRd', ax=ax, fig=fig, data=data , campo_data_extra='start_timer')
    
    plt.title(filtered_data["nombre"])
    
    # plt.colorbar()
    cax = fig.add_axes([0.05, 0.2, 0.01, 0.6])  
    plt.colorbar(cax=cax, orientation='vertical')
    fig.set_size_inches(14, 4)
    center_figure(fig)
    fig.subplots_adjust(hspace=0.5)
    plt.show()
    
def habito_calendario_check(id_habito_especifico):
    with open('habitos/lista_habitos.json', 'r') as f:
        data_habito = json.load(f)

    # Filtrar los datos por id usando una comprensión de lista
    filtered_data = [item for item in data_habito if item['id'] == id_habito_especifico]
    filtered_data = filtered_data[0]
    
    
    data = pd.read_csv('registros/check_historial_habitos.csv')
    
    data = data.loc[data['id_habito'] == id_habito_especifico]

    data['fecha_hora'] = pd.to_datetime(data['fecha_hora'])

    # data['duracion'] = pd.to_timedelta(data['duracion'])
    # data['duracion'] = data['duracion'].dt.components['minutes'] + data['duracion'].dt.components['seconds'] / 60

    data.set_index('fecha_hora', inplace=True)

    idx = pd.date_range(start='1/1/2023', end='12/31/2023')
    data = data.reindex(idx, fill_value=np.nan)
    fig, (ax, ax2) = plt.subplots(2, figsize=(10, 6))
 
  
    ax2 = grafico_lineas(id_habito_especifico, ax2, fig)
    

    # cursor1 = crear_cursor(ax)
    # cursor2 = crear_cursor(ax2)
    
    date_heatmap(data['hecho'], cmap='YlOrRd', ax=ax, fig=fig, data=data, campo_data_extra='id_habito')
    
    plt.title(filtered_data["nombre"])
    
    # plt.colorbar()
    cax = fig.add_axes([0.05, 0.2, 0.01, 0.6])  
    plt.colorbar(cax=cax, orientation='vertical')
    fig.set_size_inches(14, 4)
    center_figure(fig)
    fig.subplots_adjust(hspace=0.5)
    plt.show()
    

#fig, ax = plt.subplots(figsize=(16, 4))

from matplotlib.widgets import Cursor

def grafico_lineas(id, ax2, fig):
    df = pd.read_csv('registros/historial_habitos.csv')

    # Convertir 'fecha' a datetime y 'duracion' a timedelta
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['duracion'] = pd.to_timedelta(df['duracion']).dt.total_seconds() / 60

    # Seleccionar el id_habito
    id_habito_seleccionado = id  # Cambia esto al ID que quieras

    # Filtrar el DataFrame para el id_habito seleccionado
    df_filtrado = df[df['id_habito'] == id_habito_seleccionado]

    # Dibujar el gráfico
    line2, = ax2.plot(df_filtrado['fecha'], df_filtrado['duracion'], label=f'ID Hábito {id_habito_seleccionado}')
    ax2.set_xlabel('Fecha')
    ax2.set_ylabel('Duración')
    ax2.legend()

    # cursor2 = Cursor(ax2, useblit=True, color='red', linewidth=1)

    # # Función para mostrar la duración en horas cuando el cursor pasa sobre un punto del gráfico
    # def onmotion_ax2(event):
    #     if event.inaxes == ax2:
    #         x, y = event.xdata, event.ydata
    #         y_hours = y / 60  # Convertir minutos a horas
    #         line2.set_label(f'ID Hábito {id_habito_seleccionado}, Duración: {y_hours:.2f} horas')
    #         ax2.legend()

    # # Conectar la función al evento de movimiento del cursor
    # fig.canvas.mpl_connect('motion_notify_event', onmotion_ax2)
    
    
    def onmotion_ax2(event):
        if event.inaxes == ax2:
            # print('aeuaoeu')
            x, y = event.xdata, event.ydata
            y_hours = y / 60  # Convertir minutos a horas
            line2.set_label(f' Duración: {y_hours:.2f} horas')
            ax2.legend()
            line2.set_visible(True)
            fig.canvas.draw_idle()
    fig.canvas.mpl_connect('motion_notify_event', onmotion_ax2)

    return ax2

def crear_cursor(ax):
    cursor = Cursor(ax, useblit=True, color='red', linewidth=1)
    return cursor