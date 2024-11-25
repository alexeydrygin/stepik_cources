import asyncio
import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import aiosqlite
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения из .env файла
load_dotenv()

# Инициализация диспетчера
dp = Dispatcher()

DATABASE_NAME = 'db.db'
db_connection = None  # Глобальная переменная для хранения соединения с базой данных


async def create_table():
    """Создает таблицу пользователей, если она не существует."""
    async with aiosqlite.connect(DATABASE_NAME) as connect:
        async with connect.cursor() as cursor:
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    full_name TEXT,
                    username TEXT
                )
            ''')
            await connect.commit()


async def add_user(user_id, full_name, username):
    """Добавляет пользователя в базу данных, если он еще не существует."""
    async with aiosqlite.connect(DATABASE_NAME) as connect:
        async with connect.cursor() as cursor:
            check_user = await cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
            check_user = await check_user.fetchone()
            if check_user is None:
                await cursor.execute('INSERT INTO users (user_id, full_name, username) VALUES (?, ?, ?)',
                                     (user_id, full_name, username))
                await connect.commit()
                logger.info(f"Пользователь {
                            full_name} добавлен в базу данных.")
            else:
                logger.info(f"Пользователь {
                            full_name} уже существует в базе данных.")


@dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    """Обработчик команды /start."""
    await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer('Добро пожаловать!')


async def main() -> None:
    """Основная функция, запускающая бота."""
    global db_connection
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("Токен бота не найден в переменных окружения")
        return

    logger.info("Бот запущен. Ожидание обновлений...")
    await create_table()
    bot = Bot(token)

    # Сохраняем соединение для дальнейшего использования
    db_connection = await aiosqlite.connect(DATABASE_NAME)

    try:
        await dp.start_polling(bot)
    finally:
        await cleanup()  # Выполнить очистку при завершении работы


async def cleanup():
    """Функция для выполнения очистки при остановке бота."""
    global db_connection
    if db_connection:
        await db_connection.close()  # Закрытие соединения с базой данных
        logger.info("Соединение с базой данных закрыто.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Программа прервана пользователем.")
    except Exception as e:
        logger.exception("Произошла ошибка: %s", str(e))
