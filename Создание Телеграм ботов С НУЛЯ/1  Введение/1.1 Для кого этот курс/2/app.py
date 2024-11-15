from tkinter import ttk
import tkinter as tk
import time

root = tk.Tk()
root.geometry('300x300+150+150')

def sleep_func():
    time.sleep(10)
    lab['text'] = 'После сна'

btn = ttk.Button(root, text='Run', command=sleep_func)
btn.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

lab = ttk.Label(root, text='Текст до нажатия')
lab.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

root.mainloop()