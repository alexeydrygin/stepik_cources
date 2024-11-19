import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command

dp = Dispatcher()


# @dp.message(F.text.lower() == 'меню')

@dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    await message.answer(f'Добрый день, {message.from_user.full_name}\nРад вас видеть, напишите Меню, чтобы узнать мои команды')


@dp.message(F.text.lower() == 'меню')
async def menu_handler(message: types.Message) -> None:
    await message.answer('Мои команды\n\nПривет - я тебе отвечу привет!\nМорс - я расскажу о том, какой вкусный облепиховый морс')


@dp.message(F.text.lower() == 'привет')
async def hello_handler(message: types.Message) -> None:
    await message.answer('Привет! Как у тебя дела?')


@dp.message(F.text.lower() == 'морс')
async def morse_handler(message: types.Message) -> None:
    await message.answer('Ты не представляешь какой вкусный морс я сегодня пил. Мне кажется, он вызывает зависимость')


async def main() -> None:
    token = "7504272217:AAEYW-RU0hbkIdqXJpeP9os0xMF_oYdTc98"
    bot = Bot(token)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
