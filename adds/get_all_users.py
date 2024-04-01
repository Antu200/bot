import sqlite3

# Подключаемся к SQLite базе данных
conn = sqlite3.connect('../databases/users/users.db')
cursor = conn.cursor()

# Выбираем и выводим всех пользователей из таблицы
cursor.execute('SELECT * FROM messaged_users')
for row in cursor.fetchall():
    print(row)

conn.close()
