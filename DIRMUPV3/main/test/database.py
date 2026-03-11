import sqlite3
import os

# Имя файла базы данных
DB_NAME = "app.db"

def get_connection():
    """Создает и возвращает соединение с базой данных."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    """Инициализирует базу данных, создавая таблицу, если её нет."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Создаем таблицу Users, если её нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT
        )
    ''')
    
    # Добавим тестовые данные, если таблица пуста
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        test_data = [
            ("Иван Иванов", 25, "ivan@example.com"),
            ("Мария Петрова", 30, "maria@example.com"),
            ("Алексей Сидоров", 22, "alex@example.com")
        ]
        cursor.executemany("INSERT INTO users (name, age, email) VALUES (?, ?, ?)", test_data)
        conn.commit()
        print("База данных создана и заполнена тестовыми данными.")
    
    conn.close()

def get_all_users():
    """Возвращает все записи из таблицы users."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    conn.close()
    return data