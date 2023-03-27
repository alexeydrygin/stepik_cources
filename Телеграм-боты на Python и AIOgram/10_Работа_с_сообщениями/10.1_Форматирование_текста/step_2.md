## HTML style
----------

Если вы уже раньше сталкивались с HTML-разметкой, например, при создании или правке web-страниц, никаких сложностей у вас возникнуть не должно - принцип тот же. Но даже если не сталкивались - сейчас расскажу и покажу. Плюс всегда можно обратиться к [официальной документации](https://core.telegram.org/bots/api#html-style). Теги бывают открывающие, например `<b>` и парные к ним закрывающие `</b>`. Текст, помещенный между открывающим и парным ему закрывающим тегом, будет как-то отформатирован, если такая пара тегов поддерживается.

На текущий момент поддерживаются следующие HTML-теги:

*   `<b>Жирный текст</b>` или то же самое `<strong>Жирный текст</strong>`
    
    ![](https://ucarecdn.com/14a889c7-a927-47d3-a6e8-d274a05dfca8/-/preview/-/enhance/78/)
    
*   `<i>Наклонный текст</i>` или то же самое `<em>Наклонный текст</em>`
    
    ![](https://ucarecdn.com/0d78fefd-7f80-4c91-8e5e-28179ab63aad/-/preview/-/enhance/78/)
    
*   `<u>Подчеркнутый текст</u>` или то же самое `<ins>Подчеркнутый текст</ins>`
    
    ![](https://ucarecdn.com/7756cd39-8193-475a-9493-1f134b5f8aff/-/preview/-/enhance/79/)
    
*   `<s>Перечеркнутый текст</s>` или то же самое `<strike>Перечеркнутый текст</strike>`, `<del>Перечеркнутый текст</del>`
    
    ![](https://ucarecdn.com/ee2ec454-8996-4e5d-87c0-4fdf5303af49/-/preview/-/enhance/81/)
    
*   `<span class="tg-spoiler">Спойлер</span>` или то же самое `<tg-spoiler>Спойлер</tg-spoiler>`
    
    ![](https://ucarecdn.com/7fb520cc-5b9b-45e1-84ee-c941b366e403/-/preview/-/enhance/78/)
    
*   `<a href="https://stepik.org/120924">Внешняя ссылка</a>`
    
    ![](https://ucarecdn.com/d5fda1f8-7409-4f8a-87b1-ec91230a87d7/-/preview/-/enhance/76/)
    
*   `<a href="tg://user?id=173901673">Внутренняя ссылка</a>`
    
    ![](https://ucarecdn.com/fba02eee-d0c5-43eb-8802-097a8bbb70b7/-/preview/-/enhance/77/)
    
*   `<code>Это моноширинный текст</code>`
    
    ![](https://ucarecdn.com/5e9ed379-73c8-4019-843d-3f9f23798f75/-/preview/-/enhance/80/)
    
*   `<pre>Предварительно отформатированный текст</pre>`
    
    ![](https://ucarecdn.com/9a29d6a9-110d-4f6d-9447-278cb737f2fb/-/preview/-/enhance/76/)
    
*   `<pre><code class="language-python">Предварительно отформатированный блок кода на языке Python</code></pre>`
    
    ![](https://ucarecdn.com/66598673-a009-4613-a013-9ba25bb89595/-/preview/-/enhance/76/)
    

Разница между тегами `<pre>` и `<code>` не совсем очевидна из скриншотов выше. Она лучше заметна, если вставить эти теги внутрь цельного предложения. Тег `<pre>` выделяет текст в отдельный блок, а тег `<code>` остается частью строки, не разрывая ее.

![](https://ucarecdn.com/daff50fd-bbb1-44f4-a916-05dc964e469b/-/preview/-/enhance/78/)

Также можно комбинировать некоторые теги, помещая одни внутрь других. Например:

*   `<b><i>Жирный наклонный текст</i></b>`
    
    ![](https://ucarecdn.com/b386e4bc-c5ab-4dfb-98f5-9b9f0754b6cb/-/preview/-/enhance/81/)
    
*   `<i><u>Наклонный подчеркнутый текст</u></i>`
    
    ![](https://ucarecdn.com/ddd00375-210a-4228-a13b-0e90ae464d86/-/preview/-/enhance/84/)
    
*   `<b><i><u>Жирный наклонный подчеркнутый текст</u></i></b>`
    
    ![](https://ucarecdn.com/782f393b-b022-49b8-b75d-90cb795e753b/-/preview/-/enhance/81/)
    

Если у вас включен `parse_mode='HTML'`  и при этом вам нужно, чтобы в тексте отображались символы "<", ">", "&", то есть, чтобы телеграм не принимал их за часть HTML-разметки, их нужно заменить соответствующими объектами:

*   `<` - заменяется на `&lt;`
*   `>` - заменяется на `&gt;`
*   `&` - заменяется на `&amp;`

Ниже привожу код бота, демонстрирующего как выглядит разметка HTML-тегами. Запустите бота и поэкспериментируйте с ним, чтобы лучше понять какие теги с какими сочетаются, как именно они влияют на текст сообщения и т.п. Попробуйте временно отключить `parse_mode='HTML'`, чтобы посмотреть как бот будет отображать разметку с выключенным режимом форматирования.

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
                     '/strike - зачеркнутый текст\n'
                     '/spoiler - спойлер\n'
                     '/link - внешняя ссылка\n'
                     '/tglink - внутренняя ссылка\n'
                     '/code - моноширинный текст\n'
                     '/pre - предварительно форматированный текст\n'
                     '/precode - предварительно форматированный блок кода\n'
                     '/precodediff - разница между &lt;code&gt; и &lt;pre&gt;\n'
                     '/boldi - жирный наклонный текст\n'
                     '/iu - наклонный подчеркнутый текст\n'
                     '/biu - жирный наклонный подчеркнутый текст')
    
    
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
                     '/strike - зачеркнутый текст\n'
                     '/spoiler - спойлер\n'
                     '/link - внешняя ссылка\n'
                     '/tglink - внутренняя ссылка\n'
                     '/code - моноширинный текст\n'
                     '/pre - предварительно форматированный текст\n'
                     '/precode - предварительно форматированный блок кода\n'
                     '/precodediff - разница между &lt;code&gt; и &lt;pre&gt;\n'
                     '/boldi - жирный наклонный текст\n'
                     '/iu - наклонный подчеркнутый текст\n'
                     '/biu - жирный наклонный подчеркнутый текст')
    
    
    # Этот хэндлер будет срабатывать на команду "/bold"
    @dp.message(Command(commands='bold'))
    async def process_bold_command(message: Message):
        await message.answer(
                text='&lt;b&gt;Это жирный текст&lt;/b&gt;:\n'
                     '<b>Это жирный текст</b>\n\n'
                     '&lt;strong&gt;И это тоже жирный текст&lt;/strong&gt;:\n'
                     '<strong>И это тоже жирный текст</strong>')
    
    
    # Этот хэндлер будет срабатывать на команду "/italic"
    @dp.message(Command(commands='italic'))
    async def process_italic_command(message: Message):
        await message.answer(
                text='&lt;i&gt;Это наклонный текст&lt;/i&gt;:\n'
                     '<i>Это наклонный текст</i>\n\n'
                     '&lt;em&gt;И это тоже наклонный текст&lt;/em&gt;:\n'
                     '<em>И это тоже наклонный текст</em>')
    
    
    # Этот хэндлер будет срабатывать на команду "/underline"
    @dp.message(Command(commands='underline'))
    async def process_underline_command(message: Message):
        await message.answer(
                text='&lt;u&gt;Это подчеркнутый текст&lt;/u&gt;:\n'
                     '<u>Это подчеркнутый текст</u>\n\n'
                     '&lt;ins&gt;И это тоже подчеркнутый текст&lt;/ins&gt;:\n'
                     '<ins>И это тоже подчеркнутый текст</ins>')
    
    
    # Этот хэндлер будет срабатывать на команду "/strike"
    @dp.message(Command(commands='strike'))
    async def process_strike_command(message: Message):
        await message.answer(
                text='&lt;s&gt;Это зачеркнутый текст&lt;/s&gt;:\n'
                     '<s>Это зачеркнутый текст</s>\n\n'
                     '&lt;strike&gt;И это зачеркнутый текст&lt;/strike&gt;:\n'
                     '<strike>И это зачеркнутый текст</strike>\n\n'
                     '&lt;del&gt;И это тоже зачеркнутый текст&lt;/del&gt;:\n'
                     '<del>И это тоже зачеркнутый текст</del>')
    
    
    # Этот хэндлер будет срабатывать на команду "/spoiler"
    @dp.message(Command(commands='spoiler'))
    async def process_spoiler_command(message: Message):
        await message.answer(
                text='&lt;span class="tg-spoiler"&gt;Это текст '
                     'под спойлером&lt;/span&gt;:\n'
                     '<span class="tg-spoiler">Это текст под '
                     'спойлером</span>\n\n'
                     '&lt;tg-spoiler&gt;И это текст под '
                     'спойлером&lt;/tg-spoiler&gt;:\n'
                     '<tg-spoiler>И это текст под спойлером</tg-spoiler>')
    
    
    # Этот хэндлер будет срабатывать на команду "/link"
    @dp.message(Command(commands='link'))
    async def process_link_command(message: Message):
        await message.answer(
                text='&lt;a href="https://stepik.org/120924"&gt;Внешняя '
                     'ссылка&lt;/a&gt;:\n'
                     '<a href="https://stepik.org/120924">Внешняя ссылка</a>')
    
    
    # Этот хэндлер будет срабатывать на команду "/tglink"
    @dp.message(Command(commands='tglink'))
    async def process_tglink_command(message: Message):
        await message.answer(
                text='&lt;a href="tg://user?id=173901673"&gt;Внутренняя '
                     'ссылка&lt;/a&gt;:\n'
                     '<a href="tg://user?id=173901673">Внутренняя ссылка</a>')
    
    
    # Этот хэндлер будет срабатывать на команду "/code"
    @dp.message(Command(commands='code'))
    async def process_code_command(message: Message):
        await message.answer(
                text='&lt;code&gt;Это моноширинный текст&lt;/code&gt;:\n'
                     '<code>Это моноширинный текст</code>')
    
    
    # Этот хэндлер будет срабатывать на команду "/pre"
    @dp.message(Command(commands='pre'))
    async def process_pre_command(message: Message):
        await message.answer(
                text='&lt;pre&gt;Предварительно отформатированный '
                     'текст&lt;/pre&gt;:\n'
                     '<pre>Предварительно отформатированный текст</pre>')
    
    
    # Этот хэндлер будет срабатывать на команду "/precode"
    @dp.message(Command(commands='precode'))
    async def process_precode_command(message: Message):
        await message.answer(
                text='&lt;pre&gt;&lt;code class="language-'
                     'python"&gt;Предварительно отформатированный '
                     'блок кода на языке Python&lt;/code&gt;&lt;/pre&gt;:\n'
                     '<pre><code class="language-python">Предварительно '
                     'отформатированный блок кода на языке Python</code></pre>')
    
    
    # Этот хэндлер будет срабатывать на команду "/precodediff"
    @dp.message(Command(commands='precodediff'))
    async def process_precodediff_command(message: Message):
        await message.answer(
                text='С помощью этого текста можно лучше понять '
                     'разницу между тегами &lt;code&gt; и '
                     '&lt;pre&gt; - текст внутри '
                     'тегов &lt;code&gt; <code>не выделяется в '
                     'отдельный блок</code>, а становится '
                     'частью строки, внутрь которой помещен, в то время как '
                     'тег &lt;pre&gt; выделяет текст <pre>в отдельный '
                     'блок,</pre> разрывая '
                     'строку, внутрь которой помещен')
    
    
    # Этот хэндлер будет срабатывать на команду "/boldi"
    @dp.message(Command(commands='boldi'))
    async def process_boldi_command(message: Message):
        await message.answer(
                text='&lt;b&gt;&lt;i&gt;Это жирный наклонный '
                     'текст&lt;/i&gt;&lt;/b&gt;:\n\n'
                     '<b><i>Это жирный наклонный текст</i></b>')
    
    
    # Этот хэндлер будет срабатывать на команду "/iu"
    @dp.message(Command(commands='iu'))
    async def process_iu_command(message: Message):
        await message.answer(
                text='&lt;i&gt;&lt;u&gt;Это наклонный подчеркнутый '
                     'текст&lt;/u&gt;&lt;/i&gt;:\n\n'
                     '<i><u>Это наклонный подчеркнутый текст</u></i>')
    
    
    # Этот хэндлер будет срабатывать на команду "/biu"
    @dp.message(Command(commands='biu'))
    async def process_biu_command(message: Message):
        await message.answer(
                text='&lt;b&gt;&lt;i&gt;&lt;u&gt;Это жирный '
                     'наклонный подчеркнутый '
                     'текст&lt;/u&gt;&lt;/i&gt;&lt;/b&gt;:\n\n'
                     '<b><i><u>Это жирный наклонный подчеркнутый '
                     'текст</u></i></b>')
    
    
    # Этот хэндлер будет срабатывать на любые сообщения, кроме команд,
    # отлавливаемых хэндлерами выше
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