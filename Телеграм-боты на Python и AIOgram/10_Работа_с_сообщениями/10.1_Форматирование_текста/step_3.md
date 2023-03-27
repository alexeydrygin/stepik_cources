## MarkdownV2 style
----------------

**Markdown** - это тоже язык разметки, позволяющий выделять участки текста для лучшей читаемости, структурированности или привлечения внимания пользователя. Markdown считается более простым, чем HTML, хотя лично я больше люблю HTML. Сейчас Markdown style практически не используется, а ему на смену пришел более продвинутый MarkdownV2 style. Если что-то будет не до конца понятно из примеров ниже - не стесняйтесь обращаться к [официальной документации](https://core.telegram.org/bots/api#markdownv2-style).

В MarkdownV2 поддерживается следующая разметка:

*   \*Жирный текст\*
    
    ![](https://ucarecdn.com/6d858467-cdfd-4a72-b76e-862248414a30/-/preview/-/enhance/79/)
    
*   \_Наклонный текст\_
    
    ![](https://ucarecdn.com/96d9815c-4e5d-4c9a-afa9-421968915d88/-/preview/-/enhance/84/)
    
*   \_\_Подчеркнутый текст\_\_
    
    ![](https://ucarecdn.com/a054a892-785a-4206-8352-5babc5b70b5e/-/preview/-/enhance/81/)
    
*   ~Перечеркнутый текст~
    
    ![](https://ucarecdn.com/9c5a06f1-5b89-42bb-af3e-930832a9539c/-/preview/-/enhance/76/)
    
*   ||Спойлер||
    
    ![](https://ucarecdn.com/7506a1ca-d297-461b-bc9f-acf49ca4b003/-/preview/-/enhance/80/)
    
*   \[Внешняя ссылка\](https://stepik.org/120924)
    
    ![](https://ucarecdn.com/a0537b4f-c666-4110-aa1f-51b75c1a2c2a/-/preview/-/enhance/82/)
    
*   \[Внутренняя ссылка\](tg://user?id=173901673)
    
    ![](https://ucarecdn.com/be53ae18-7ee6-4449-a296-4370fe74345a/-/preview/-/enhance/78/)
    
*   \`Моноширинный текст\`
    
    ![](https://ucarecdn.com/b5f2b632-fd96-485e-8d2a-b75acc17f92a/-/preview/-/enhance/79/)
    
*   \`\`\`  
    Предварительно отформатированный текст  
    \`\`\`
    
    ![](https://ucarecdn.com/dcaf31bd-0b04-4bed-8841-5f2d5d912d9e/-/preview/-/enhance/85/)
    
*   \`\`\`python  
    Предварительно отформатированный блок кода на языке Python  
    \`\`\`
    
    ![](https://ucarecdn.com/c5e23843-5ce9-4b8a-aff9-421c12ec41ae/-/preview/-/enhance/82/)
    

Так же, как и в случае с HTML-разметкой, можно комбинировать некоторые способы разметки в MarkdownV2

*     \*\_Жирный наклонный текст\_\*
    
    ![](https://ucarecdn.com/56db0add-1c8d-45fc-99d5-9153b8768ea2/-/preview/-/enhance/81/)
    
*   \_\_\_Наклонный подчеркнутый текст\_\\r\_\_
    
    ![](https://ucarecdn.com/2b680a78-39d1-4734-91cf-d909bedf6c16/-/preview/-/enhance/77/)
    
*   \*\_\_\_Жирный наклонный подчеркнутый текст\_\\r\_\_\*
    
    ![](https://ucarecdn.com/7922c2b2-5a5f-4230-b9e2-5c815037d3d2/-/preview/-/enhance/84/)
    

**Примечание 1.** Символы при работе в режиме MarkdownV2, которые не должны восприниматься телеграмом как часть разметки, должны быть экранированы символом '\\'

**Примечание 2.** В случае, когда текст должен быть написан курсивом и подчеркнут одновременно, кажущееся логичным форматирование вида `___Наклонный подчеркнутый текст___` будет приводить к ошибке. Необходимо добавить специальный символ '\\r' после первого подчеркивания в конце форматированного текста. То есть правильным вариантом будет `___Наклонный подчеркнутый текст_\r__`.

Ниже привожу код бота, демонстрирующего как работает MarkdownV2-разметка. Запустите бота и поэкспериментируйте с ним, чтобы лучше понять как такая разметка работает. Попробуйте временно отключить `parse_mode='MarkdownV2'`, чтобы посмотреть как бот будет отображать разметку с выключенным режимом форматирования.

    from aiogram import Bot, Dispatcher
    from aiogram.filters import Command, CommandStart
    from aiogram.types import Message
    
    # Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
    # полученный у @BotFather
    BOT_TOKEN = 'BOT TOKEN HERE'
    
    bot: Bot = Bot(BOT_TOKEN, parse_mode='MarkdownV2')
    dp: Dispatcher = Dispatcher()
    
    
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(
                text='Привет\!\n\nЯ бот, демонстрирующий '
                     'как работает разметка MardownV2\. Отправь команду '
                     'из списка ниже:\n\n'
                     '/bold \- жирный текст\n'
                     '/italic \- наклонный текст\n'
                     '/underline \- подчеркнутый текст\n'
                     '/strike \- зачеркнутый текст\n'
                     '/spoiler \- спойлер\n'
                     '/link \- внешняя ссылка\n'
                     '/tglink \- внутренняя ссылка\n'
                     '/code \- моноширинный текст\n'
                     '/pre \- предварительно форматированный текст\n'
                     '/precode \- предварительно форматированный блок кода\n'
                     '/boldi \- жирный наклонный текст\n'
                     '/iu \- наклонный подчеркнутый текст\n'
                     '/biu \- жирный наклонный подчеркнутый текст')
    
    
    # Этот хэндлер будет срабатывать на команду "/help"
    @dp.message(Command(commands='help'))
    async def process_help_command(message: Message):
        await message.answer(
                text='Я бот, демонстрирующий '
                     'как работает разметка MardownV2\. Отправь команду '
                     'из списка ниже:\n\n'
                     '/bold \- жирный текст\n'
                     '/italic \- наклонный текст\n'
                     '/underline \- подчеркнутый текст\n'
                     '/strike \- зачеркнутый текст\n'
                     '/spoiler \- спойлер\n'
                     '/link \- внешняя ссылка\n'
                     '/tglink \- внутренняя ссылка\n'
                     '/code \- моноширинный текст\n'
                     '/pre \- предварительно форматированный текст\n'
                     '/precode \- предварительно форматированный блок кода\n'
                     '/boldi \- жирный наклонный текст\n'
                     '/iu \- наклонный подчеркнутый текст\n'
                     '/biu \- жирный наклонный подчеркнутый текст')
    
    
    # Этот хэндлер будет срабатывать на команду "/bold"
    @dp.message(Command(commands='bold'))
    async def process_bold_command(message: Message):
        await message.answer(
                text='\*Это жирный текст\*:\n'
                     '*Это жирный текст*')
    
    
    # Этот хэндлер будет срабатывать на команду "/italic"
    @dp.message(Command(commands='italic'))
    async def process_italic_command(message: Message):
        await message.answer(
                text='\_Это наклонный текст\_:\n'
                     '_Это наклонный текст_')
    
    
    # Этот хэндлер будет срабатывать на команду "/underline"
    @dp.message(Command(commands='underline'))
    async def process_underline_command(message: Message):
        await message.answer(
                text='\_\_Это подчеркнутый текст\_\_:\n'
                     '__Это подчеркнутый текст__')
    
    
    # Этот хэндлер будет срабатывать на команду "/strike"
    @dp.message(Command(commands='strike'))
    async def process_strike_command(message: Message):
        await message.answer(
                text='\~Это зачеркнутый текст\~:\n'
                     '~Это зачеркнутый текст~')
    
    
    # Этот хэндлер будет срабатывать на команду "/spoiler"
    @dp.message(Command(commands='spoiler'))
    async def process_spoiler_command(message: Message):
        await message.answer(
                text='\|\|Это текст под спойлером\|\|:\n'
                     '||Это текст под спойлером||')
    
    
    # Этот хэндлер будет срабатывать на команду "/link"
    @dp.message(Command(commands='link'))
    async def process_link_command(message: Message):
        await message.answer(
                text='\[Внешняя ссылка\]\(https://stepik\.org/120924\):\n'
                     '[Внешняя ссылка](https://stepik.org/120924)')
    
    
    # Этот хэндлер будет срабатывать на команду "/tglink"
    @dp.message(Command(commands='tglink'))
    async def process_tglink_command(message: Message):
        await message.answer(
                text='\[Внутренняя ссылка\]\(tg://user?id\=173901673\):\n'
                     '[Внутренняя ссылка](tg://user?id=173901673)')
    
    
    # Этот хэндлер будет срабатывать на команду "/code"
    @dp.message(Command(commands='code'))
    async def process_code_command(message: Message):
        await message.answer(
                text='\`Моноширинный текст\`:\n'
                     '`Моноширинный текст`')
    
    
    # Этот хэндлер будет срабатывать на команду "/pre"
    @dp.message(Command(commands='pre'))
    async def process_pre_command(message: Message):
        await message.answer(
                text='\`\`\` Предварительно отформатированный текст\`\`\`:\n'
                     '``` Предварительно отформатированный текст```')
    
    
    # Этот хэндлер будет срабатывать на команду "/precode"
    @dp.message(Command(commands='precode'))
    async def process_precode_command(message: Message):
        await message.answer(
                text='\`\`\`python Предварительно отформатированный блок '
                     'кода на языке Python\`\`\`:\n'
                     '```python Предварительно отформатированный блок '
                     'кода на языке Python```')
    
    
    # Этот хэндлер будет срабатывать на команду "/boldi"
    @dp.message(Command(commands='boldi'))
    async def process_boldi_command(message: Message):
        await message.answer(
                text='\*\_Это жирный наклонный текст\_\*:\n'
                     '*_Это жирный наклонный текст_*')
    
    
    # Этот хэндлер будет срабатывать на команду "/iu"
    @dp.message(Command(commands='iu'))
    async def process_iu_command(message: Message):
        await message.answer(
                text='\_\_\_Это наклонный подчеркнутый текст\_\\\\r\_\_:\n'
                     '___Это наклонный подчеркнутый текст_\r__')
    
    
    # Этот хэндлер будет срабатывать на команду "/biu"
    @dp.message(Command(commands='biu'))
    async def process_biu_command(message: Message):
        await message.answer(
                text='\*\_\_\_Это жирный наклонный подчеркнутый текст\_\\\\r\_\_\*:\n'
                     '*___Это жирный наклонный подчеркнутый текст_\r__*')
    
    
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

**Примечание.** Код этого и других уроков доступен на [GitHub](https://github.com/kmsint/aiogram3_stepik_course).