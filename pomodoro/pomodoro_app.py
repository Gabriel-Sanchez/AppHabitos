import time
import tkinter as tk
from tkinter import messagebox
from registros.CRUD_registros import registrar_habito, registrar_Fin_habito,registrar_Inicio_habito, registrar_habito_descanso
import pygame

pygame.init()
sound_file = "assets/sounds/fin_bien.mp3"  

sonido_fin = pygame.mixer.Sound(sound_file)
sonido_fin.set_volume(0.2)


def set_variables(work_time, short_break,id):
    global work_time_global
    work_time_global = work_time
    global short_break_global
    short_break_global = short_break
    global break_time
    break_time = True
    global running
    running = False
    global time_running
    time_running = 0
    global id_global
    id_global = id
    
    global must_save
    must_save = False


def start_timer(root, timer_label, timer_label_count, work_time, short_break, count, id):
    global must_save
    must_save = True
    global id_global
    id_global = id
    global running
    global break_time
    global work_time_global
    work_time_global = work_time
    global short_break_global
    short_break_global = short_break
    global count_global
    count_global = count
    running = True
    break_time = True
    registrar_Inicio_habito(id_global)
    count_down(root, timer_label,timer_label_count, work_time * 60)

def count_down(root, timer_label,timer_label_count, seconds):
    global id_global
    global running
    global time_running
    global count_global
    global short_break_global
    global work_time_global
    global break_time
    if running and seconds >= 0 and count_global > 0 :
        mins, secs = divmod(seconds, 60)
        time_running = mins * 60 + secs
        timer_label['text'] = f'{mins:02d}:{secs:02d}'
        # root.title(f'{mins:02d}:{secs:02d}')
        root.after(1000, count_down, root, timer_label, timer_label_count, seconds - 1)
        if break_time:
            root.configure(bg='#ff0000')
        else:
            root.configure(bg='green')
        # print(break_time)
    elif running and seconds < 0 and count_global > 0:
        sonido_fin.play()
        if break_time:
            count_down(root, timer_label, timer_label_count, short_break_global * 60)
            timer_label_count['text'] = f'{count_global:02d}'
            break_time = False
            registrar_habito(id_global,work_time_global * 60)
        else:
            break_time = True
            count_down(root, timer_label, timer_label_count, work_time_global * 60)
            count_global -= 1
            timer_label_count['text'] =  f'{count_global:02d}'
            registrar_habito_descanso(id_global, short_break_global *60 )
        
    # elif running and seconds < 0 :
    #     count_global -= 1
    #     messagebox.showinfo("Pomodoro", "Timer finished!")
    elif count_global == 0:
        running = False
        registrar_Fin_habito(id_global)
        messagebox.showinfo("Pomodoro", "All Timer finished!")
        

def pause_timer():
    global running
    running = False

def resume_timer(root, timer_label, timer_label_count):
    global running
    running = True
    global time_running
    resume_time_running = time_running
    # resume_seconds = int(timer_label['text'][:2]) * 60 + int(timer_label['text'][3:5])
    resume_seconds = resume_time_running
    count_down(root, timer_label, timer_label_count, resume_seconds)
    
def stop_timer():
    global running
    running = False


def save_csv_timer(): 
    global running
    global break_time
    global time_running
    global short_break_global
    global work_time_global
    running = False
    
    print("short_break_global")
    print(short_break_global)
    print("time_running")
    print(time_running)
    
    if must_save:
        if break_time:
            tiempo = (work_time_global * 60) - time_running
            registrar_habito(id_global, tiempo)
        else:
            tiempo = (short_break_global * 60) - time_running
            registrar_habito_descanso(id_global, tiempo)
        registrar_Fin_habito(id_global)
        

    


# import time
# import tkinter as tk
# from tkinter import messagebox
# import json
# from tkinter import simpledialog
# # import pygame

# def start_timer():
#     global running
#     global work_time
#     running = True
#     count_down(work_time * 60)

# def resume_timer():
#     global running
#     running = True
#     count_down(int(timer_label['text'][:2]) * 60 + int(timer_label['text'][3:5]))


# def count_down(seconds):
#     global running
#     if running and seconds >= 0:
#         mins, secs = divmod(seconds, 60)
#         timer_label['text'] = f'{mins:02d}:{secs:02d}'
#         root.after(1000, count_down, seconds - 1)
#     elif running and seconds < 0:
#         running = False
#         if is_break:
#             messagebox.showinfo("Pomodoro", "¡Descanso terminado! ¡A trabajar de nuevo!")
#             count_down(work_time * 60)
#         else:
#             # pygame.mixer.init()
#             # pygame.mixer.music.load("alarm_sound.mp3")  # Reemplaza "alarm_sound.mp3" con el archivo de sonido que desees reproducir
#             # pygame.mixer.music.play()
#             if messagebox.askyesno("Pomodoro", "¡Tiempo de trabajo terminado! ¿Tomar un descanso?"):
#                 running = True
#                 count_down(short_break * 60)
#             else:
#                 running = True
#                 count_down(work_time * 60)

# def start_button_clicked():
#     global work_time
#     work_time = int(work_time_input.get())
#     start_button['state'] = 'disabled'
#     pause_button['state'] = 'normal'
#     stop_button['state'] = 'normal'
#     start_timer()

# def pause_button_clicked():
#     global running
#     running = False
#     start_button['state'] = 'normal'
#     pause_button['state'] = 'disabled'
#     resume_button['state'] = 'normal'

# def resume_button_clicked():
#     resume_button['state'] = 'disabled'
#     pause_button['state'] = 'normal'
#     resume_timer()


# def stop_button_clicked():
#     global running
#     running = False
#     start_button['state'] = 'normal'
#     pause_button['state'] = 'disabled'
#     stop_button['state'] = 'disabled'
#     timer_label['text'] = "00:00"
    
# # Configuración inicial
# work_time = 1  # Tiempo de trabajo en minutos
# short_break = 1  # Tiempo de descanso corto en minutos
# is_break = False
# running = False




