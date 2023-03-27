## Эксперименты с редактированием сообщений
----------------------------------------

Надеюсь, вам удалось обзавестись id разного типа контента, чтобы мы вместе могли продолжить экспериментировать с редактированием сообщений разных типов. Если возникли сложности - напишите либо в комментариях к уроку, либо в [группе курса](https://t.me/aiogram_stepik_course) в телеграм - кто-нибудь вам обязательно поможет.

Для работы с примерами ниже, будем использовать одного и того же бота, только при этом будем немного видоизменять хэндлеры.

    from aiogram import Bot, Dispatcher
    from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                               InlineKeyboardMarkup, InputMediaAudio,
                               InputMediaDocument, InputMediaPhoto,
                               InputMediaVideo, Message)
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from aiogram.filters import CommandStart, Text
    from aiogram.exceptions import TelegramBadRequest
    
    # Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
    # полученный у @BotFather
    # BOT_TOKEN = 'BOT TOKEN HERE'
    BOT_TOKEN = '5424991242:AAFbT6ckF2HYKPDyLWLFvx5C2jV71TsG9vQ'
    
    bot: Bot = Bot(BOT_TOKEN)
    dp: Dispatcher = Dispatcher()
    
    
    LEXICON: dict[str, str] = {
        'audio': '🎶 Аудио',
        'text': '📃 Текст',
        'photo': '🖼 Фото',
        'video': '🎬 Видео',
        'document': '📑 Документ',
        'voice': '📢 Голосовое сообщение',
        'text_1': 'Это обыкновенное текстовое сообщение, его можно легко отредактировать другим текстовым сообщением, но нельзя отредактировать сообщением с медиа.',
        'text_2': 'Это тоже обыкновенное текстовое сообщение, которое можно заменить на другое текстовое сообщение через редактирование.',
        'photo_id1': 'AgACAgIAAxkBAAIU5WPJSt9TUFzUwbCqewIUNtp9gJBYAAIJxTEbp5JJSvDAdS74pTGAAQADAgADcwADLQQ',
        'photo_id2': 'AgACAgIAAxkBAAIU_WPJgB1KZiyEIu4OikbsEsJInzV-AALxxTEbp5JJSnu2IKkQdDDQAQADAgADcwADLQQ',
        'voice_id1': 'AwACAgIAAxkBAAIU52PJSwWbxtBrhoL8o3njUdvNaHckAALZJwACp5JJStGYVdp4u5cILQQ',
        'voice_id2': 'AwACAgIAAxkBAAIU9mPJfLxFoKpSTie3CZFL3PcFfTHhAAKWKQACp5JJSqoWOXKpDRntLQQ',
        'audio_id1': 'CQACAgIAAxkBAAIVRWPKsPl83xynqlF9YvF5MRyF9GxeAAL1JAACkhBZSmyFCDY61yX8LQQ',
        'audio_id2': 'CQACAgIAAxkBAAIVR2PKsXppkdhAnOlqwpOHDJivtfvJAAL4JAACkhBZSoMVyPSB59h5LQQ',
        'document_id1': 'BQACAgIAAxkBAAIVEmPKY_5RcBfEMeQ55X02PNimd1FdAAJ1IwACkhBRSmszrVZWfOY6LQQ',
        'document_id2': 'BQACAgIAAxkBAAIVFGPKZCYnp07PHr_OwXIKo5Z8fxcEAAJ3IwACkhBRSoZiZmUOrb4nLQQ',
        'video_id1': 'BAACAgIAAxkBAAIVFmPKZL_cgfokLm3pBU5w3zspn3-lAAJ5IwACkhBRSs4Lk37jVF8xLQQ',
        'video_id2': 'BAACAgIAAxkBAAIVGGPKZTURYRphKtnnVFHy8Oa6OxPXAAJ6IwACkhBRSnfUGQW2UKeBLQQ',
        }
    
    
    # Функция для генерации клавиатур с инлайн-кнопками
    def get_markup(width: int, *args, **kwargs) -> InlineKeyboardMarkup:
        # Инициализируем билдер
        kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        # Инициализируем список для кнопок
        buttons: list[InlineKeyboardButton] = []
        # Заполняем список кнопками из аргументов args и kwargs
        if args:
            for button in args:
                buttons.append(InlineKeyboardButton(
                    text=LEXICON[button] if button in LEXICON else button,
                    callback_data=button))
        if kwargs:
            for button, text in kwargs.items():
                buttons.append(InlineKeyboardButton(
                    text=text,
                    callback_data=button))
        # Распаковываем список с кнопками в билдер методом row c параметром width
        kb_builder.row(*buttons, width=width)
        # Возвращаем объект инлайн-клавиатуры
        return kb_builder.as_markup()
    
    
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        pass
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    @dp.callback_query(Text(text=['text',
                                  'audio',
                                  'video',
                                  'document',
                                  'photo',
                                  'voice']))
    async def process_button_press(callback: CallbackQuery):
        pass
    
    
    # Этот хэндлер будет срабатывать на все остальные сообщения
    @dp.message()
    async def send_echo(message: Message):
        print(message)
        await message.answer(
                text='Не понимаю')
    
    
    if __name__ == '__main__':
        dp.run_polling(bot)

