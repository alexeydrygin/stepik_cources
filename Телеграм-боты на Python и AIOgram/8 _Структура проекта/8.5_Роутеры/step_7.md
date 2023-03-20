## Модуль other\_handlers.py
-------------------------

Данный модуль состоит всего из одного хэндлера, который будет отправлять пользователю его же сообщение, если только это не команды /start или /help - их мы будем обрабатывать отдельными хэндлерами, которые рассмотрели на предыдущем шаге.

### other\_handlers.py

    from aiogram.types import Message
    
    from lexicon.lexicon import LEXICON_RU
    
    
    # Этот хэндлер будет срабатывать на любые ваши сообщения,
    # кроме команд "/start" и "/help"
    @dp.message()
    async def send_echo(message: Message):
        try:
            await message.send_copy(chat_id=message.chat.id)
        except TypeError:
            await message.reply(text=LEXICON_RU['no_echo'])

И снова IDE подчеркивает `dp`

![](https://ucarecdn.com/12e7dddc-1396-4c57-bb3d-c41fb37301af/-/preview/-/enhance/77/)

Остался последний модуль и начнем разбираться.