from tkinter import *
from tkinter import ttk
import database
import database_orders
from database_orders import init_db as init_orders_db, get_all_orders
from database import init_db as init_users_db, verify_user

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
        self.add_screen("manager_dashboard", self.create_manager_dashboard)

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
        label = ttk.Label(frame, text="Добро пожаловать, вас приветствует компания АвтоТранс", font=("Arial", 20))
        label.pack(pady=50)

        btn_login = ttk.Button(frame, text="Войти", command=lambda: self.show_screen("login"))
        btn_login.pack(pady=10)

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
        ttk.Label(frame, text="Список заказов").pack()

            # Создаем таблицу (Treeview)
        columns = ("requestid", "startdate", "cartype", "carmodel", "problemdescription", "requeststatus", "completiondate", "repairparts", "masterid", "clientid")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        # Настройка заголовков
        self.tree.heading("requestid", text="ID")
        self.tree.heading("startdate", text="Дата заявки")
        self.tree.heading("cartype", text="Тип автомобиля")
        self.tree.heading("carmodel", text="Название")
        self.tree.heading("problemdescription", text="Проблема")
        self.tree.heading("requeststatus", text="Статус заказа")
        self.tree.heading("completiondate", text="Дата завершения")
        self.tree.heading("repairparts", text="Детали на замену")
        self.tree.heading("masterid", text="ID работника")
        self.tree.heading("clientid", text="ID клиента")

        # Настройка ширины колонок
        self.tree.column("requestid", width=50)
        self.tree.column("startdate", width=150)
        self.tree.column("cartype", width=80)
        self.tree.column("carmodel", width=200)
        self.tree.column("problemdescription", width=50)
        self.tree.column("requeststatus", width=50)
        self.tree.column("completiondate", width=50)
        self.tree.column("repairparts", width=50)
        self.tree.column("masterid", width=50)
        self.tree.column("clientid", width=50)

        # Добавляем скроллбар
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Упаковываем виджеты в фрейм
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Кнопка обновления
        btn_refresh = ttk.Button(frame, text="Обновить данные", command=self.on_refresh)
        btn_refresh.pack(pady=10)

        # Кнопка изменения данных
        btn_edit = ttk.Button(frame, text="Изменить", command=self.edit_info)
        btn_edit.pack(pady=15)
        
        # Загружаем данные при создании экрана
        self.load_data()

        btn_logout = ttk.Button(frame, text="Выйти", command=lambda: self.show_screen("main"))
        btn_logout.pack(pady=20)

    def create_manager_dashboard(self, frame):
        ttk.Label(frame, text="Личный кабинет Менеджера", font=("Arial", 24)).pack(pady=20)
        ttk.Label(frame, text="Список заказов").pack()

        btn_logout = ttk.Button(frame, text="Выйти", command=lambda: self.show_screen("main"))
        btn_logout.pack(pady=20)

    # --- Методы класса ---

    def load_data(self):
        """Загружает данные из БД и обновляет таблицу в фрейме."""
        if not hasattr(self, 'tree'):
            return
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Получаем данные
        data = database_orders.get_all_orders()
        
        # Вставляем данные в таблицу
        for row in data:
            self.tree.insert("", "end", values=row)

    def on_refresh(self, event=None):
        """Обработчик кнопки обновления."""
        self.load_data()

    def edit_info(self):
        """Ввод номера заказа"""
        self.editor = Tk()
        self.editor.title("Изменение данных")
        self.editor.geometry("400x200")
        self.label=ttk.Label(self.editor, text="Введите номер заказа:")
        self.label.pack(anchor=N)

        self.editor_input = ttk.Entry(self.editor, width=30)
        self.editor_input.pack(pady=5)

        self.id_btn = ttk.Button(self.editor, text = "Ввод", command=self.edit_engine)
        self.id_btn.pack()

    def edit_engine(self):
        """Окно изменения данных"""
        self.edit = Tk()
        self.edit.title("Поиск")
        self.edit.geometry("400x200")
        self.label=ttk.Label(self.edit, text="Введите данные которые хотите изменить:")
        self.label.pack(anchor=N)

        status_list = ["В процессе ремона", "Готова к выдаче", "Новая заявка", "Ожидание автозапчастей"]
        self.status_edit = ttk.Combobox(self.edit, values=status_list)
        self.status_edit.pack()

        self.problem_edit = ttk.Entry(self.edit, width=30)
        self.problem_edit.pack()

        self.workerid_edit = ttk.Entry(self.edit, width=30)
        self.workerid_edit.pack()

        self.parts_edit = ttk.Entry(self.edit, width=30)
        self.parts_edit.pack()

        self.edit_confirm = ttk.Button(self.edit, text = "Изменить", command=self.search_engine)
        self.edit_confirm.pack()
    # --- Логика ---

    def check_credentials(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        # Проверяем через новую функцию
        is_valid, role = verify_user(login, password)
        
        if is_valid:
            if role == "admin":
                self.show_screen("admin_dashboard")
            elif role == "client":
                self.show_screen("client_dashboard")
            elif role == "manager":
                self.show_screen("main")
        else:
            self.show_error("Неверный логин или пароль!")

    def show_error(self, message):
        # Простое сообщение об ошибке (можно сделать messagebox)
        print(f"Ошибка: {message}")
        # Для наглядности можно вывести в консоль или создать всплывающее окно
        # from tkinter import messagebox; messagebox.showerror("Ошибка", message)

def main():
    # Инициализируем обе базы данных ПЕРЕД запуском
    print("Инициализация баз данных...")
    init_users_db()
    init_orders_db()
    print("Готово!")

    root = Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()