## URL-кнопки
----------

URL-кнопки - это такие инлайн-кнопки, нажатие на которые переводит нас в браузер по ссылке, связанной с этой кнопкой, или на какой-то внутренний ресурс самого Телеграм (канал, группу и т.п.) тоже по ссылке. За них отвечает атрибут `url` класса `InlineKeyboardButton`. Давайте посмотрим, как такие кнопки работают.

Напишем простенького бота с одним хэндлером, срабатывающим на команду /start, и отправляющим в чат сообщение с инлайн-клавиатурой с url-кнопками.

    from aiogram import Bot, Dispatcher
    from aiogram.filters import CommandStart
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
    
    # Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
    # полученный у @BotFather
    API_TOKEN: str = 'BOT TOKEN HERE'
    
    # Создаем объекты бота и диспетчера
    bot: Bot = Bot(token=API_TOKEN)
    dp: Dispatcher = Dispatcher()
    
    # Создаем объекты инлайн-кнопок
    url_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='Курс "Телеграм-боты на Python и AIOgram"',
        url='https://stepik.org/120924')
    url_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='Документация Telegram Bot API',
        url='https://core.telegram.org/bots/api')
    
    # Создаем объект инлайн-клавиатуры
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[url_button_1],
                         [url_button_2]])
    
    
    # Этот хэндлер будет срабатывать на команду "/start"
    # и отправлять в чат клавиатуру c url-кнопками
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text='Это инлайн-кнопки с параметром "url"',
                             reply_markup=keyboard)
    
    
    if __name__ == '__main__':
        dp.run_polling(bot)

Если запустить такого бота и отправить ему команду /start, увидим сообщение с прикрепленными к нему инлайн-кнопками:

![](https://ucarecdn.com/d47950df-d5ae-4d1d-9704-9a3d1e62c9bf/-/preview/-/enhance/77/)

Нажатие на одну из таких кнопок приводит к появлению окна подтверждения и затем, в случае согласия, происходит переход во внешний браузер по ссылке, скрывающейся за инлайн-кнопкой.

![](https://ucarecdn.com/c004eb05-065d-4c3c-9e6d-06617ad0e033/-/preview/-/enhance/80/)

Впрочем, некоторые ссылки, принадлежащие Telegram, открываются без подтверждающего окна.

В качестве параметра в `url` могут быть указаны не только ссылки `http://` и `https://`, но и `tg://`. Последние открываются в самом приложении Telegram, также как и ссылки вида `https://t.me/`. По сути, ссылки `tg://` и `https://t.me/` делают одно и то же чуть разными способами - открывают внутренний телеграм-ресурс прямо в приложении телеграм. Только `tg://` - это специальный протокол самого телеграм, позволяющий открывать ссылки, даже если домен `t.me` заблокирован, как это было несколько лет назад.

    # ...
    
    # Создаем объекты инлайн-кнопок
    group_name = 'aiogram_stepik_course'
    url_button_1: InlineKeyboardButton = InlineKeyboardButton(
                                        text='Группа "Телеграм-боты на AIOgram"',
                                        url=f'tg://resolve?domain={group_name}')
    user_id = 173901673
    url_button_2: InlineKeyboardButton = InlineKeyboardButton(
                                        text='Автор курса на Степике по телеграм-ботам',
                                        url=f'tg://user?id={user_id}')
    
    channel_name = 'toBeAnMLspecialist'
    url_button_3: InlineKeyboardButton = InlineKeyboardButton(
                                        text='Канал "Стать специалистом по машинному обучению"',
                                        url=f'https://t.me/{channel_name}')
                                        
    # Создаем объект инлайн-клавиатуры
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[url_button_1],
                         [url_button_2],
                         [url_button_3]])
    
    # ...

Вот так это будет выглядеть:

![](https://ucarecdn.com/863e72c6-8383-4b96-ba23-4554459a4ad8/-/preview/-/enhance/71/)

Нажатие на такие кнопки не переводит в браузер, а приводит к переходу в группу, канал и т.п. в самом приложении Telegram.

![](https://ucarecdn.com/a87550b5-625c-455d-928e-b58885bfce42/)

**Примечание.** Нажатие на инлайн-кнопки с параметром `url` не генерирует никаких апдейтов, которые можно было бы обработать.