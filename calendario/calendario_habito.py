import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DAYS = ['Sun.', 'Mon.', 'Tues.', 'Wed.', 'Thurs.', 'Fri.', 'Sat.']
MONTHS = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May', 'June', 'July', 'Aug.', 'Sept.', 'Oct.', 'Nov.', 'Dec.']

def date_heatmap(series, start=None, end=None, mean=False, ax=None, fig=None,   **kwargs):
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
    mesh = ax.pcolormesh(x, y, heatmap, edgecolor='black', vmin=0, **kwargs)
    ax.invert_yaxis()
    
    

    ax.set_xticks(list(ticks.keys()))
    ax.set_xticklabels(list(ticks.values()))
    ax.set_yticks(np.arange(7))
    ax.set_yticklabels(DAYS)

    plt.sca(ax)
    plt.sci(mesh)

    annot = ax.annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(i, j, value):
        annot.xy = (j,i)
        text = f"{value} : min - {i}-{j}"
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(1)

    def hover(event):
        if event.inaxes == ax:
            col = int(event.xdata+0.5)
            row = int(event.ydata+0.5)
            value = heatmap[row, col]
            update_annot(row, col, value)
            annot.set_visible(True)
            fig.canvas.draw_idle()
        else:
            if annot.get_visible():
                annot.set_visible(False)
                fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)

    return ax


def habito_calendario(id_habito_especifico):
    data = pd.read_csv('registros/historial_habitos.csv')
    
    data = data.loc[data['id_habito'] == id_habito_especifico]

    data['fecha'] = pd.to_datetime(data['fecha'])

    data['duracion'] = pd.to_timedelta(data['duracion'])
    data['duracion'] = data['duracion'].dt.components['minutes'] + data['duracion'].dt.components['seconds'] / 100

    data.set_index('fecha', inplace=True)

    idx = pd.date_range(start='1/1/2023', end='12/31/2023')
    data = data.reindex(idx, fill_value=np.nan)
    fig, ax = plt.subplots(figsize=(16, 4))
 
    
    date_heatmap(data['duracion'], cmap='YlOrRd', ax=ax, fig=fig)
    plt.colorbar()
    plt.show()

#fig, ax = plt.subplots(figsize=(16, 4))