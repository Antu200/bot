from telethon import TelegramClient, events
import sqlite3
from config import config
import logging

# Настройка логгирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    # Подключение к базе данных SQLite
    conn = sqlite3.connect('databases/users/users.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS messaged_users (user_id INTEGER PRIMARY KEY)''')
    conn.commit()
    logging.info('База данных SQLite успешно инициализирована')
except Exception as e:
    logging.error(f'Ошибка при инициализации базы данных SQLite: {e}')

try:
    # Создание клиента Telegram
    client = TelegramClient('anon', config.api_id, config.api_hash)
    logging.info('Клиент Telegram успешно создан')
except Exception as e:
    logging.error(f'Ошибка при создании клиента Telegram: {e}')

@client.on(events.NewMessage(chats=config.channel_username))
async def handler(event):
    try:
        user_id = event.sender_id
        cursor.execute('SELECT user_id FROM messaged_users WHERE user_id = ?', (user_id,))
        if cursor.fetchone() is None:
            cursor.execute('INSERT INTO messaged_users (user_id) VALUES (?)', (user_id,))
            conn.commit()
            logging.info(f'Новый пользователь {user_id} добавлен в базу данных')
            try:
                await client.send_message(-4095716021, f'{user_id} впервые написал в чат {config.channel_username}!')
                logging.info(f'Сообщение о новом пользователе {user_id} отправлено')
            except Exception as e:
                logging.error(f'Ошибка при отправке сообщения о новом пользователе {user_id}: {e}')
    except Exception as e:
        logging.error(f'Ошибка при обработке нового сообщения: {e}')

async def main():
    try:
        await client.start()
        logging.info('Клиент Telegram успешно запущен')
        await client.run_until_disconnected()
    except Exception as e:
        logging.error(f'Ошибка при запуске клиента Telegram: {e}')
    finally:
        conn.close()
        logging.info('Соединение с базой данных SQLite закрыто')

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())