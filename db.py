import sqlite3

def init_db():
    conn = sqlite3.connect('maun.db')
    cursor = conn.cursor()

    # Groups table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            telegram_id INTEGER,
            name TEXT,
            is_admin BOOLEAN,
            FOREIGN KEY (group_id) REFERENCES groups(id)
        )
    ''')

    # Items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            user_id INTEGER,
            name TEXT,
            category TEXT,
            expiry_date TEXT,
            is_taken BOOLEAN,
            taken_by INTEGER,
            FOREIGN KEY (group_id) REFERENCES groups(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
