import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные окружения из .env файла

print("Бот онлайн.")

dp = Dispatcher()

# Импровизированные данные пользователя
user_data = {
    'name': 'Иван',
    'user_id': 123456,
    'balance': 1000
}

# Информация о курсах
courses = {
    'python': {'price': 500, 'description': 'Курс по Python'},
    'aiogram': {'price': 600, 'description': 'Курс по Aiogram'},
    'telebot': {'price': 400, 'description': 'Курс по Telebot'},
    'django': {'price': 700, 'description': 'Курс по Django'}
}


async def send_course_info(callback: types.CallbackQuery, course_key: str):
    course = courses[course_key]
    await callback.message.answer(
        f"{course['description']}\nЦена: {course['price']}₽\n"
        'Нажмите "Купить" для завершения покупки.',
        reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
            [types.InlineKeyboardButton(
                text="Купить", callback_data=f'buy_{course_key}')]
        ])
    )


@dp.message(Command('start'))
async def start_command(message: types.Message) -> None:
    kb = [
        [types.InlineKeyboardButton(text="Каталог", callback_data='catalog')],
        [
            types.InlineKeyboardButton(
                text="Профиль", callback_data='profile'),
            types.InlineKeyboardButton(
                text="Тех. поддержка", callback_data='support')
        ],
        [types.InlineKeyboardButton(text="О нас", callback_data='about')]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await message.answer('=М=А=Г=А=З=И=Н=', reply_markup=keyboard)


@dp.callback_query(F.data == "catalog")
async def catalog_callback(callback: types.CallbackQuery):
    kb = [
        [types.InlineKeyboardButton(
            text=f"Курс по {course['description']}", callback_data=f'course_{key}')]
        for key, course in courses.items()
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer('Выберите курс:', reply_markup=keyboard)


@dp.callback_query(F.data.startswith("course_"))
async def course_callback(callback: types.CallbackQuery):
    course_key = callback.data.split('_')[1]
    if course_key in courses:
        await send_course_info(callback, course_key)
    else:
        await callback.message.answer('Ошибка: курс не найден.')


@dp.callback_query(F.data.startswith("buy_"))
async def buy_course_callback(callback: types.CallbackQuery):
    course_key = callback.data.split('_')[1]
    if course_key in courses:
        price = courses[course_key]['price']
        if user_data['balance'] >= price:
            user_data['balance'] -= price
            await callback.message.answer(f'Вы успешно купили {courses[course_key]["description"]}!\nСкоро вы его получите.')
        else:
            await callback.message.answer('У вас недостаточно средств для покупки этого курса.')
    else:
        await callback.message.answer('Ошибка: курс не найден.')

    await callback.message.answer('Сейчас переведу Вас в главное меню.')
    await asyncio.sleep(3)  # Ждать 3 секунды
    await start_command(callback.message)


@dp.callback_query(F.data == "profile")
async def profile_callback(callback: types.CallbackQuery):
    profile_info = f'Имя: {user_data["name"]}\n' \
                   f'User  ID: {user_data["user_id"]}\n' \
                   f'Баланс: {user_data["balance"]}₽'
    kb = [[types.InlineKeyboardButton(
        text="Назад в меню", callback_data='back_to_menu')]]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=kb)
    await callback.message.answer(profile_info, reply_markup=keyboard)



@dp.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: types.CallbackQuery):
    await start_command(callback.message)


@dp.callback_query(F.data == "support")
async def support_callback(callback: types.CallbackQuery):
    await callback.message.answer('Если у вас есть вопросы, вы можете обратиться к разработчику: @your_developer_username')


@dp.callback_query(F.data == "about")
async def about_callback(callback: types.CallbackQuery):
    about_info = 'Это бот-магазин, который поможет вам приобрести курсы по программированию. ' \
                 'Мы предлагаем качественные материалы и поддержку.'
    await callback.message.answer(about_info)
    


async def main() -> None:
    # Используйте переменные окружения для хранения токена
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = Bot(token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n' * 80)
        print("Программа прервана. Выполняется очистка...")
