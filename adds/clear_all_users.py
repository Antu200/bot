import sqlite3

# Подключаемся к SQLite базе данных
conn = sqlite3.connect('../databases/users/users.db')
cursor = conn.cursor()

# Выбираем и выводим всех пользователей из таблицы
cursor.execute('DELETE FROM messaged_users')
conn.commit()
conn.close()
