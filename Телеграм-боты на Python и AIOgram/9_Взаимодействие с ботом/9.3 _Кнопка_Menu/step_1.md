## Кнопка "Menu"
-------------

Какое-то время назад в Телеграме появилась возможность добавлять своему боту нативную кнопку "Menu" с командами и их описанием.

![](https://ucarecdn.com/76ce79f6-4c6b-4e51-8b46-4de821faf957/-/preview/-/enhance/83/)

Мы уже [рассматривали ранее](https://stepik.org/lesson/759382/step/7?unit=761398) как можно добавить в главное меню команды через [@BotFather](https://t.me/BotFather), но также это можно сделать и через соотвествующие https-запросы к Telegram Bot API, а соответственно, и средствами библиотеки `aiogram`. Метод `set_my_commands` является репрезентацией метода Telegram Bot API `setMyCommands`:

![](https://ucarecdn.com/c4ad0be5-ff0f-421f-bc10-61101d611622/-/preview/-/enhance/83/)

С использованием `aiogram`, делается это следующим образом:

    from aiogram import Bot, Dispatcher
    from aiogram.types import BotCommand
    
    # Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
    # полученный у @BotFather
    API_TOKEN: str = 'BOT TOKEN HERE'
    
    # Создаем объекты бота и диспетчера
    bot: Bot = Bot(token=API_TOKEN)
    dp: Dispatcher = Dispatcher()
    
    
    # Создаем асинхронную функцию
    async def set_main_menu(bot: Bot):
    
        # Создаем список с командами и их описанием для кнопки menu
        main_menu_commands = [
            BotCommand(command='/help',
                       description='Справка по работе бота'),
            BotCommand(command='/support',
                       description='Поддержка'),
            BotCommand(command='/contacts',
                       description='Другие способы связи'),
            BotCommand(command='/payments',
                       description='Платежи')]
    
        await bot.set_my_commands(main_menu_commands)
    
    
    if __name__ == '__main__':
        # Регистрируем асинхронную функцию в диспетчере,
        # которая будет выполняться на старте бота,
        dp.startup.register(set_main_menu)
        # Запускаем поллинг
        dp.run_polling(bot)

В `aiogram.types` есть специальный класс `BotCommand`, который является репрезентацией типа `BotCommand` из Telegram Bot API.

![](https://ucarecdn.com/4bcd6c87-9c2f-4ffe-ae70-9fccf88ac2fe/-/preview/-/enhance/72/)

У этого класса есть два атрибута:

*   `command` - имя команды, начинающееся с символа `/`
*   `description` - описание, что делает команда

Если у бота вызвать метод `set_my_commands`, передав туда список объектов `BotCommand`, у него появится, если еще не было, кнопка "Menu" со списком переданных команд. Если же кнопка уже была ранее - изменится ее список команд.

![](https://ucarecdn.com/d8523057-0720-443d-b98d-22341379a39d/-/preview/-/enhance/79/)

Нажатие на команды из кнопки "Menu", будет отправлять в чат с ботом соответствующую команду. Это бывает довольно удобно, чтобы не набирать команды вручную.

И некоторое пояснение по инструкции `dp.startup.register(set_main_menu)`, которая нам еще не встречалась ранее. Таким способом можно регистрировать в диспетчере функции, которые должны выполняться при старте бота. По сути, это способ добавить функцию в событийный цикл средствами `aiogram`, не обращаясь напрямую к `asyncio`. Причем, функция эта может быть как синхронной, так и асинхронной, `aiogram` сам разберется как ее выполнить. Подробнее про добавление задач в цикл событий будем говорить в соответствующем уроке.

**Примечание.** Код данного бота, как и остальной код из уроков, доступен на GitHub по [ссылке](https://github.com/kmsint/aiogram3_stepik_course).