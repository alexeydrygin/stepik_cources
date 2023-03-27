## Форматирование текста в сообщениях
----------------------------------

Когда я только начинал знакомство с телеграм-ботами, где-то мне попалась информация о том, что можно форматировать сообщения с помощью HTML-тегов. Я тогда подумал: вот это круто! Это можно же любой текст с любым оформлением сделать! И сразу пошел пытаться экспериментировать с тегом `<style>`, который отвечает за стили. Ну, как вы, наверное, можете догадаться, ничего у меня не получилось. Оказалось, что количество тегов, поддерживаемых Telegram, сильно ограничено. И тем не менее, немного разнообразить текст все-таки можно.

Мы уже с вами пользовались режимом форматирования "HTML", когда писали ботов, но я не заострял на этом особого внимания. Пришло время разобраться с данным вопросом подробнее.

Telegram поддерживает три способа разметки текста:

*   **HTML style**
*   **Markdown style**
*   **MarkdownV2 style**

При этом поддержка **Markdown style**, начиная с третьей версии `aiogram`, не планируется, поэтому мы на нем не будем останавливаться. Разберем **HTML sytle** и **MarkdownV2 style**.

Чтобы включить поддержку требуемого стиля, надо либо в каждом отправляемом сообщении указывать параметр `parse_mode`, либо сделать это один раз на этапе инициализации бота. Второй способ, конечно, предпочтительнее, потому что требует написания меньшего количества кода, но и про первый нужно знать, мало ли какие ситуации могут быть.

### Пример кода с параметром `parse_mode` в отдельном сообщении.

Напишем самого простого бота с несколькими хэндлерами. В некоторых из них будем указывать параметр `parse_mode` при отправке сообщений, а в других не будем, чтобы лучше понять разницу.

    from aiogram import Bot, Dispatcher
    from aiogram.filters import Command, CommandStart
    from aiogram.types import Message
    
    # Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
    # полученный у @BotFather
    BOT_TOKEN = 'BOT TOKEN HERE'
    
    bot: Bot = Bot(BOT_TOKEN)
    dp: Dispatcher = Dispatcher()
    
    
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(
                text='Привет!\n\nЯ бот, демонстрирующий '
                     'как работает разметка. Отправь команду '
                     'из списка ниже:\n\n'
                     '/html - пример разметки с помощью HTML\n'
                     '/markdownv2 - пример разметки с помощью MarkdownV2\n'
                     '/noformat - пример с разметкой, но без указания '
                     'параметра parse_mode')
    
    
    # Этот хэндлер будет срабатывать на команду "/help"
    @dp.message(Command(commands='help'))
    async def process_help_command(message: Message):
        await message.answer(
                text='Я бот, демонстрирующий '
                     'как работает разметка. Отправь команду '
                     'из списка ниже:\n\n'
                     '/html - пример разметки с помощью HTML\n'
                     '/markdownv2 - пример разметки с помощью MarkdownV2\n'
                     '/noformat - пример с разметкой, но без указания '
                     'параметра parse_mode')
    
    
    # Этот хэндлер будет срабатывать на команду "/html"
    @dp.message(Command(commands='html'))
    async def process_html_command(message: Message):
        await message.answer(
                text='Это текст, демонстрирующий '
                     'как работает HTML-разметка:\n\n'
                     '<b>Это жирный текст</b>\n'
                     '<i>Это наклонный текст</i>\n'
                     '<u>Это подчеркнутый текст</u>\n'
                     '<span class="tg-spoiler">А это спойлер</span>\n\n'
                     'Чтобы еще раз посмотреть список доступных команд - '
                     'отправь команду /help',
                parse_mode='HTML')
    
    
    # Этот хэндлер будет срабатывать на команду "/markdownv2"
    @dp.message(Command(commands='markdownv2'))
    async def process_markdownv2_command(message: Message):
        await message.answer(
                text='Это текст, демонстрирующий '
                     'как работает MarkdownV2\-разметка:\n\n'
                     '*Это жирный текст*\n'
                     '_Это наклонный текст_\n'
                     '__Это подчеркнутый текст__\n'
                     '||А это спойлер||\n\n'
                     'Чтобы еще раз посмотреть список доступных команд \- '
                     'отправь команду /help',
                parse_mode='MarkdownV2')
    
    
    # Этот хэндлер будет срабатывать на команду "/noformat"
    @dp.message(Command(commands='noformat'))
    async def process_noformat_command(message: Message):
        await message.answer(
                text='Это текст, демонстрирующий '
                     'как отображается текст, если не указать '
                     'параметр parse_mode:\n\n'
                     '<b>Это мог бы быть жирный текст</b>\n'
                     '_Это мог бы быть наклонный текст_\n'
                     '<u>Это мог бы быть подчеркнутый текст</u>\n'
                     '||А это мог бы быть спойлер||\n\n'
                     'Чтобы еще раз посмотреть список доступных команд - '
                     'отправь команду /help')
    
    
    # Этот хэндлер будет срабатывать на любые сообщения, кроме команд,
    # отлавливаемых хэндлерами выше
    @dp.message()
    async def send_echo(message: Message):
        await message.answer(
                text='Я даже представить себе не могу, '
                     'что ты имеешь в виду\n\n'
                     'Чтобы посмотреть список доступных команд - '
                     'отправь команду /help')
    
    
    # Запускаем поллинг
    if __name__ == '__main__':
        dp.run_polling(bot)

