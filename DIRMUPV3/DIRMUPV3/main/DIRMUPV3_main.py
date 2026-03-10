from tkinter import *
from tkinter import ttk
import database  # Подключаем наш файл с базой данных

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Автосервис «АвтоТранс»")
        self.root.geometry("1920x1080")
        self.root.attributes("-toolwindow", True)
        self.root.minsize(320, 240)
        self.root.maxsize(1920, 1080) 

        # Создаем контейнер для всех экранов
        self.container = Frame(root)
        self.container.pack(fill=BOTH, expand=True)

        # Создаем экраны (Фреймы)
        self.screens = {}
        self.add_screen("main", self.create_main_screen)
        self.add_screen("login", self.create_login_screen)
        self.add_screen("client_dashboard", self.create_client_dashboard)
        self.add_screen("admin_dashboard", self.create_admin_dashboard)

        # Показываем главный экран при запуске
        self.show_screen("main")

    def add_screen(self, name, create_func):
        frame = Frame(self.container)
        frame.pack(fill=BOTH, expand=True)
        self.screens[name] = frame
        create_func(frame)

    def show_screen(self, name):
        # Скрываем все экраны
        for frame in self.screens.values():
            frame.pack_forget()
        # Показываем нужный
        self.screens[name].pack(fill=BOTH, expand=True)

    # --- Экран 1: Главное меню ---
    def create_main_screen(self, frame):
        label = ttk.Label(frame, text="Добро пожаловать, что вы хотите сделать?", font=("Arial", 20))
        label.pack(pady=50)

        btn_client = ttk.Button(frame, text="Войти как Клиент", command=lambda: self.show_screen("login"))
        btn_client.pack(pady=10)

        btn_admin = ttk.Button(frame, text="Я сотрудник (Админ)", command=lambda: self.show_screen("login"))
        btn_admin.pack(pady=10)

        btn_guest = ttk.Button(frame, text="Продолжить без профиля", command=self.open_guest)
        btn_guest.pack(pady=10)

    # --- Экран 2: Вход (Логин/Пароль) ---
    def create_login_screen(self, frame):
        ttk.Label(frame, text="Авторизация", font=("Arial", 24)).pack(pady=20)

        # Поле для логина
        ttk.Label(frame, text="Логин / Почта:").pack()
        self.login_entry = ttk.Entry(frame, width=30)
        self.login_entry.pack(pady=5)

        # Поле для пароля (пароль скрыт звездочками)
        ttk.Label(frame, text="Пароль:").pack()
        self.password_entry = ttk.Entry(frame, width=30, show="*")
        self.password_entry.pack(pady=5)

        # Кнопка входа
        btn_login = ttk.Button(frame, text="Войти", command=self.check_credentials)
        btn_login.pack(pady=20)

        # Кнопка назад
        btn_back = ttk.Button(frame, text="Назад", command=lambda: self.show_screen("main"))
        btn_back.pack(pady=5)

    # --- Экран 3: Личный кабинет Клиента ---
    def create_client_dashboard(self, frame):
        ttk.Label(frame, text="Личный кабинет Клиента", font=("Arial", 24)).pack(pady=20)
        ttk.Label(frame, text="Здесь будет информация о заказах...").pack()
        
        btn_logout = ttk.Button(frame, text="Выйти", command=lambda: self.show_screen("main"))
        btn_logout.pack(pady=20)

    # --- Экран 4: Личный кабинет Админа ---
    def create_admin_dashboard(self, frame):
        ttk.Label(frame, text="Панель Администратора", font=("Arial", 24)).pack(pady=20)
        ttk.Label(frame, text="Здесь управление сервисом...").pack()

        btn_logout = ttk.Button(frame, text="Выйти", command=lambda: self.show_screen("main"))
        btn_logout.pack(pady=20)

    # --- Логика ---

    def check_credentials(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        # Проверяем, есть ли такой пользователь в базе
        if login in database.USERS:
            user_data = database.USERS[login]
            # Проверяем пароль
            if user_data["password"] == password:
                role = user_data["role"]
                if role == "admin":
                    self.show_screen("admin_dashboard")
                elif role == "client":
                    self.show_screen("client_dashboard")
                else:
                    self.show_screen("main") # Если роль неизвестна
            else:
                self.show_error("Неверный пароль!")
        else:
            self.show_error("Пользователь не найден!")

    def show_error(self, message):
        # Простое сообщение об ошибке (можно сделать messagebox)
        print(f"Ошибка: {message}")
        # Для наглядности можно вывести в консоль или создать всплывающее окно
        # from tkinter import messagebox; messagebox.showerror("Ошибка", message)

    def open_guest(self):
        # Просто открываем заглушку
        self.show_screen("client_dashboard") # Пока просто показываем клиентский экран как гостевой

if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.mainloop()