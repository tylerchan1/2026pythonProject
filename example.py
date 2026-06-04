import tkinter as tk

def update_text(event):
    current = entry.get()
    label.config(text=current)

window = tk.Tk()
window.title("GUI 예제")
window.geometry("300x200")

label = tk.Label(window, text="안녕하세요")
label.pack()

button = tk.Button(window, text="클릭")
button.pack()

entry = tk.Entry(window)
entry.pack()

entry.bind("<KeyRelease>", update_text)

window.mainloop()