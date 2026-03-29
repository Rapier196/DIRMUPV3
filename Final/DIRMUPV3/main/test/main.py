import tkinter as tk
from tkinter import ttk
from database import init_db, get_all_users

# Глобальная переменная для таблицы
tree = None

def load_data():
    """Загружает данные из БД и обновляет таблицу в фрейме."""
    global tree
    # Очищаем старую таблицу
    for row in tree.get_children():
        tree.delete(row)
    
    # Получаем данные
    data = get_all_users()
    
    # Вставляем данные в таблицу
    for row in data:
        tree.insert("", "end", values=row)

def on_refresh(event=None):
    """Обработчик кнопки обновления."""
    load_data()

def main():
    global tree
    # 1. Инициализируем базу данных
    init_db()

    # 2. Создаем главное окно
    root = tk.Tk()
    root.title("Отображение Базы Данных")
    root.geometry("600x400")

    # 3. Создаем Фрейм
    main_frame = tk.Frame(root, bg="#f0f0f0")
    main_frame.pack(fill='both', expand=True, padx=10, pady=10)

    # 4. Создаем заголовок
    title_label = tk.Label(main_frame, text="Список пользователей", font=("Arial", 14, "bold"))
    title_label.pack(pady=(0, 10))

    # 5. Создаем таблицу (Treeview)
    columns = ("id", "name", "age", "email")
    tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)

    # Настройка заголовков
    tree.heading("id", text="ID")
    tree.heading("name", text="Имя")
    tree.heading("age", text="Возраст")
    tree.heading("email", text="Email")

    # Настройка ширины колонок
    tree.column("id", width=50)
    tree.column("name", width=150)
    tree.column("age", width=80)
    tree.column("email", width=200)

    # 6. Добавляем скроллбар
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # 7. Упаковываем виджеты в фрейм
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # 8. Кнопка обновления
    btn_refresh = tk.Button(main_frame, text="Обновить данные", command=on_refresh)
    btn_refresh.pack(pady=10)

    # 9. Загружаем данные при старте
    load_data()

    # Запуск цикла событий
    root.mainloop()

if __name__ == "__main__":
    main()