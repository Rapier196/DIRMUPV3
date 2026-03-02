from tkinter import *
from tkinter import ttk
 
root = Tk()
root.title("Автосервис «АвтоТранс»")
root.geometry("1920x1080")
root.attributes("-toolwindow", True)
root.minsize(320,240)
root.maxsize(1920,1080) 
icon = PhotoImage(file = "i.png")
root.iconphoto(True, icon)

label = ttk.Label(text="Добро пожаловать, что вы хотите сделать?")
label.pack()

def noprofile():
    windownp = Tk()
    windownp.title("Главная страница")
    windownp.geometry("1920x1080")
    windownp.attributes("-toolwindow", True)
    label = ttk.Label(windownp, text="Скоро тут чото будет (за эту упшку я узнал больше чем за 3 года в этом «прекрасном» колледже)")
    windownp.minsize(320,240)
    windownp.maxsize(1920,1080)
    label.pack()

btn = ttk.Button(text = "Войти в свой профиль", state = ["disabled"])
btn.pack()
btn.place(relx=0.15, rely=0.45, width=200, height=70)
btn = ttk.Button(text = "Я сотрудник", state = ["disabled"])
btn.pack()
btn.place(relx=0.45, rely=0.45, width=200, height=70)
btn = ttk.Button(text = "Продолжить без профиля", command = noprofile)
btn.pack()
btn.place(relx=0.75, rely=0.45, width=200, height=70)

root.mainloop()