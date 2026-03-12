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

    # Удаляем старую таблицу, если она есть (для сброса структуры)
    cursor.execute("DROP TABLE IF EXISTS orders")
    
    # Создаем таблицу Orders
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            requestid INTEGER PRIMARY KEY AUTOINCREMENT,
            startdate TEXT NOT NULL,
            cartype TEXT NOT NULL,
            carmodel TEXT NOT NULL,
            problemdescription TEXT NOT NULL,
            requeststatus TEXT NOT NULL,
            completiondate TEXT,
            repairparts TEXT,
            masterid INTEGER,
            clientid INTEGER NOT NULL,
            comment TEXT
        )
    ''')
    
    # Добавим тестовые данные, если таблица пуста
    cursor.execute("SELECT COUNT(*) FROM orders")
    if cursor.fetchone()[0] == 0:
        test_data = [
            ("2023-06-06", "Легковая", "Hyundai Avante (CN7)", "Отказали тормоза.", "В процессе ремонта", None, None, 2, 7, "Очень странно."),
            ("2023-05-05", "Легковая", "Nissan 180SX", "Отказали тормоза.", "В процессе ремонта", None, None, 3, 8, "Будем разбираться!"),
            ("2022-07-07", "Легковая", "Toyota 2000GT", "В салоне пахнет бензином.", "Готова к выдаче", "2023-01-01", None, None, 9, "Будем разбираться!"),
            ("2023-08-02", "Грузовая", "Citroen Berlingo (B9)", "Руль плохо крутится.", "Новая заявка", None, None, None, 8, None),
            ("2023-08-02", "Грузовая", "УАЗ 2360", "Руль плохо крутится.", "Новая заявка", None, None, None, 9, None)
        ]
        cursor.executemany("INSERT INTO orders (startdate, cartype, carmodel, problemdescription, requeststatus, completiondate, repairparts, masterid, clientid, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", test_data)
        conn.commit()
        print("База данных создана и заполнена тестовыми данными.")
    else:
        print("База данных заказов уже существует.")
    
    conn.close()

def get_all_orders():
    """Возвращает все записи из таблицы orders."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    data = cursor.fetchall()
    conn.close()
    return data

def get_orders_by_client_id(client_id):
    """Возвращает заказы конкретного клиента."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE clientid = ?", (client_id,))
    data = cursor.fetchall()
    conn.close()
    return data

def get_order_by_id(order_id):
    """Возвращает заказ по ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders WHERE requestid = ?", (order_id,))
    data = cursor.fetchone()
    conn.close()
    return data

def create_order(startdate, cartype, carmodel, problemdescription, requeststatus, client_id, completiondate=None, repairparts=None, masterid=None, comment=None):
    """Создаёт новый заказ."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO orders (startdate, cartype, carmodel, problemdescription, requeststatus, completiondate, repairparts, masterid, clientid, comment) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (startdate, cartype, carmodel, problemdescription, requeststatus, completiondate, repairparts, masterid, client_id, comment))
        
        conn.commit()
        print(f"Заказ успешно создан!")
        return True
    except Exception as e:
        print(f"Ошибка создания заказа: {str(e)}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()

def update_order(order_id, **kwargs):
    """Обновляет заказ по ID. kwargs - только поля, которые нужно изменить"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Формируем SQL запрос только с изменёнными полями
        if kwargs:
            set_clause = ", ".join([f"{key} = ?" for key in kwargs.keys()])
            values = list(kwargs.values())
            values.append(order_id)

            cursor.execute(f"UPDATE orders SET {set_clause} WHERE requestid = ?", values)
            conn.commit()
            print("Заказ {order_id} успешно обновлён!")
        else:
            print("Нет данных для обновления")

        return True
    except Exception as e:
        print(f"Ошибка обновления: {str(e)}")
        if conn:
            conn.rollback()
        return False
    finally:
        if conn:
            conn.close()