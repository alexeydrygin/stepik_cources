## Модульный эхо-бот с применением роутеров
----------------------------------------

Переделать нам надо только 3 модуля - точку входа **bot.py** и модули с хэндлерами. Да, и еще можно удалить модуль, который мы создавали в процессе экспериментирования - **create\_dp.py**.

### bot.py

    import asyncio
    
    from aiogram import Bot, Dispatcher
    from config_data.config import Config, load_config
    from handlers import other_handlers, user_handlers
    
    
    # Функция конфигурирования и запуска бота
    async def main():
    
        # Загружаем конфиг в переменную config
        config: Config = load_config()
        
        # Инициализируем бот и диспетчер
        bot: Bot = Bot(token=config.tg_bot.token)
        dp: Dispatcher = Dispatcher()
    
        # Регистриуем роутеры в диспетчере
        dp.include_router(user_handlers.router)
        dp.include_router(other_handlers.router)
    
        # Пропускаем накопившиеся апдейты и запускаем polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    
    
    if __name__ == '__main__':
        asyncio.run(main())

### user\_handlers.py

    from aiogram import Router
    from aiogram.filters import Command, CommandStart
    from aiogram.types import Message
    from lexicon.lexicon import LEXICON_RU
    
    # Инициализируем роутер уровня модуля
    router: Router = Router()
    
    
    # Этот хэндлер срабатывает на команду /start
    @router.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text=LEXICON_RU['/start'])
    
    
    # Этот хэндлер срабатывает на команду /help
    @router.message(Command(commands='help'))
    async def process_help_command(message: Message):
        await message.answer(text=LEXICON_RU['/help'])

### other\_handlers.py

    from aiogram import Router
    from aiogram.types import Message
    from lexicon.lexicon import LEXICON_RU
    
    # Инициализируем роутер уровня модуля
    router: Router = Router()
    
    
    # Этот хэндлер будет срабатывать на любые ваши сообщения,
    # кроме команд "/start" и "/help"
    @router.message()
    async def send_echo(message: Message):
        try:
            await message.send_copy(chat_id=message.chat.id)
        except TypeError:
            await message.reply(text=LEXICON_RU['no_echo'])

В модулях с хэндлерами изменилось совсем немного. Во-первых, появился импорт класса `Router`.

    from aiogram import Router

Во-вторых, инициализация роутера уровня модуля (то есть этот роутер будет общим на весь модуль).

    # Инициализируем роутер уровня модуля
    router: Router = Router()

Ну, и в-третьих, хэндлеры мы теперь декорируем через объект `router`, а не `dp` как раньше.

    @router.message()
    async def send_echo(message: Message):
        # ...

В точке входа **bot.py** тоже есть ряд изменений. Во-первых, мы теперь безболезненно, не боясь циклических импортов, можем импортировать модули с хэндлерами. Можно, конечно, и роутеры отдельно импортировать, но они у нас в этом примере называются одинаково, поэтому будем их различать по имени модуля, которому принадлежит роутер. То есть `user_handlers.router` и `other_handlers.router`.

    from handlers import other_handlers, user_handlers

И после инициализации диспетчера внутри функции `main` мы подключаем роутеры к диспетчеру с помощью метода `include_router()`

    # Регистриуем роутеры в диспетчере
        dp.include_router(user_handlers.router)
        dp.include_router(other_handlers.router)

Вот теперь, наконец-то можно запустить модульного эхо-бота и убедиться, что все работает. Ура!

![](https://ucarecdn.com/6e94a997-c025-4a41-92dd-8a8993b1adf9/)