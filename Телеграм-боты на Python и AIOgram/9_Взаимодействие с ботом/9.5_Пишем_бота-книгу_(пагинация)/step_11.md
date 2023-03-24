## Клавиатуры: main_menu.py
-------------------------

В пакете 📁**keyboards** хранятся функции, помогающие генерировать клавиатуры, которые бот будет отправлять пользователю в процессе взаимодействия.

Начнем с файла **main\_menu.py**. Ранее я говорил, что это не совсем клавиатура, это команды, которые будут отображаться в главном меню бота, при нажатии на кнопку "Menu". Думаю, особые пояснения к коду из этого файла не требуются. Мы его подробно разбирали в этом модуле, в уроке, посвященном кнопке "Menu".

### main\_menu.py

    from aiogram import Bot
    from aiogram.types import BotCommand
    
    from lexicon.lexicon import LEXICON_COMMANDS
    
    
    # Функция для настройки кнопки Menu бота
    async def set_main_menu(bot: Bot):
        main_menu_commands = [BotCommand(
            command=command,
            description=description
        ) for command,
            description in LEXICON_COMMANDS.items()]
        await bot.set_my_commands(main_menu_commands)

 После того, как отработает асинхронная функция `set_main_menu` - у бота появится соответствующее меню:

![](https://ucarecdn.com/16a34931-4203-4cf7-a113-23011cdebaf9/-/preview/-/enhance/81/)

Иногда кнопка "Menu" появляется или меняется не сразу. Если, вдруг, у вас так - попробуйте закрыть и снова открыть телеграм-клиент.