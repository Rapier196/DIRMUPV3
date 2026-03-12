from tkinter import *
from tkinter import ttk
import database
import database_orders
from database_orders import init_db as init_orders_db, get_all_orders, get_orders_by_client_id, get_order_by_id, update_order, create_order
from database import init_db as init_users_db, verify_user, get_client_id_by_login

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
        self.trees = {}
        self.current_user_id = None # ID текущего пользователя
        self._current_role = None # Текущая роль (для редактирования)
        
        self.add_screen("main", self.create_main_screen)
        self.add_screen("login", self.create_login_screen)
        self.add_screen("client_dashboard", self.create_client_dashboard)
        self.add_screen("admin_dashboard", self.create_admin_dashboard)
        self.add_screen("manager_dashboard", self.create_manager_dashboard)
        self.add_screen("mechanic_dashboard", self.create_mechanic_dashboard)

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
        ttk.Label(frame, text="Логин:").pack()
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
        ttk.Label(frame, text="Мои заказы").pack()

        # Кнопка создания заявки
        btn_create = ttk.Button(frame, text="Создать заявку", command=self.create_order_form)
        btn_create.pack(pady=10)

        # Создаём таблицу
        self._create_order_table(frame, "client")

        btn_logout = ttk.Button(frame, text="Выйти", command=lambda: self.show_screen("main"))
        btn_logout.pack(pady=20)

    # --- Экран 4: Личный кабинет Оператора ---
    def create_admin_dashboard(self, frame):
        self._create_order_table(frame, "admin")
        btn_logout = ttk.Button(frame, text="Выйти", command=lambda: self.show_screen("main"))
        btn_logout.pack(pady=20)

    # --- Экран 5: Личный кабинет Менеджера ---
    def create_manager_dashboard(self, frame):
        self._create_order_table(frame, "manager")
        btn_logout = ttk.Button(frame, text="Выйти", command=lambda: self.show_screen("main"))
        btn_logout.pack(pady=20)

    # --- Экран 6: Личный кабинет Автомеханика ---
    def create_mechanic_dashboard(self, frame):
        self._create_order_table(frame, "mechanic")
        btn_logout = ttk.Button(frame, text="Выйти", command=lambda: self.show_screen("main"))
        btn_logout.pack(pady=20)

    def _create_order_table(self, frame, role):
        """Создаёт таблицу заказов с учётом роли"""
        columns = ("requestid", "startdate", "cartype", "carmodel", "problemdescription", "requeststatus", "completiondate", "repairparts", "masterid", "clientid", "comment")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)

        tree.heading("requestid", text="ID")
        tree.heading("startdate", text="Дата заявки")
        tree.heading("cartype", text="Тип автомобиля")
        tree.heading("carmodel", text="Название")
        tree.heading("problemdescription", text="Проблема")
        tree.heading("requeststatus", text="Этап выполнения")
        tree.heading("completiondate", text="Дата завершения")
        tree.heading("repairparts", text="Запчасти на замену")
        tree.heading("masterid", text="ID работника")
        tree.heading("clientid", text="ID клиента")
        tree.heading("comment", text="Комментарий")

        tree.column("requestid", width=50)
        tree.column("startdate", width=150)
        tree.column("cartype", width=80)
        tree.column("carmodel", width=200)
        tree.column("problemdescription", width=50)
        tree.column("requeststatus", width=50)
        tree.column("completiondate", width=50)
        tree.column("repairparts", width=50)
        tree.column("masterid", width=50)
        tree.column("clientid", width=50)
        tree.column("comment", width=50)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        btn_refresh = ttk.Button(frame, text="Обновить данные", command=self.on_refresh(role))
        btn_refresh.pack(pady=10)

        # Кнопка редактирования зависит от роли
        if role == "admin":
            btn_edit = ttk.Button(frame, text="Изменить", command=self.edit_info_admin)
        elif role == "manager":
            btn_edit = ttk.Button(frame, text="Изменить", command=self.edit_info_manager)
        elif role == "mechanic":
            btn_edit = ttk.Button(frame, text="Изменить", command=self.edit_info_mechanic)
        else:
            btn_edit = None # У клиента нет кнопки "Изменить"
        
        if btn_edit:
            btn_edit.pack(pady=15)
        
        self.trees[role] = tree
        self.load_data(role)

    def load_data(self, role):
        if role not in self.trees: # Проверка на наличие таблицы
            return
        tree = self.trees[role] # Получаем таблицу из словаря
        for row in tree.get_children():
            tree.delete(row)
        
        if role == "client":
            # Для клиента показываем только его заказы
            if hasattr(self, 'current_user_id') and self.current_user_id is not None:
                data = database_orders.get_orders_by_client_id(self.current_user_id)
            else:
                # Если пользователь не вошёл, показываем пустую таблицу
                data = []
        else:
            # Для остальных показываем все заказы
            data = database_orders.get_all_orders()

        for row in data:
            tree.insert("", "end", values=row)

    def on_refresh(self, role):
        """Обновляет таблицу"""
        self.load_data(role) # Передаём роль

    # ==================== СОЗДАНИЕ ЗАЯВКИ ====================
    def create_order_form(self):
        """Форма создания новой заявки"""
        self.order_form = Toplevel(self.root)
        self.order_form.title("Создание заявки")
        self.order_form.geometry("500x500")
        self.order_form.transient(self.root)
        self.order_form.grab_set()

        ttk.Label(self.order_form, text="Новая заявка", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = Frame(self.order_form)
        form_frame.pack(pady=10, padx=20, fill=X)

        # Поля для ввода
        fields = [
            ("startdate", "Дата заявки:", "Entry"),
            ("cartype", "Тип автомобиля:", "Entry"),
            ("carmodel", "Модель автомобиля:", "Entry"),
            ("problemdescription", "Описание проблемы:", "Entry"),
            ("requeststatus", "Статус:", "Combobox"),
            ("comment", "Комментарий:", "Entry"),
        ]

        self.order_widgets = {}
        status_list = ["Новая заявка"]

        for i, (field_name, label_text, widget_type) in enumerate(fields):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky=W, pady=5)

            if widget_type == "Entry":
                entry = ttk.Entry(form_frame, width=30)
                entry.grid(row=i, column=1, pady=5)
                self.order_widgets[field_name] = entry
            elif widget_type == "Combobox":
                combo = ttk.Combobox(form_frame, values=status_list, state="readonly", width=27)
                combo.grid(row=i, column=1, pady=5)
                combo.set("Новая заявка")
                self.order_widgets[field_name] = combo

        # Кнопки
        btn_frame = Frame(self.order_form)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Создать", command=self.submit_order).pack(side=LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", command=self.order_form.destroy).pack(side=LEFT, padx=10)

    def submit_order(self):
        """Отправляет данные о новой заявке в БД"""
        try:
            startdate = self.order_widgets["startdate"].get().strip()
            cartype = self.order_widgets["cartype"].get().strip()
            carmodel = self.order_widgets["carmodel"].get().strip()
            problemdescription = self.order_widgets["problemdescription"].get().strip()
            requeststatus = self.order_widgets["requeststatus"].get().strip()
            comment = self.order_widgets["comment"].get().strip()

            if not all([startdate, cartype, carmodel, problemdescription, requeststatus]):
                self.show_error("Заполните все обязательные поля!")
                return
            
            # Создаём заказ
            result = create_order(
                startdate=startdate,
                cartype=cartype,
                carmodel=carmodel,
                problemdescription=problemdescription,
                requeststatus=requeststatus,
                client_id=self.current_user_id,
                completiondate=None,
                repairparts=None,
                masterid=None,
                comment=comment if comment else None
            )

            if result:
                self.show_error("Заявка успешно создана!")
                self.order_form.destroy()
                for role in ["client", "admin", "manager", "mechanic"]: # Добавляем цикл
                    self.load_data(role)
            else:
                self.show_error("Ошибка создания заявки!")
        except Exception as e:
            self.show_error(f"Ошибка: {str(e)}")

    # ==================== АДМИН ====================
    def edit_info_admin(self):
        """Ввод номера заказа для администратора"""
        self._current_role = "admin"
        self._show_order_id_input()

    # ==================== МЕНЕДЖЕР ====================
    def edit_info_manager(self):
        """Ввод номера заказа для менеджера"""
        self._current_role = "manager"
        self._show_order_id_input()

    # ==================== МЕХАНИК ====================
    def edit_info_mechanic(self):
        """Ввод номера заказа для автомеханика"""
        self._current_role = "mechanic"
        self._show_order_id_input()

    def _show_order_id_input(self):
        """Общее окно ввода номера заказа"""
        self.editor = Toplevel(self.root)
        self.editor.title("Изменение данных")
        self.editor.geometry("400x200")
        self.editor.transient(self.root)
        self.editor.grab_set()

        self.label = ttk.Label(self.editor, text="Введите номер заказа:")
        self.label.pack(anchor=N, pady=10)

        self.editor_input = ttk.Entry(self.editor, width=30)
        self.editor_input.pack(pady=5)

        self.id_btn = ttk.Button(self.editor, text="Ввод", command=self._get_order_data)
        self.id_btn.pack(pady=10)

    def _get_order_data(self):
        """Получение данных из БД"""
        try:
            order_id = int(self.editor_input.get())
        except ValueError:
            self.show_error("Введите корректный номер заказа!")
            return
        
        order_data = get_order_by_id(order_id)

        if not order_data:
            self.show_error("Заказ с таким ID не найден!")
            return
        
        self.editor.destroy()
        self.order_id = order_id
        self.order_data = order_data

        # Определяем роль и создаём форму
        if self._current_role == "admin":
            self._create_admin_edit_form()
        elif self._current_role == "manager":
            self._create_manager_edit_form()
        elif self._current_role == "mechanic":
            self._create_mechanic_edit_form()

    def _create_admin_edit_form(self):
        """Форма редактирования для администратора"""
        self.edit = Toplevel(self.root)
        self.edit.title("Редактирование заказа")
        self.edit.geometry("500x400")
        self.edit.transient(self.root)
        self.edit.grab_set()

        ttk.Label(self.edit, text="Редактирование заказа", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = Frame(self.edit)
        form_frame.pack(pady=10, padx=20, fill=X)

        fields = [
            ("problemdescription", "Проблема:", "Entry"),
            ("requeststatus", "Этап выполнения:", "Combobox"),
            ("completiondate", "Дата завершения:", "Entry"),
            ("repairparts", "Запчасти на замену:", "Entry"),
            ("masterid", "ID работника:", "Entry"),
            ("comment", "Комментарий:", "Entry"),
        ]

        self.edit_widgets = {}
        status_list = ["В процессе ремонта", "Готова к выдаче", "Новая заявка", "Ожидание автозапчастей"]

        for i, (field_name, label_text, widget_type) in enumerate(fields):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky=W, pady=5)

            if widget_type == "Entry":
                entry = ttk.Entry(form_frame, width=30)
                entry.grid(row=i, column=1, pady=5)
                self.edit_widgets[field_name] = entry
            elif widget_type == "Combobox":
                combo = ttk.Combobox(form_frame, values=status_list, state="readonly", width=27)
                combo.grid(row=i, column=1, pady=5)
                self.edit_widgets[field_name] = combo

        btn_frame = Frame(self.edit)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Применить", command=self.save_changes).pack(side=LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", command=self.edit.destroy).pack(side=LEFT, padx=10)

        self._load_current_data()

    def _create_manager_edit_form(self):
        """Форма редактирования для менеджера"""
        self.edit = Toplevel(self.root)
        self.edit.title("Редактирование заказа")
        self.edit.geometry("500x400")
        self.edit.transient(self.root)
        self.edit.grab_set()

        ttk.Label(self.edit, text="Редактирование заказа", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = Frame(self.edit)
        form_frame.pack(pady=10, padx=20, fill=X)

        fields = [
            ("completiondate", "Дата завершения:", "Entry"),
            ("masterid", "ID работника:", "Entry"),
        ]

        self.edit_widgets = {}

        for i, (field_name, label_text, widget_type) in enumerate(fields):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky=W, pady=5)

            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            self.edit_widgets[field_name] = entry

        btn_frame = Frame(self.edit)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Применить", command=self.save_changes).pack(side=LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", command=self.edit.destroy).pack(side=LEFT, padx=10)

        self._load_current_data()

    def _create_mechanic_edit_form(self):
        """Форма редактирования для автомеханика"""
        self.edit = Toplevel(self.root)
        self.edit.title("Редактирование заказа")
        self.edit.geometry("500x400")
        self.edit.transient(self.root)
        self.edit.grab_set()

        ttk.Label(self.edit, text="Редактирование заказа", font=("Arial", 16, "bold")).pack(pady=10)

        form_frame = Frame(self.edit)
        form_frame.pack(pady=10, padx=20, fill=X)

        fields = [
            ("repairparts", "Запчасти на замену:", "Entry"),
            ("comment", "Комментарий:", "Entry"),
        ]

        self.edit_widgets = {}

        for i, (field_name, label_text, widget_type) in enumerate(fields):
            ttk.Label(form_frame, text=label_text).grid(row=i, column=0, sticky=W, pady=5)

            entry = ttk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            self.edit_widgets[field_name] = entry

        btn_frame = Frame(self.edit)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Применить", command=self.save_changes).pack(side=LEFT, padx=10)
        ttk.Button(btn_frame, text="Отмена", command=self.edit.destroy).pack(side=LEFT, padx=10)

        self._load_current_data()

    # ==================== ОБЩИЕ МЕТОДЫ ====================
    def _load_current_data(self):
        """Загружает текущие данные в поля редактирования"""
        # order_data: (requestid, startdate, cartype, carmodel, problemdescription, requeststatus, completiondate, repairparts, masterid, clientid, comment)
        # Индексы: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10

        if not hasattr(self, 'order_data'):
            return
        
        order_data = self.order_data

        if "problemdescription" in self.edit_widgets:
            self.edit_widgets["problemdescription"].insert(0, order_data[4] or "")
        if "requeststatus" in self.edit_widgets:
            self.edit_widgets["requeststatus"].set(order_data[5] or "")
        if "completiondate" in self.edit_widgets:
            self.edit_widgets["completiondate"].insert(0, order_data[6] or "")
        if "repairparts" in self.edit_widgets:
            self.edit_widgets["repairparts"].insert(0, order_data[7] or "")
        if "masterid" in self.edit_widgets:
            self.edit_widgets["masterid"].insert(0, str(order_data[8]) if order_data[8] else "")
        if "comment" in self.edit_widgets:
            self.edit_widgets["comment"].insert(0, order_data[10] or "")
    
    def save_changes(self):
        """Сохраняет изменения в БД"""
        # Формируем словарь с изменёнными полями
        changes = {}

        for field_name, widget in self.edit_widgets.items():
            value = widget.get().strip()
            if value: # Обновляем только если поле не пустое
                if field_name == "masterid":
                    try:
                        value = int(value)
                    except ValueError:
                        self.show_error("ID работника должен быть числом!")
                        return
                changes[field_name] = value
            
        if not changes:
            self.show_error("Не выбрано ни одного поля для изменения!")
            return
            
        # Обновляем базу данных
        try:
            result = update_order(self.order_id, **changes)
            if result:
                self.show_error("Данные успешно обновлены!")
                # Используем self._current_role вместо self._load_data()
                if self._current_role == "client":
                    self.load_data("client")
                elif self._current_role == "admin":
                    self.load_data("admin")
                elif self._current_role == "manager":
                    self.load_data("manager")
                elif self._current_role == "mechanic":
                    self.load_data("mechanic")
                self.edit.destroy()
            else:
                self.show_error("Ошибка обновления данных!")
        except Exception as e:
            self.show_error(f"Ошибка обновления: {str(e)}")

    # --- Логика ---

    def check_credentials(self):
        login = self.login_entry.get()
        password = self.password_entry.get()

        # Проверяем через новую функцию
        is_valid, role, user_id = verify_user(login, password)
        
        if is_valid:
            self.current_user_id = user_id # Сохраняем ID пользователя
            self._current_role = role # Сохраняем роль пользователя
            if role == "admin":
                self.show_screen("admin_dashboard")
            elif role == "client":
                self.show_screen("client_dashboard")
            elif role == "manager":
                self.show_screen("manager_dashboard")
            elif role == "mechanic":
                self.show_screen("mechanic_dashboard")
            else:
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