## Собственный генератор клавиатур
-------------------------------

С точки зрения модульного программирования, формировать клавиатуры напрямую в хэндлерах - это не очень хорошая практика. Намного лучше вызывать готовую клавиатуру из другого модуля или формировать ее "на лету" с помощью функций или классов, также хранящихся в других модулях. Использовать билдер для клавиатур мы с вами научились и, в принципе, он решает большинство задач по созданию клавиатур, но иногда бывает удобнее использовать собственную функцию, генерирующую клавиатуры, в зависимости от переданных аргументов. В этом шаге я покажу как примерно может выглядеть такая функция для динамического формирования инлайн-клавиатуры с callback-кнопками, которая будет нормально работать в большинстве случаев. И, по сути, это будет просто некоторая обертка над билдером.

Мы уже знаем, что количество кнопок в ряду, если добавлять их методом `row()` билдера, регулируется параметром `width`. Расположение кнопок автоматически подтстраивается под значение этого параметра. Это свойство и будем использовать, когда нам не очень важно, как именно расположены кнопки, лишь бы они были. Конечно, если вы захотите какую-то мудреную конфигурацию - придется что-то допиливать, но как я уже сказал, для большинства задач автоматическое расположение кнопок билдером, вполне подходит.

А что мы вообще хотим от функции - генератора инлайн-клавиатур?

*   Чтобы на вход она принимала параметр `width`, который мы потом передадим как аргумент в метод `row()` билдера
*   Чтобы принимала строки - callback.data будущих кнопок
*   Чтобы проверяла нет ли в словаре `LEXICON` ключей, совпадающих с переданными в нее строками, чтобы если есть, использовать значения по этим ключам в качестве текста, отображаемого на кнопках
*   Чтобы принимала именованные параметры (ключи/значения) из которых можно сформировать инлайн-кнопки, не прибегая к помощи словаря `LEXICON`

Сейчас все покажу на примерах.

Итак, функция `create_inline_kb`. Ее удобно хранить в одном из модулей пакета `keyboards` шаблона бота.

    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from <имя_директории_с_проектом>.lexicon import LEXICON
    
    
    # Функция для формирования инлайн-клавиатуры на лету
    def create_inline_kb(width: int,
                         *args: str,
                         **kwargs: str) -> InlineKeyboardMarkup:
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

