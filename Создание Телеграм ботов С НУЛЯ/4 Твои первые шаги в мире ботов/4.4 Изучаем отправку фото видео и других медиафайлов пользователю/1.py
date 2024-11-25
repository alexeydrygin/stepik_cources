import asyncio
from aiogram import Bot, Dispatcher, types, F
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()  # Загружает переменные окружения из .env файла

dp = Dispatcher()

@dp.message()
async def file_handler(message: types.Message) -> None:
    print(message.document.file_id)


# @dp.message()
# async def echo_handler(message: types.Message) -> None:
#     await message.answer('Подождите, пожалуйста, я думаю...')
#     await asyncio.sleep(5)
#     await message.send_copy(chat_id=message.chat.id)

async def main() -> None:
    try:
        token = os.getenv("TELEGRAM_BOT_TOKEN")
        if not token:
            raise ValueError("Токен бота не найден в переменных окружения")

        print('\n' * 10)
        logger.info("Бот запущен. Ожидание обновлений...")
        bot = Bot(token)
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n' * 80)
        print("Программа прервана. Выполняется очистка...")



