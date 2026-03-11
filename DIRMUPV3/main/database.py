import sqlite3
import hashlib
# Имя файла базы данных
DB_NAME = "profiles_list.db"

def get_connection():
    """Создает и возвращает соединение с базой данных."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    """Инициализирует базу данных, создавая таблицу, если её нет."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Создаем таблицу Profiles, если её нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL 
        )
    ''')
    
    # Добавим тестовые данные, если таблица пуста
    cursor.execute("SELECT COUNT(*) FROM profiles")
    if cursor.fetchone()[0] == 0:
        test_data = [
            ("admin", hash_password("admin123"), "admin"),
            ("client", hash_password("client123"), "client"),
            ("manager", hash_password("manager123"), "manager")
        ]
        cursor.executemany("INSERT INTO profiles (login, password, role) VALUES (?, ?, ?)", test_data)
        conn.commit()
        print("База данных создана и заполнена тестовыми данными.")
    
    conn.close()

def hash_password(password):
    """Хэширует пароль для безопасности."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(login, password):
    """Проверяет логин и пароль."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password, role FROM profiles WHERE login = ?", (login,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password, role = result
        if stored_password == hash_password(password):
            return True, role
    return False, None