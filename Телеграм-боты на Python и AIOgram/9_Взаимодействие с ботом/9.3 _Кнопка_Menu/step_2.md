## Настройка кнопки "Menu" как часть шаблона
-----------------------------------------

На предыдущем шаге мы с вами рассмотрели принцип, который лежит в основе настройки кнопки "Menu" программным методом, по сути, написав целого отдельного бота. Но не будем же мы каждый раз запускать такого бота, чтобы просто кнопку поменять. Надо встроить функцию настройки кнопки в наш шаблон и запускать ее при старте исполняемого файла **bot.py**.

Есть один вопрос. Где именно хранить настройки этой кнопки в шаблоне? По идее, это конфигурационные настройки, которые устанавливаются один раз при старте бота и, в дальнейшем, при работе бота, больше нигде не используются. Поэтому логично было бы хранить их в файле **config.py**. Но, с другой стороны, кнопка "Menu" - это часть интерфейса взаимодействия пользователя с ботом, а кнопки интерфейса мы договорились хранить в пакете **keyboards**. Я встречал и один и другой подходы и, как мне кажется, они равноправны. Решайте сами какой подход вам ближе. Лично я храню настройки кнопки "Menu" в модуле **set\_menu.py** в пакете **keyboards**. И выглядит этот модуль так:

### set\_menu.py

    from aiogram import Bot
    from aiogram.types import BotCommand
    
    from lexicon.lexicon_ru import LEXICON_COMMANDS_RU
    
    
    # Функция для настройки кнопки Menu бота
    async def set_main_menu(bot: Bot):
        main_menu_commands = [BotCommand(
                                    command=command,
                                    description=description
                              ) for command,
                                    description in LEXICON_COMMANDS_RU.items()]
        await bot.set_my_commands(main_menu_commands)

Команды и их описания хранятся в модуле **lexicon\_ru.py** пакета **lexicon**, в словаре `LEXICON_COMMANDS_RU`

### lexicon\_ru.py

    LEXICON_COMMANDS_RU: dict[str, str] = {
                    '/command_1': 'command_1 desription',
                    '/command_2': 'command_2 desription',
                    '/command_3': 'command_3 desription',
                    '/command_4': 'command_4 desription'}

А саму функцию `set_main_menu` из модуля **set\_menu.py** я вызываю в исполняемом файле **bot.py** внутри функции `main` после инициализации бота и диспетчера. Не забывая о том, что функция асинхронная:

### bot.py

    # ...
    
    from aiogram import Bot, Dispatcher
    from keyboards.set_menu import set_main_menu
    
    # ...
    
    
    # Функция конфигурирования и запуска бота
    async def main():
        # ...
    
        # Инициализируем бот и диспетчер
        bot: Bot = Bot(token=config.tg_bot.token,
                       parse_mode='HTML')
        dp: Dispatcher = Dispatcher()
    
        # Настраиваем кнопку Menu
        await set_main_menu(bot)
    
        # ...