При отправке команды /start, бот будет отправлять в чат сообщение того типа, с которым мы хотим провести эксперимент с прикрепленной к нему инлайн-кнопкой. При нажатии на эту кнопку будем пытаться отредактировать это сообщение. Поехали!

### 1\. Меняем текст на текст

Мы с вами уже знаем, что так можно. Мы этим неоднократно пользовались. Но для полноты картины оставлю пример и здесь тоже. Хэндлеры, обрабатывающие команду /start и нажатие на инлайн-кнопку, будут следующими: 

    # ...
    
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        markup = get_markup(2, 'text')
        await message.answer(
                        text=LEXICON['text_1'],
                        reply_markup=markup)
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    @dp.callback_query(Text(text=['text',
                                  'audio',
                                  'video',
                                  'document',
                                  'photo',
                                  'voice']))
    async def process_button_press(callback: CallbackQuery):
        markup = get_markup(2, 'text')
        if callback.message.text == LEXICON['text_1']:
            text = LEXICON['text_2']
        else:
            text = LEXICON['text_1']
        await callback.message.edit_text(
                                text=text,
                                reply_markup=markup)
    
    # ...

И, соответственно, результат:

![](https://ucarecdn.com/792212e6-7a74-470f-aa99-34b612e4e336/)

Вот, мы в очередной раз убедились, что текстовые сообщения прекрасно редактируются. Продолжаем эксперимент.

### 2\. Меняем текст на медиа

Теперь пример немного посложнее. Давайте попробуем поменять текстовое сообщение на фото с помощью метода `edit_message_media` у объекта типа `Bot`. В этом пункте просто выполним код без особых пояснений, а в следующем я подробно расскажу про то, как `edit_message_media` работает. Изменим код хэндлеров:

    # ...
    
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        markup = get_markup(2, 'photo')
        await message.answer(
                        text=LEXICON['text_1'],
                        reply_markup=markup)
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    @dp.callback_query(Text(text=['text',
                                  'audio',
                                  'video',
                                  'document',
                                  'photo',
                                  'voice']))
    async def process_button_press(callback: CallbackQuery, bot: Bot):
        markup = get_markup(2, 'photo')
        await bot.edit_message_media(
                            chat_id=callback.message.chat.id,
                            message_id=callback.message.message_id,
                            media=InputMediaPhoto(
                                    media=LEXICON['photo_id1'],
                                    caption='Это фото 1'),
                            reply_markup=markup)
    
    # ...

Запускаем бота и проверяем.

![](https://ucarecdn.com/5b4631ec-fed7-41c9-926b-be19775634fb/)

Не работает :( И в терминале видим ошибку:

    aiogram.exceptions.TelegramBadRequest: Telegram server says Bad Request: there is no media in the message to edit

То есть, в апдейте нет медиа, которое мы смогли бы отредактировать. То же самое получим, если будем пытаться менять текстовое сообщение на любой другой тип медиа-контента. Можете поэкспериментировать и увидеть это сами.

### 3\. Меняем фото на фото

А теперь убедимся, что фото прекрасно редактируется, если тип контента нового сообщения тоже фото. Заодно разберем еще один неочевидный нюанс касательно хранения контента телеграмом. Сначала код хэндлеров.

    # ...
    
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        markup = get_markup(2, 'photo')
        await message.answer_photo(
                            photo=LEXICON['photo_id1'],
                            caption='Это фото 1',
                            reply_markup=markup)
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    @dp.callback_query(Text(text=['text',
                                  'audio',
                                  'video',
                                  'document',
                                  'photo',
                                  'voice']))
    async def process_button_press(callback: CallbackQuery, bot: Bot):
        markup = get_markup(2, 'photo')
        try:
            await bot.edit_message_media(
                                chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                media=InputMediaPhoto(
                                        media=LEXICON['photo_id2'],
                                        caption='Это фото 2'),
                                reply_markup=markup)
        except TelegramBadRequest:
            await bot.edit_message_media(
                                chat_id=callback.message.chat.id,
                                message_id=callback.message.message_id,
                                media=InputMediaPhoto(
                                        media=LEXICON['photo_id1'],
                                        caption='Это фото 1'),
                                reply_markup=markup)
    
    # ...

И результат:

![](https://ucarecdn.com/bc3e1f95-6c66-4f8c-ab24-b1549cc9ee76/)

Во-первых, мы убедились, что все работает и сообщение с фото отлично редактируется через метод `edit_message_media` у объекта типа Bot, если взамен старого фото отправлять новое. Во-вторых, ранее, для редактирования текстового сообщения, мы использовали метод `edit_text`. Похожего метода, который мог бы называться по аналогии `edit_photo`, в Telegram Bot API не предусмотрено, поэтому и `edit_message_media`, где в качестве параметра передается экземпляр класса соответствующего типу медиа. Доступные типы есть в [разделе документации](https://core.telegram.org/bots/api#inputmedia), посвященному типу `InputMedia`.

![](https://ucarecdn.com/bfeccacb-a9bf-4e4e-97c6-92e47a7d1b88/-/preview/-/enhance/81/)

Для фото мы как раз использовали `InputMediaPhoto`, создав экземпляр этого класса и, передав его в качестве параметра.

![](https://ucarecdn.com/ca639e38-f18f-4b0d-905f-58064cfba106/-/preview/-/enhance/76/)

В-третьих, некоторые пояснения к самой логике работы кода.

Когда мы редактировали текст в первом примере этого шага - мы просто сравнивали на полное совпадение старый и новый текст, чтобы избежать исключения `TelegramBadRequest`, потому что, как мы уже неоднократно убеждались, такое исключение возникает, когда новое сообщение полностью повторяет старое. Телеграм понимает, что менять нечего и соответствующим образом отвечает на запрос от `aiogram`. Почему же в примере с фото мы просто не проверяем на соответствие id старого фото новому? Если не совпадают - берем одно фото, если совпадают - берем другое. Почему не так? Дело в том, что `file_id` меняется с каждым новым апдейтом. То есть, мы отправляем фото в чат по одному `file_id`, а апдейт приходит уже с другим `file_id`. Я уже где-то говорил, что `file_id` зависит от чата, в котором такой файл был получен, но еще он зависит от времени отправки. Ну, вот, так это устроено.

А как тогда различать фото между собой, если у них все время разный `file_id`? Если посмотреть на апдейт с фото, да и на самом деле, на любой апдейт с медиа, можно увидеть, что у апдейта есть не только поле `file_id`, но и `file_unique_id`. Вот по этому уникальному id медиа-объекты и различаются в Telegram, потому что он остается неизменным при пересылках объекта.

    {
      "message_id": 5422,
      "from": {
        "id": 173901673,
        "is_bot": false,
        "first_name": "Mikhail",
        "last_name": "Kryzhanovskiy",
        "username": "kmsint",
        "language_code": "ru"
      },
      "chat": {
        "id": 173901673,
        "first_name": "Mikhail",
        "last_name": "Kryzhanovskiy",
        "username": "kmsint",
        "type": "private"
      },
      "date": 1674216860,
      "photo": [
        {
          "file_id": "AgACAgIAAxkBAAIVLmPKhZw0ixJcJTmIKTHlYlSk_hITAAJawzEbkhBZSmPcWTtlTwfkAQADAgADcwADLQQ",
          "file_unique_id": "AQADWsMxG5IQWUp4",
          "file_size": 1924,
          "width": 90,
          "height": 90
        },
        {
          "file_id": "AgACAgIAAxkBAAIVLmPKhZw0ixJcJTmIKTHlYlSk_hITAAJawzEbkhBZSmPcWTtlTwfkAQADAgADbQADLQQ",
          "file_unique_id": "AQADWsMxG5IQWUpy",
          "file_size": 18642,
          "width": 320,
          "height": 320
        },
        {
          "file_id": "AgACAgIAAxkBAAIVLmPKhZw0ixJcJTmIKTHlYlSk_hITAAJawzEbkhBZSmPcWTtlTwfkAQADAgADeAADLQQ",
          "file_unique_id": "AQADWsMxG5IQWUp9",
          "file_size": 32304,
          "width": 512,
          "height": 512
        }
      ]
    }

Но, позвольте! Почему же тогда мы, в качестве параметра `media`, указываем `file_id`, а не `file_unique_id`? Ведь тогда можно будет избежать того, что телеграм меняет `file_id`. К сожалению, нет. Указав `media=file_unique_id` мы получим ошибку. Это, увы, не работает. Отправить объект еще раз из уже отправленных нами ранее, можно только указав его `file_id`. А, вот, отличить объекты друг от друга можно по `file_unique_id`. Такие дела. Учитывайте это, когда будете сохранять от пользователей какие-нибудь медиа-объекты, а потом с ними как-то работать в дальнейшем. Сохраняйте для них оба параметра. Теперь, надеюсь, понятно для чего.

Ну, а мы с вами не сохраняли `file_unique_id` объектов на предыдущем шаге, поэтому теперь нам приходится отлавливать исключение `TelegramBadRequest`. Для нашей учебной задачи это вполне допустимо.

Продолжаем эксперименты.

### 4\. Меняем документ на документ

Переписываем хэндлеры:

    # ...
    
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        markup = get_markup(2, 'document')
        await message.answer_document(
                            document=LEXICON['document_id1'],
                            caption='Это документ 1',
                            reply_markup=markup)
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    @dp.callback_query(Text(text=['text',
                                  'audio',
                                  'video',
                                  'document',
                                  'photo',
                                  'voice']))
    async def process_button_press(callback: CallbackQuery, bot: Bot):
        markup = get_markup(2, 'document')
        try:
            await bot.edit_message_media(
                            chat_id=callback.message.chat.id,
                            message_id=callback.message.message_id,
                            media=InputMediaDocument(
                                    media=LEXICON['document_id2'],
                                    caption='Это документ 2'),
                            reply_markup=markup)
        except TelegramBadRequest:
            await bot.edit_message_media(
                            chat_id=callback.message.chat.id,
                            message_id=callback.message.message_id,
                            media=InputMediaDocument(
                                    media=LEXICON['document_id1'],
                                    caption='Это документ 1'),
                            reply_markup=markup)
    
    # ...

Запускаем бота и получаем результат.

![](https://ucarecdn.com/9be9faed-f130-42a2-9abb-14568772a301/)

Сообщение с документом также прекрасно редактируется. Скриншот из [документации](https://core.telegram.org/bots/api#inputmediadocument), посвященный типу `InputMediaDocument`:

![](https://ucarecdn.com/01a73e87-aae3-4cf3-9d5a-ed2c90a99ede/-/preview/-/enhance/78/)

### 5\. Меняем видео на видео

С видео попробуйте самостоятельно. Здесь приведу только результат, код отредактируйте сами по аналогии.

![](https://ucarecdn.com/43241774-44f0-46b1-bcaa-ac670b058ab3/)

Как видно, сообщения с видео тоже прекрасно редактируются.

### 6\. Меняем аудио на аудио

Тут все как с видео, фото или документами. Аудиофайлы меняются один на другой, через редактирование сообщения, без проблем.

    # ...
    
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        markup = get_markup(2, 'audio')
        await message.answer_audio(
                            audio=LEXICON['audio_id1'],
                            caption='Это аудио 1',
                            reply_markup=markup)
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    @dp.callback_query(Text(text=['text',
                                  'audio',
                                  'video',
                                  'document',
                                  'photo',
                                  'voice']))
    async def process_button_press(callback: CallbackQuery):
        markup = get_markup(2, 'audio')
        try:
            await bot.edit_message_media(
                            chat_id=callback.message.chat.id,
                            message_id=callback.message.message_id,
                            media=InputMediaAudio(
                                    media=LEXICON['audio_id2'],
                                    caption='Это аудио 2'),
                            reply_markup=markup)
        except TelegramBadRequest:
            await bot.edit_message_media(
                            chat_id=callback.message.chat.id,
                            message_id=callback.message.message_id,
                            media=InputMediaAudio(
                                    media=LEXICON['audio_id1'],
                                    caption='Это аудио 1'),
                            reply_markup=markup)
    
    # ...

Результат ожидаемый.

![](https://ucarecdn.com/ce3274c4-baef-48cf-bd7d-6927c466984d/)

### 7\. Меняем один тип медиа на другой

То, что текстовое сообщение нельзя отредактировать сообщением с медиа мы уже поняли. То, что сообщения с одним типом медиа легко редактируются, мы уже тоже поняли. А можно ли поменять один тип медиа на другой? Например, фото на видео. Или видео на аудио. Попробуем! Код приводить не буду, покажу только результат. Если захотите воспроизвести, думаю, не составит труда написать самим по аналогии.

**Аудио на видео**

![](https://ucarecdn.com/6dcffdce-758c-42db-a5ad-2614957cb5a8/)

**Аудио на документ**

![](https://ucarecdn.com/5a3b7892-241d-4000-b773-e59d092f4742/)

**Видео на фото**

![](https://ucarecdn.com/a61cee5f-2729-481e-b4c9-ace98a9a5a1a/)

Ну, думаю, не сложно догадаться, что в рамках медиа можно редактировать сообщение с одним типом медиа на другой без всяких ограничений. И на мой взгляд, это довольно удобно.