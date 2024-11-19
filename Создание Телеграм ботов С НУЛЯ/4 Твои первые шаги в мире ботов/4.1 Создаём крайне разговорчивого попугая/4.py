import asyncio
from aiogram import Bot, Dispatcher, types

dp = Dispatcher()

@dp.message()
async def echo_handler(message: types.Message) -> None:
    await message.answer('Подождите, пожалуйста, я думаю...')
    await asyncio.sleep(5)
    await message.send_copy(chat_id=message.chat.id)

async def main() -> None:
    token = "7504272217:AAEYW-RU0hbkIdqXJpeP9os0xMF_oYdTc98"
    bot = Bot(token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
