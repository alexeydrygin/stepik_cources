import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message

dp = Dispatcher()

@dp.message(Command('start'))
async def start_command(message: Message) -> None:
    await message.answer(f'Добрый день, {message.from_user.full_name}\nРад вас видеть, напишите Меню, чтобы узнать мои команды')

@dp.message(F.text == 'Меню')
async def menu_handler(message: Message) -> None:
    await message.answer('Мои команды\n\nПривет - я тебе отвечу привет!\nМорс - я расскажу о том, какой вкусный облепиховый морс')

@dp.message(F.text == 'Привет')
async def hello_handler(message: Message) -> None:
    await message.answer('Привет! Как у тебя дела?')

@dp.message(F.text == 'Морс')
async def morse_handler(message: Message) -> None:
    await message.answer('Ты не представляешь какой вкусный морс я сегодня пил. Мне кажется, он вызывает зависимость')

@dp.message()
async def all_handler(message: Message) -> None:
    await message.answer('Я ловлю всех и вся')

async def main() -> None:
    token = "7504272217:AAEYW-RU0hbkIdqXJpeP9os0xMF_oYdTc98"
    bot = Bot(token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
