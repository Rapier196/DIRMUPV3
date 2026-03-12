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

    # Удаляем старую таблицу, если она есть
    cursor.execute("DROP TABLE IF EXISTS profiles")
    
    # Создаем таблицу Profiles
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fio TEXT NOT NULL,
            phone INTEGER UNIQUE NOT NULL,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL 
        )
    ''')
    
    # Добавим тестовые данные, если таблица пуста
    cursor.execute("SELECT COUNT(*) FROM profiles")
    if cursor.fetchone()[0] == 0:
        test_data = [
            ("Белов Александр Давидович", 89210563128, "login1", hash_password("pass1"), "manager"),
            ("Харитонова Мария Павловна", 89535078985, "login2", hash_password("pass2"), "mechanic"),
            ("Марков Давид Иванович", 89210673849, "login3", hash_password("pass3"), "mechanic"),
            ("Громова Анна Семёновна", 89990563748, "login4", hash_password("pass4"), "admin"),
            ("Карташова Мария Данииловна", 89994563847, "login5", hash_password("pass5"), "admin"),
            ("Касаткин Егор Львович", 89219567849, "login11", hash_password("pass11"), "client"),
            ("Ильина Тамара Даниловна", 89219567842, "login12", hash_password("pass12"), "client"),
            ("Елисеева Юлиана Алексеевна", 89216234542, "login13", hash_password("pass13"), "client"),
            ("Никифорова Алиса Тимофеевна", 89219567843, "login14", hash_password("pass14"), "client"),
            ("Васильев Али Евгеньевич", 89219567844, "login15", hash_password("pass15"), "mechanic")
        ]
        cursor.executemany("INSERT INTO profiles (fio, phone, login, password, role) VALUES (?, ?, ?, ?, ?)", test_data)
        conn.commit()
        print("База данных создана и заполнена тестовыми данными.")
    else:
        print("База данных пользователей уже существует.")
    
    conn.close()

def hash_password(password):
    """Хэширует пароль для безопасности."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(login, password):
    """Проверяет логин и пароль."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password, role, id FROM profiles WHERE login = ?", (login,))
    result = cursor.fetchone()
    conn.close()

    if result:
        stored_password, role, user_id = result
        if stored_password == hash_password(password):
            return True, role, user_id
    return False, None, None

def get_client_id_by_login(login):
    """Возвращает ID клиента по логину."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM profiles WHERE login = ? AND role = 'client'", (login,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None