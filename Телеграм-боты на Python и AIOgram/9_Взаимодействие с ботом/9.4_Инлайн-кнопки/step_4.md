## Нотификации и алерты
--------------------

На предыдущем шаге мы сообщали телеграму о том, что приняли и обработали callback, с помощью инструкции `callback.answer()`. Но у метода `answer` могут быть дополнительные параметры:

*   `text` - отвечает за текст всплывающего на пару секунд окна нотификации или алерта (до 200 символов)
*   `show_alert` - отвечает за превращение всплывающего и самостоятельно исчезающего окошка нотификации в алерт, требующий закрытия, если установить равным `True`. По умолчанию - `False`.
*   `url` - ссылка, которая будет открыта клиентом пользователя (поддерживаются не любые ссылки, а только специфические)
*   `cache_time` - отвечает за максимальное время (в секундах) кэширования результата запроса обратного вызова клиентом пользователя.

Из документации к Telegram Bot API:

![](https://ucarecdn.com/e7ccb1eb-5027-4214-900c-923357909c69/-/preview/-/enhance/71/)

Пункты `url` и `cache_time`, думаю, не очень понятны, но они нам пока и не нужны, не будем забивать голову. В контексте этого урока, нас интересуют `text` и `show_alert`.

Сначала давайте посмотрим как ведет себя просто добавление текста, без указания параметра `show_alert`. Возьмем код бота из предыдущего урока и добавим, в обработчиках нажатия на инлайн-кнопки, параметр `text` методу `answer`.

    from aiogram import Bot, Dispatcher
    from aiogram.filters import CommandStart, Text
    from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                               InlineKeyboardMarkup, Message)
    
    # Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
    # полученный у @BotFather
    API_TOKEN: str = 'BOT TOKEN HERE'
    
    # Создаем объекты бота и диспетчера
    bot: Bot = Bot(token=API_TOKEN)
    dp: Dispatcher = Dispatcher()
    
    # Создаем объекты инлайн-кнопок
    big_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text='БОЛЬШАЯ КНОПКА 1',
        callback_data='big_button_1_pressed')
    
    big_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text='БОЛЬШАЯ КНОПКА 2',
        callback_data='big_button_2_pressed')
    
    # Создаем объект инлайн-клавиатуры
    keyboard: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[big_button_1],
                         [big_button_2]])
    
    
    # Этот хэндлер будет срабатывать на команду "/start"
    # и отправлять в чат клавиатуру с инлайн-кнопками
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text='Это инлайн-кнопки. Нажми на любую!',
                             reply_markup=keyboard)
    
    
    # Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
    # с data 'big_button_1_pressed'
    @dp.callback_query(Text(text=['big_button_1_pressed']))
    async def process_button_1_press(callback: CallbackQuery):
        if callback.message.text != 'Была нажата БОЛЬШАЯ КНОПКА 1':
            await callback.message.edit_text(
                text='Была нажата БОЛЬШАЯ КНОПКА 1',
                reply_markup=callback.message.reply_markup)
        await callback.answer(text='Ура! Нажата кнопка 1')
    
    
    # Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
    # с data 'big_button_2_pressed'
    @dp.callback_query(Text(text=['big_button_2_pressed']))
    async def process_button_2_press(callback: CallbackQuery):
        if callback.message.text != 'Была нажата БОЛЬШАЯ КНОПКА 2':
            await callback.message.edit_text(
                text='Была нажата БОЛЬШАЯ КНОПКА 2',
                reply_markup=callback.message.reply_markup)
        await callback.answer(text='Ура! Нажата кнопка 2')
    
    
    if __name__ == '__main__':
        dp.run_polling(bot)

Будем внутри всплывающего окна нотификации отображать текст о том, какая кнопка нажата.

    await callback.answer(text='Ура! Нажата кнопка 1')

Запустим бота и проверим как это работает.

![](https://ucarecdn.com/e54cd08f-42a8-4825-894d-1eea41aab16c/)

Окошко с текстом из параметра `text` метода `answer` появляется на пару секунд и затем исчезает. Бывает удобно через такую нотификацию уведомлять пользователя, что какое-то действие, связанное с нажатием инлайн-кнопки, выполнено, не меняя при этом само сообщение с кнопкой.

А теперь давайте добавим хэндлеру, срабатывающему на нажатие первой кнопки, параметр `show_alert` и сделаем его равным  `True`.

    # ...
    
    # Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
    # с data 'big_button_1_pressed'
    @dp.callback_query(Text(text=['big_button_1_pressed']))
    async def process_button_1_press(callback: CallbackQuery):
        if callback.message.text != 'Была нажата БОЛЬШАЯ КНОПКА 1':
            await callback.message.edit_text(
                text='Была нажата БОЛЬШАЯ КНОПКА 1',
                reply_markup=callback.message.reply_markup)
        await callback.answer(text='Ура! Нажата кнопка 1',
                              show_alert=True)
    
    # ...

Запустим бота.

![](https://ucarecdn.com/dee95f6e-95db-4510-b961-dab100ae3b8c/)

Теперь вместо всплывающего и самостоятельно исчезающего окошка с нотификацией, появился алерт, требующий нажатия на кнопку "OK", чтобы быть убранным. Это бывает полезно, когда нужно обязательно привлечь внимание пользователя, чтобы без подтверждения он не мог дальше взаимодействовать с ботом.