import tkinter as tk
from tkinter import messagebox
from pomodoro.pomodoro_app import start_timer, pause_timer, resume_timer, stop_timer, save_csv_timer, set_variables
from pomodoro.lee_habito import get_times_pomodoro

def ventana_pomodoro(opcion):
    
    def start_button_clicked():
        # work_time = int(work_time_input.get())
        start_button['state'] = 'disabled'
        pause_button['state'] = 'normal'
        stop_button['state'] = 'normal'
        start_timer(root, timer_label, timer_label_count, work_time, short_break, count, id)

    def pause_button_clicked():
        pause_timer()
        start_button['state'] = 'normal'
        pause_button['state'] = 'disabled'
        resume_button['state'] = 'normal'

    def resume_button_clicked():
        resume_button['state'] = 'disabled'
        pause_button['state'] = 'normal'
        resume_timer(root, timer_label, timer_label_count)
    
    def stop_button_clicked():
        stop_timer()
        start_button['state'] = 'normal'
        pause_button['state'] = 'disabled'
        stop_button['state'] = 'disabled'
        timer_label['text'] = "00:00"
    
    def on_closing():
        if messagebox.askokcancel("Salir", "¿Realmente desea salir?"):
            save_csv_timer()
            root.destroy()
    

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

    timer_label = tk.Label(root, text=str(work_time)+":00", font=('Arial', 40))
    timer_label.pack(pady=10)
    
    timer_label_count = tk.Label(root, text="restan:"+str(count), font=('Arial', 20))
    timer_label_count.pack(pady=10)

    start_button = tk.Button(root, text="Start", command=start_button_clicked)
    start_button.pack(side=tk.LEFT, padx=10)

    pause_button = tk.Button(root, text="Pause", command=pause_button_clicked, state='disabled')
    pause_button.pack(side=tk.LEFT, padx=10)

    resume_button = tk.Button(root, text="Resume", command=resume_button_clicked, state='disabled')
    resume_button.pack(side=tk.LEFT, padx=10)

    stop_button = tk.Button(root, text="Stop", command=stop_button_clicked,  state='disabled')
    stop_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()
