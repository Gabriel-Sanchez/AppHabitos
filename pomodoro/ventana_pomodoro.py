import tkinter as tk
from tkinter import messagebox
from pomodoro.pomodoro_app import start_timer, pause_timer, resume_timer, stop_timer, save_csv_timer, set_variables
from pomodoro.lee_habito import get_times_pomodoro
from tkinter import font



def ventana_pomodoro(opcion):
    
    def start_button_clicked():
        # work_time = int(work_time_input.get())
        start_button['state'] = 'disabled'
        pause_button['state'] = 'normal'
        stop_button['state'] = 'normal'
        start_timer(root, timer_label, timer_label_count, work_time, short_break, count, id)

    def pause_button_clicked():
        pause_timer()
        start_button['state'] = 'disabled'
        pause_button['state'] = 'disabled'
        resume_button['state'] = 'normal'
        root.configure(bg="#ffa300")

    def resume_button_clicked():
        resume_button['state'] = 'disabled'
        pause_button['state'] = 'normal'
        resume_timer(root, timer_label, timer_label_count)
    
    def stop_button_clicked():
        stop_timer()
        start_button['state'] = 'normal'
        pause_button['state'] = 'disabled'
        stop_button['state'] = 'disabled'
        resume_button['state'] = 'disabled'
        timer_label['text'] = "00:00"
    
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Realmente desea salir?"):
            save_csv_timer()
            root.destroy()
    

    background_color = "#1f1f1f"
    
    root = tk.Tk()
    root.title("Pomodoro Timer")
    
    root.protocol("WM_DELETE_WINDOW", on_closing)

    work_time, short_break, count, id = get_times_pomodoro(opcion)
    set_variables(work_time, short_break, id)
    # work_time_input = tk.StringVar()
    # work_time_input.set(work_time)


    # work_label = tk.Label(root, text="Work Time (minutes):")
    # work_label.pack()

    # work_entry = tk.Entry(root, textvariable=work_time_input)
    # work_entry.pack()

    timer_label = tk.Label(root, text=f'{work_time:02d}:{00:02d}', font=('Arial', 12), bg=background_color, fg='white')
    # timer_label.pack(pady=10)
    timer_label.grid(row=0, column=0, padx=(3,0), pady=3)
    
    timer_label_count = tk.Label(root, text= f'{count:02d}', font=('Arial', 12), bg=background_color, fg='white')
    # timer_label_count.pack(pady=10)
    timer_label_count.grid(row=0, column=1, padx=3, pady=0)

    start_button = tk.Button(root, text="\u25B6", font=("Arial", 8), bg=background_color, command=start_button_clicked, fg='white')
    # start_button.pack(side=tk.LEFT, padx=10)
    start_button.grid(row=0, column=2, padx=0, pady=0)
    
    pause_button = tk.Button(root, text="\u23F8", font=("Arial", 8), bg=background_color, command=pause_button_clicked, state='disabled', fg='white')
    # pause_button.pack(side=tk.LEFT, padx=10)
    pause_button.grid(row=0, column=3, padx=0, pady=0)

    resume_button = tk.Button(root, text="\u25B6\u25B6", font=("Arial", 8), bg=background_color, command=resume_button_clicked, state='disabled', fg='white')
    # resume_button.pack(side=tk.LEFT, padx=10)
    resume_button.grid(row=0, column=4, padx=0, pady=0)

    stop_button = tk.Button(root, text="\u25A0", font=("Arial", 8), bg=background_color, command=stop_button_clicked,  state='disabled', fg='white')
    # stop_button.pack(side=tk.LEFT, padx=10)
    stop_button.grid(row=0, column=5, padx=(0,3), pady=0)
    
    
    # root.configure(bg='blue')
    
    
    
    
    
    


    # def mover_ventana(event):
    #     root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))
    
    def start_move(event):
        root.startX = event.x
        root.startY = event.y

    def stop_move(event):
        root.startX = None
        root.startY = None

    def do_move(event):
        dx = event.x - root.startX
        dy = event.y - root.startY
        x = root.winfo_x() + dx
        y = root.winfo_y() + dy
        root.geometry(f"+{x}+{y}")

    def cerrar_ventana():
        on_closing()
        # root.destroy()

   
    root.overrideredirect(True)  # Quita el borde de la ventana

    # Crea un marco para la barra de título
    barra_titulo = tk.Frame(root, bg='black', relief='raised', bd=1)
    barra_titulo.grid(row=0, column=6, padx=(0,5), pady=0)

    # Crea un label para mover la ventana
    label_mover = tk.Label(barra_titulo, text="\u21AA", bg='#089aff', fg='white', bd=2)
    label_mover.grid(row=0, column=0, sticky="w")
    # label_mover.bind('<B1-Motion>', mover_ventana)
    label_mover.bind("<ButtonPress-1>", start_move)
    label_mover.bind("<ButtonRelease-1>", stop_move)
    label_mover.bind("<B1-Motion>", do_move)

    # Crea un botón para cerrar la ventana
    boton_cerrar = tk.Button(barra_titulo, text='X', command=cerrar_ventana, bg='red', fg='white', bd=0)
    boton_cerrar.grid(row=0, column=1, padx=(0,0), pady=0)

    root.attributes("-topmost", True)

    def posicionar_ventana():
        # Obtiene el tamaño de la pantalla
        ancho_pantalla = root.winfo_screenwidth()
        alto_pantalla = root.winfo_screenheight()

        # Obtiene el tamaño de la ventana
        root.update_idletasks()
        ancho_ventana = root.winfo_width()
        alto_ventana = root.winfo_height()

        # Asume un alto de barra de tareas
        alto_barra_tareas = 50  # Cambia este valor según tu sistema

        # Calcula la posición de la ventana
        x = ancho_pantalla - ancho_ventana
        y = alto_pantalla - alto_ventana - alto_barra_tareas

        # Posiciona la ventana en la parte inferior derecha, por encima de la barra de tareas
        root.geometry('+{0}+{1}'.format(x, y))
    
    posicionar_ventana()
    
    
    

    root.mainloop()
