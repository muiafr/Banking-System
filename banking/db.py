from os import getenv


import mysql.connector
from dotenv import load_dotenv

load_dotenv()

MYSQL_HOST = getenv("MYSQL_HOST")
MYSQL_USER = getenv("MYSQL_USER")
MYSQL_PASSWORD = getenv("MYSQL_PASSWORD")
MYSQL_DATABASE = getenv("MYSQL_DATABASE")


def get_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
    )


def ensure_tables():
    connect = get_connection()
    cursor = connect.cursor()
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nickname VARCHAR(50) NOT NULL UNIQUE,
                first_name VARCHAR(50) NOT NULL,
                last_name VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL UNIQUE,
                phone_number VARCHAR(20) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                balance DECIMAL(10, 2) DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                sender_id INT NOT NULL,
                recipient_id INT NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                created_at DATETIME NOT NULL,
                FOREIGN KEY (sender_id) REFERENCES users(id),
                FOREIGN KEY (recipient_id) REFERENCES users(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS deposits (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                created_at DATETIME NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        connect.commit()
    finally:
        cursor.close()
        connect.close()




def _row_to_user_dict(row):
    if row is None:
        return None
    return {
        "id": row[0],
        "user_nickname": row[1],
        "first_name": row[2],
        "last_name": row[3],
        "email": row[4],
        "phone_number": row[5],
        "balance": row[6],
    }


def find_user_by_id(cursor, user_id):
    cursor.execute(
        "SELECT id, nickname, first_name, last_name, email, phone_number, balance "
        "FROM users WHERE id = %s",
        (user_id,)
    )
    return _row_to_user_dict(cursor.fetchone())


def find_user_by_nickname(cursor, nickname):
    cursor.execute(
        "SELECT id, nickname, first_name, last_name, email, phone_number, balance "
        "FROM users WHERE nickname = %s",
        (nickname,)
    )
    return _row_to_user_dict(cursor.fetchone())


def find_user_by_email(cursor, email):
    cursor.execute(
        "SELECT id, nickname, first_name, last_name, email, phone_number, balance "
        "FROM users WHERE email = %s",
        (email,)
    )
    return _row_to_user_dict(cursor.fetchone())


def find_user_by_phone(cursor, phone_number):
    cursor.execute(
        "SELECT id, nickname, first_name, last_name, email, phone_number, balance "
        "FROM users WHERE phone_number = %s",
        (phone_number,)
    )
    return _row_to_user_dict(cursor.fetchone())


def insert_user(cursor, nickname, first_name, last_name, email, phone_number, password_hash, balance):
    cursor.execute(
        "INSERT INTO users (nickname, first_name, last_name, email, phone_number, password, balance) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (nickname, first_name, last_name, email, phone_number, password_hash, balance)
    )
    return cursor.lastrowid


def update_user_field(cursor, user_id, field, value):
    allowed_fields = {"nickname", "email", "phone_number", "password"}
    if field not in allowed_fields:
        raise ValueError(f"Недопустимое поле для обновления: {field}")
    cursor.execute(f"UPDATE users SET {field} = %s WHERE id = %s", (value, user_id))


def delete_user_by_id(cursor, user_id):
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))


def get_balance_for_update(cursor, user_id):
    """Читает баланс с блокировкой строки — использовать только внутри start_transaction()."""
    cursor.execute("SELECT balance FROM users WHERE id = %s FOR UPDATE", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else None


def adjust_balance(cursor, user_id, delta):
    cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (delta, user_id))


def insert_transaction(cursor, sender_id, recipient_id, amount, created_at):
    cursor.execute(
        "INSERT INTO transactions (sender_id, recipient_id, amount, created_at) "
        "VALUES (%s, %s, %s, %s)",
        (sender_id, recipient_id, amount, created_at)
    )
    return cursor.lastrowid


def list_transactions_for_user(cursor, user_id):
    cursor.execute(
        "SELECT id, sender_id, recipient_id, amount, created_at FROM transactions "
        "WHERE sender_id = %s OR recipient_id = %s ORDER BY created_at DESC",
        (user_id, user_id)
    )
    return cursor.fetchall()



def insert_deposit(cursor, user_id, amount, created_at):
    cursor.execute(
        "INSERT INTO deposits (user_id, amount, created_at) VALUES (%s, %s, %s)",
        (user_id, amount, created_at)
    )
    return cursor.lastrowid