Запустите бота и посмотрите как выглядит разметка. Ниже скриншот HTML-разметки.

![](https://ucarecdn.com/a26da865-0a5c-4284-b5ef-3dd53c5e893c/-/preview/-/enhance/75/)

### Пример кода с параметром `parse_mode` в объекте бота.

Здесь мы уже не указываем параметр `parse_mode` в каждом отправляемом сообщении, а делаем это один раз при инициализации объекта бота.

    from aiogram import Bot, Dispatcher
    from aiogram.filters import Command, CommandStart
    from aiogram.types import Message
    
    # Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
    # полученный у @BotFather
    BOT_TOKEN = 'BOT TOKEN HERE'
    
    bot: Bot = Bot(BOT_TOKEN, parse_mode='HTML')
    dp: Dispatcher = Dispatcher()
    
    
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(
                text='Привет!\n\nЯ бот, демонстрирующий '
                     'как работает HTML-разметка. Отправь команду '
                     'из списка ниже:\n\n'
                     '/bold - жирный текст\n'
                     '/italic - наклонный текст\n'
                     '/underline - подчеркнутый текст\n'
                     '/spoiler - спойлер')
    
    
    # Этот хэндлер будет срабатывать на команду "/help"
    @dp.message(Command(commands='help'))
    async def process_help_command(message: Message):
        await message.answer(
                text='Я бот, демонстрирующий '
                     'как работает HTML-разметка. Отправь команду '
                     'из списка ниже:\n\n'
                     '/bold - жирный текст\n'
                     '/italic - наклонный текст\n'
                     '/underline - подчеркнутый текст\n'
                     '/spoiler - спойлер')
    
    
    # Этот хэндлер будет срабатывать на команду "/bold"
    @dp.message(Command(commands='bold'))
    async def process_bold_command(message: Message):
        await message.answer(
                text='<b>Это текст, демонстрирующий '
                     'как работает HTML-разметка, '
                     'делающая текст жирным.\n\n'
                     'Чтобы еще раз посмотреть список доступных команд - '
                     'отправь команду /help</b>')
    
    
    # Этот хэндлер будет срабатывать на команду "/italic"
    @dp.message(Command(commands='italic'))
    async def process_italic_command(message: Message):
        await message.answer(
                text='<i>Это текст, демонстрирующий '
                     'как работает HTML-разметка, '
                     'делающая текст наклонным.\n\n'
                     'Чтобы еще раз посмотреть список доступных команд - '
                     'отправь команду /help</i>')
    
    
    # Этот хэндлер будет срабатывать на команду "/underline"
    @dp.message(Command(commands='underline'))
    async def process_underline_command(message: Message):
        await message.answer(
                text='<u>Это текст, демонстрирующий '
                     'как работает HTML-разметка, '
                     'делающая текст подчеркнутым.\n\n'
                     'Чтобы еще раз посмотреть список доступных команд - '
                     'отправь команду /help</u>')
    
    
    # Этот хэндлер будет срабатывать на команду "/spoiler"
    @dp.message(Command(commands='spoiler'))
    async def process_spoiler_command(message: Message):
        await message.answer(
                text='<tg-spoiler>Это текст, демонстрирующий '
                     'как работает HTML-разметка, '
                     'убирающая текст под спойлер.\n\n'
                     'Чтобы еще раз посмотреть список доступных команд - '
                     'отправь команду /help</tg-spoiler>')
    
    
    # Этот хэндлер будет срабатывать на любые сообщения, кроме команд,
    # отлавливаемых хэндлерами выше
    @dp.message()
    async def send_echo(message: Message):
        await message.answer(
                text='Я даже представить себе не могу, '
                     'что ты имеешь в виду\n\n'
                     'Чтобы посмотреть список доступных команд - '
                     'отправь команду /help')
    
    
    # Запускаем поллинг
    if __name__ == '__main__':
        dp.run_polling(bot)

Также запустите бота и посмотрите, что разметка работает как ожидается.

![](https://ucarecdn.com/232678f6-99f8-468b-927b-f98f32c494fa/-/preview/-/enhance/78/)

**Примечание.** Код этого и других уроков доступен на [GitHub](https://github.com/kmsint/aiogram3_stepik_course).