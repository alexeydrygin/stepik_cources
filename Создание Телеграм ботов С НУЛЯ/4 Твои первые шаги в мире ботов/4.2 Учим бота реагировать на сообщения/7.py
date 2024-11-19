from aiogram import Bot, Dispatcher, filters
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters.command import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

dp = Dispatcher()

# Создаем кнопки
button_about = KeyboardButton(text="Обо мне")
button_contacts = KeyboardButton(text="Контакты")
button_services = KeyboardButton(text="Услуги")
button_reviews = KeyboardButton(text="Отзывы")
button_menu = KeyboardButton(text="Меню")

# Создаем клавиатуру с кнопками

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [button_about, button_contacts],
        [button_services, button_reviews],
        [button_menu]
    ],
    resize_keyboard=True
)


@dp.message(filters.Command('start'))
async def start_command(message: Message) -> None:
    await message.answer(f'Добрый день, {message.from_user.full_name}\nРад вас видеть! Выберите опцию:', reply_markup=keyboard)

@dp.message(F.text == 'Обо мне')
async def about_me_handler(message: Message) -> None:
    await message.answer('Я - ваш виртуальный помощник, созданный для упрощения вашей жизни. Моя задача - помочь вам с вопросами и задачами.')


@dp.message(F.text == 'Контакты')
async def contacts_handler(message: Message) -> None:
    await message.answer('Вы можете связаться со мной по электронной почте: example@mail.com или по телефону: +123456789.')


@dp.message(F.text == 'Услуги')
async def services_handler(message: Message) -> None:
    await message.answer('Я предлагаю следующие услуги: консультации, поддержка 24/7, помощь в обучении.')


@dp.message(F.text == 'Отзывы')
async def reviews_handler(message: Message) -> None:
    await message.answer('Вот что говорят о нас: "Отличный сервис!", "Очень помогли!", "Рекомендую всем!".')


@dp.message(F.text == 'Меню')
async def menu_handler(message: Message) -> None:
    await message.answer('Мои команды:\n\nОбо мне - узнать о вас\nКонтакты - ваши контактные данные\nУслуги - список услуг\nОтзывы - отзывы клиентов', reply_markup=keyboard)


@dp.message()
async def all_handler(message: Message) -> None:
    await message.answer('Я ловлю всех и вся')


async def main() -> None:
    token = "7504272217:AAEYW-RU0hbkIdqXJpeP9os0xMF_oYdTc98"
    bot = Bot(token)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('\n'*80)
        print("Программа прервана. Выполняется очистка...")
        

