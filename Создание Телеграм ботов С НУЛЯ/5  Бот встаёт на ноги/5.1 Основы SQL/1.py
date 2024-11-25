import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import aiosqlite
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Загружает переменные окружения из .env файла


dp = Dispatcher()


async def create_table():
    connect = await aiosqlite.connect('db.db')
    cursor = await connect.cursor()
    await cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT
        )
    ''')
    await connect.commit()
    await cursor.close()
    await connect.close()

    
async def add_user(user_id, full_name, username):
    connect = await aiosqlite.connect('db.db')
    cursor = await connect.cursor()
    check_user = await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    check_user = await check_user.fetchone()
    if check_user is None:
        await cursor.execute('INSERT INTO users (user_id, full_name, username) VALUES (?, ?, ?)',
                             (user_id, full_name, username))
        await connect.commit()
    await cursor.close()
    await connect.close()


@dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer('Добро пожаловать!')


async def main() -> None:
    try:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise ValueError("Токен бота не найден в переменных окружения")

        print('\n' * 10)
        logger.info("Бот запущен. Ожидание обновлений...")
        bot = Bot(token)
        await create_table()
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n' * 80)
        print("Программа прервана. Выполняется очистка...")
