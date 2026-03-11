import sqlite3
# Имя файла базы данных
DB_NAME = "orders_list.db"

def get_connection():
    """Создает и возвращает соединение с базой данных."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def init_db():
    """Инициализирует базу данных, создавая таблицу, если её нет."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Создаем таблицу Orders, если её нет
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            requestid INTEGER PRIMARY KEY AUTOINCREMENT,
            startdate TEXT NOT NULL,
            cartype TEXT NOT NULL,
            carmodel TEXT NOT NULL,
            problemdescription TEXT NOT NULL,
            requeststatus TEXT NOT NULL,
            completiondate INTEGER,
            repairparts TEXT,
            masterid INTEGER,
            clientid INTEGER NOT NULL
        )
    ''')
    
    # Добавим тестовые данные, если таблица пуста
    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        test_data = [
            ("2023-06-06", "Легковая", "Hyundai Avante (CN7)", "Отказали тормоза.", "В процессе ремонта", None, None, 2, 7),
            ("2023-05-05", "Легковая", "Nissan 180SX", "Отказали тормоза.", "В процессе ремонта", None, None, 3, 8),
            ("2022-07-07", "Легковая", "Toyota 2000GT", "В салоне пахнет бензином.", "Готова к выдаче", "2023-01-01", None, None, 9),
            ("2023-08-02", "Грузовая", "Citroen Berlingo (B9)", "Руль плохо крутится.", "Новая заявка", None, None, None, 8),
            ("2023-08-02", "Грузовая", "УАЗ 2360", "Руль плохо крутится.", "Новая заявка", None, None, None, 9)
        ]
        cursor.executemany("INSERT INTO orders (startdate, cartype, carmodel, problemdescription, requeststatus, completiondate, repairparts, masterid, clientid) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", test_data)
        conn.commit()
        print("База данных создана и заполнена тестовыми данными.")
    
    conn.close()

def get_all_orders():
    """Возвращает все записи из таблицы orders."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    data = cursor.fetchall()
    conn.close()
    return data