Немного подробностей о том, как она работает. В качестве аргументов функция принимает параметр `width`, который затем будет использован в качестве значения параметра `width` метода `row()` у объекта `InlineKeyboardBuilder`, а также любое количество позиционных (`*args`) и именованных (`**kwargs`) аргументов. Если вы не знаете или не помните, что это такое - рекомендую [статью на Хабре](https://habr.com/ru/company/ruvds/blog/482464/). А возвращает функция объект клавиатуры - экземпляр класса `InlineKeyboardMarkup` с нашими кнопками.

Кнопки можно передать одним из двух способов или их сочетанием:

1.  Через `callback_data` для кнопок (за это отвечает `*args`)
2.  Через именованные аргументы (за это отвечает `**kwargs`), где ключами будут `callback_data` кнопки, а значениями - отображаемый на них текст.

В первом случае будет происходить проверка есть ли в словаре `LEXICON` соответствие `callback_data` кнопок текстам на них и если нет, то текст на кнопках совпадает с генерируемым `callback_data`, а если есть - текст для кнопок берется из словаря. А во втором случае подразумевается, что такое соответствие мы передаем в функцию напрямую в виде пар ключ-значение.

Сначала внутри функции мы инициализируем билдер `kb_builder`, как экземпляр класса `InlineKeyboardBuilder`. Затем инициализируем список `buttons`, который будем наполнять объектами инлайн-кнопок.

Т.к. `args` внутри функции - это кортеж, а `kwargs` - это словарь - мы можем по ним проитерироваться, последовательно создавая экземпляры класса `InlineKeyboardButton` из каждого элемента коллекции, и добавляя каждый из них в список `buttons`.

После чего готовый список с кнопками `buttons` мы передаем методу `row()` билдера, не забывая указать `width`, который также был передан в качестве параметра в нашу функцию.

Ну, а возвращает функция готовый объект клавиатуры `InlineKeyboardMarkup`, который мы уже можем передать как готовую клавиатуру в качестве аргумента туда, где это требуется.

А теперь давайте посмотрим как это работает на практике. Пусть наш очень простой бот формирует клавиатуру "на лету" в хэндлере, который будет срабатывать на команду /start. Никаких хэндлеров, обрабатывающих коллбэки, для простоты этого примера, писать не будем. Код разносить по модулям тоже не будем.

    from aiogram import Bot, Dispatcher
    from aiogram.filters import CommandStart
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    
    # Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
    # полученный у @BotFather
    API_TOKEN: str = 'BOT TOKEN HERE'
    
    # Создаем объекты бота и диспетчера
    bot: Bot = Bot(token=API_TOKEN)
    dp: Dispatcher = Dispatcher()
    
    LEXICON: dict[str, str] = {
        'but_1': 'Кнопка 1',
        'but_2': 'Кнопка 2',
        'but_3': 'Кнопка 3',
        'but_4': 'Кнопка 4',
        'but_5': 'Кнопка 5',
        'but_6': 'Кнопка 6',
        'but_7': 'Кнопка 7',}
    
    BUTTONS: dict[str, str] = {
        'btn_1': '1',
        'btn_2': '2',
        'btn_3': '3',
        'btn_4': '4',
        'btn_5': '5',
        'btn_6': '6',
        'btn_7': '7',
        'btn_8': '8',
        'btn_9': '9',
        'btn_10': '10',
        'btn_11': '11'}
    
    
    # Функция для генерации инлайн-клавиатур "на лету"
    def create_inline_kb(width: int,
                         *args: str,
                         **kwargs: str) -> InlineKeyboardMarkup:
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
    # и отправлять в чат клавиатуру
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        keyboard = create_inline_kb(2, 'but_1', 'but_3', 'but_7')
        await message.answer(text='Вот такая получается клавиатура',
                             reply_markup=keyboard)
    
    
    if __name__ == '__main__':
        dp.run_polling(bot)

Обратите внимание на строчку `keyboard = create_inline_kb(2, 'but_1', 'but_3', 'but_7')` в хэндлере. Только ее мы будем менять в процессе экспериментов ниже. Сначала запустим код как есть.

![](https://ucarecdn.com/2314393e-4192-47cd-8f16-51c8c543b0ff/-/preview/-/enhance/72/)

То есть функция взяла аргумент `width` для ширины клавиатуры, и ключи `'but_1'`, `'but_3'`, `'but_7'`, по которым нашла в словаре `LEXICON` тексты-значения и построила соответствующую клавиатуру.

Если мы передадим параметр `width` со значением `1` - кнопки выстроятся одна под другой.

    keyboard = create_inline_kb(1, 'but_1', 'but_3', 'but_7')

![](https://ucarecdn.com/151d268d-3c8e-4c9d-9982-03b5375bb2dc/-/preview/-/enhance/76/)

Теперь давайте попробуем передать в функцию именованные аргументы.

    keyboard = create_inline_kb(2, btn_tel='Телефон', 
                                   btn_email='email', 
                                   btn_website='Web-сайт', 
                                   btn_vk='VK', 
                                   btn_tgbot='Наш телеграм-бот')

Тоже все работает:

![](https://ucarecdn.com/7b75923a-19f5-45e8-b120-b424bab0abb9/-/preview/-/enhance/77/)

А давайте теперь попробуем передать весь словарь `BUTTONS` с кнопками. Не забудьте распаковать (\*\*) словарь, при передаче в функцию.

    keyboard = create_inline_kb(4, **BUTTONS)

И снова все работает как задумано.

![](https://ucarecdn.com/bdb4f0ca-db00-4710-93a8-a70a07e08fe5/-/preview/-/enhance/75/)

Соответственно, можно комбинировать способы передачи аргументов в функцию и получать разные клавиатуры. Надо только помнить, что сначала будут идти кнопки из словаря `LEXICON`, переданные как аргументы `*args`, а потом кнопки из именованных аргументов - `**kwargs`.

Также вам никто не запрещает модифицировать функцию под свои задачи. Иногда, например, обязательно в клавиатуре нужна последняя кнопка, которая будет занимать отдельный последний ряд. Можно добавить в функцию именованный аргумент `last_btn` со значением по умолчанию `None`, а в теле функции проверять его. Если он содержит в себе что-то - рисуем последнюю кнопку, а если нет - не рисуем. Вот так будет выглядеть модифицированная функция:

    # Функция для генерации инлайн-клавиатур "на лету"
    def create_inline_kb(width: int,
                         *args: str,
                         last_btn: str | None = None,
                         **kwargs: str) -> InlineKeyboardMarkup:
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
        # Добавляем в билдер последнюю кнопку, если она передана в функцию
        if last_btn:
            kb_builder.row(InlineKeyboardButton(
                                text=last_btn,
                                callback_data='last_btn'))
    
        # Возвращаем объект инлайн-клавиатуры
        return kb_builder.as_markup()

И если с ее помощью теперь сформировать клавиатуру:

    keyboard = create_inline_kb(4, last_btn='Последняя кнопка', **BUTTONS)

Результат получится ожидаемым:

![](https://ucarecdn.com/9ff080ab-f04c-414e-850d-315e63b6079b/-/preview/-/enhance/76/)