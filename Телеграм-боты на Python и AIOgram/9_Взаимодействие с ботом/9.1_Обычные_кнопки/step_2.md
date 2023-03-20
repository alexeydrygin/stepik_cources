## Обычные кнопки
--------------

Как уже было сказано ранее, обычные кнопки чаще всего используются как шаблоны текстовых ответов, но есть еще и специальные обычные кнопки. Их мы рассмотрим в одном из следующих шагов, а сейчас давайте разберемся с тем как создавать кнопки-шаблоны и как обрабатывать нажатия на них.

Для работы с обычными кнопками из `aiogram.types` понадобятся следующие классы:

*   `ReplyKeyboardMarkup` - для создания объекта клавиатуры ([ссылка](https://core.telegram.org/bots/api#replykeyboardmarkup) на документацию Telegram Bot API)
*   `KeyboardButton` - для создания кнопок клавиатуры ([ссылка](https://core.telegram.org/bots/api#keyboardbutton) на документацию Telegram Bot API)
*   `ReplyKeyboardRemove` - для удаления клавиатуры ([ссылка](https://core.telegram.org/bots/api#replykeyboardremove) на документацию Telegram Bot API)

Это репрезентация одноименных типов из Telegram Bot API.

### ReplyKeyboardMarkup

![](https://ucarecdn.com/e37b700a-48a3-4a73-80ad-b59ae65a6e34/-/preview/-/enhance/80/)

### KeyboardButton

![](https://ucarecdn.com/0320619b-4dee-4746-ac37-489a8d1d2ca2/-/preview/-/enhance/81/)

### ReplyKeyboardRemove

![](https://ucarecdn.com/c12eff99-972e-4187-93cc-1e4f12afedce/-/preview/-/enhance/81/)

Соответственно, те атрибуты, которые есть у типов Telegram Bot API есть и у соответствующих классов `aiogram`. Плюс для удобства в классы добавлены еще дополнительные методы.

Если посмотреть на описание того, что такое параметр `keyboard` у `ReplyKeyboardMarkup` - становится понятно, что клавиатура - это массив массивов из объектов `KeyboardButton`. Каждый такой массив внутри основного массива - это, в конечном итоге, ряд кнопок. То есть клавиатуры можно строить по довольно простому принципу:

1.  Создаем объекты кнопок клавиатуры
2.  Создаем объект клавиатуры
3.  Добавляем массивы нужной конфигурации с кнопками в основной массив клавиатуры

Далее останется только в нужном хэндлере отправить созданную клавиатуру пользователю. Ну, а если клавиатура больше не нужна - можно ее удалить. Например, хэндлером, который срабатывает на нажатие кнопки на клавиатуре. То есть, если бот отправляет вопрос и варианты ответа на кнопках, то после нажатия на один из ответов, клавиатура может стать больше не нужной и лучше ее удалить, чтобы она не занимала место на экране.

Для примера давайте напишем простого бота, который будет задавать пользователю вопрос и присылать клавиатуру с вариантами ответов, а после нажатия на одну из кнопок с ответами, удалять ее.

Мы уже с вами рассмотрели более продвинутый шаблон для бота, чем весь код в одном файле, но чтобы не усложнять текущую демонстрацию, пока все же останемся в рамках одного файла. А изученный шаблон применим, когда будем писать бота посложнее в следующих уроках. Итак, код:

    from aiogram import Bot, Dispatcher
    from aiogram.filters import CommandStart, Text
    from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                               ReplyKeyboardRemove)
    
    # Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
    # полученный у @BotFather
    API_TOKEN: str = 'BOT TOKEN HERE'
    
    # Создаем объекты бота и диспетчера
    bot: Bot = Bot(token=API_TOKEN)
    dp: Dispatcher = Dispatcher()
    
    # Создаем объекты кнопок
    button_1: KeyboardButton = KeyboardButton(text='Собак 🦮')
    button_2: KeyboardButton = KeyboardButton(text='Огурцов 🥒')
    
    # Создаем объект клавиатуры, добавляя в него кнопки
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                        keyboard=[[button_1, button_2]])
    
    
    # Этот хэндлер будет срабатывать на команду "/start"
    # и отправлять в чат клавиатуру
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text='Чего кошки боятся больше?',
                             reply_markup=keyboard)
    
    
    # Этот хэндлер будет срабатывать на ответ "Собак 🦮" и удалять клавиатуру
    @dp.message(Text(text='Собак 🦮'))
    async def process_dog_answer(message: Message):
        await message.answer(text='Да, несомненно, кошки боятся собак. '
                                  'Но вы видели как они боятся огурцов?',
                             reply_markup=ReplyKeyboardRemove())
    
    
    # Этот хэндлер будет срабатывать на ответ "Огурцов 🥒" и удалять клавиатуру
    @dp.message(Text(text='Огурцов 🥒'))
    async def process_cucumber_answer(message: Message):
        await message.answer(text='Да, иногда кажется, что огурцов '
                                  'кошки боятся больше',
                             reply_markup=ReplyKeyboardRemove())
    
    
    if __name__ == '__main__':
        dp.run_polling(bot)

Результат можно увидеть на скриншоте:

![](https://ucarecdn.com/ea564c71-dd65-4e1e-b9f0-3ac09cd10579/-/preview/-/enhance/85/)

Какие-то огромные кнопки, вам не кажется? Если кажется, то можно их сделать значительно симпатичнее, если добавить в объект клавиатуры следующий аргумент `resize_keyboard=True`:

    # Создаем объект клавиатуры, добавляя в него кнопки
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                        keyboard=[[button_1, button_2]],
                                        resize_keyboard=True)

Перезапускаем бота и ...

![](https://ucarecdn.com/ef1c016f-8a59-4b88-abf7-bb557a5cfc96/-/preview/-/enhance/81/)

кажется, так намного лучше.

Если нажать на одну из кнопок - сработает соответствующий хэндлер и клавиатура исчезнет из чата совсем - из-за аргумента `reply_markup=ReplyKeyboardRemove()` . Но иногда нам нужно, чтобы клавиатура просто скрывалась, но была доступна для вызова при необходимости. Так тоже можно. За это отвечает аргумент объекта клавиатуры  `one_time_keyboard=True`. Тогда после нажатия на кнопку, клавиатура будет просто сворачиваться. Ну, разумеется, если мы ее непосредственно не будем удалять в хэндлерах. Перепишем немного код так, чтобы клавиатура не удалялась, а сворачивалась. Т.к. изменения затронут только создание объекта клавиатуры и хэндлеры, то весь код бота приводить не буду, чтобы избежать загромождения.

    # ...
    
    # Создаем объект клавиатуры, добавляя в него кнопки
    keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                        keyboard=[[button_1, button_2]],
                                        resize_keyboard=True,
                                        one_time_keyboard=True)
    
    # ...
    
    # Этот хэндлер будет срабатывать на ответ "Собак 🦮" и удалять клавиатуру
    @dp.message(Text(text='Собак 🦮'))
    async def process_dog_answer(message: Message):
        await message.answer(text='Да, несомненно, кошки боятся собак. '
                                  'Но вы видели как они боятся огурцов?')
    
    
    # Этот хэндлер будет срабатывать на ответ "Огурцов 🥒" и удалять клавиатуру
    @dp.message(Text(text='Огурцов 🥒'))
    async def process_cucumber_answer(message: Message):
        await message.answer(text='Да, иногда кажется, что огурцов '
                                  'кошки боятся больше')
    
    # ...

Мы просто передали объекту клавиатуры аргумент `one_time_keyboard=True`, а из хэндлеров убрали удаление клавиатуры `reply_markup=ReplyKeyboardRemove()`. И теперь клавиатура доступна в любое время, но после нажатия на любую кнопку она сворачивается.

![](https://ucarecdn.com/a45b2052-447d-4d64-a4b7-676b8b2bb04d/)

На следующем шаге детально разберем принципы, по которым располагаются кнопки в клавиатуре.