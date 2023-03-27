## Редактирование других типов сообщений
-------------------------------------

Давайте попробуем отредактировать, например, голосовое сообщение...

А, вот, здесь нас с вами ждет сюрприз :) Казалось бы, ну чем аудио голосовых сообщений отличается от аудиофайлов? По каким признакам мы должны понять, что голосовое сообщение не отредактировать? А, вот, не редактируется. Точнее, не так. Строго говоря, сообщение можно отредактировать. Можно заменить описание к голосовому сообщению или заменить клавиатуру (методы `edit_message_caption` и `edit_message_reply_markup`). А, вот, заменить само голосовое сообщение, как мы это делали с аудиофайлами, фото, видео или документами - не получится. Давайте убедимся на практике.

    # ...
    
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        markup = get_markup(2, 'voice')
        await message.answer_audio(
                            audio=LEXICON['voice_id1'],
                            caption='Это голосовое сообщение 1',
                            reply_markup=markup)
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    @dp.callback_query(Text(text=['text',
                                  'audio',
                                  'video',
                                  'document',
                                  'photo',
                                  'voice']))
    async def process_button_press(callback: CallbackQuery, bot: Bot):
        markup = get_markup(2, 'voice')
        try:
            await bot.edit_message_media(
                            chat_id=callback.message.chat.id,
                            message_id=callback.message.message_id,
                            media=InputMediaAudio(
                                    media=LEXICON['voice_id2'],
                                    caption='Это голосове сообщение 2'),
                            reply_markup=markup)
        except TelegramBadRequest:
            await bot.edit_message_media(
                            chat_id=callback.message.chat.id,
                            message_id=callback.message.message_id,
                            media=InputMediaAudio(
                                    media=LEXICON['voice_id1'],
                                    caption='Это голосове сообщение 1'),
                            reply_markup=markup)
    
    # ...

Результат:

![](https://ucarecdn.com/b2c0f8a4-c594-443c-ae2a-29c6ce3e5868/)

Не работает. Согласен, немного странная история, особенно если учесть, что для отправки голосового сообщения работают методы `answer_audio`, а также `send_audio`, хотя есть `answer_voice` и `send_voice`, но, вот, видимо, нужно принять это как данность и с этим жить :) Типы медиа разные и метод `edit_message_media` не поддерживает `Voice`, равно как и `VideoNote`, `Sticker` и так далее.