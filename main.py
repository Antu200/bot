from telethon import TelegramClient, events
import sqlite3
from config import config

conn = sqlite3.connect('databases/users/users.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS messaged_users (user_id INTEGER PRIMARY KEY)''')
conn.commit()

client = TelegramClient('anon', config.api_id, config.api_hash)

@client.on(events.NewMessage(chats=config.channel_username))
async def handler(event):
    user_id = event.sender_id
    cursor.execute('SELECT user_id FROM messaged_users WHERE user_id = ?', (user_id,))
    if cursor.fetchone() is None:
        cursor.execute('INSERT INTO messaged_users (user_id) VALUES (?)', (user_id,))
        conn.commit()
        await client.send_message(-4095716021, f'{user_id} впервые написал в чат {config.channel_username}!')


async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
