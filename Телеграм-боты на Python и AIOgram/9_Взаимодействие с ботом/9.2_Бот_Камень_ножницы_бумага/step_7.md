## Файл keyboards.py
-----------------

В данном модуле будут храниться две клавиатуры. Одна с кнопками "Давай!" и "Не хочу!", а вторая с игровыми кнопками "Камень 🗿", "Ножницы ✂" и "Бумага 📜". Причем, для того, чтобы еще раз лучше понять разницу между созданием клавиатур с помощью билдера клавиатур и без него, реализуем оба варианта. Первая клавиатура будет с билдером, а вторая без.
```python

    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    from aiogram.utils.keyboard import ReplyKeyboardBuilder
    
    from lexicon.lexicon_ru import LEXICON_RU
    
    # ------- Создаем клавиатуру через ReplyKeyboardBuilder -------
    
    # Создаем кнопки с ответами согласия и отказа
    button_yes: KeyboardButton = KeyboardButton(text=LEXICON_RU['yes_button'])
    button_no: KeyboardButton = KeyboardButton(text=LEXICON_RU['no_button'])
    
    # Инициализируем билдер для клавиатуры с кнопками "Давай" и "Не хочу!"
    yes_no_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    
    # Добавляем кнопки в билдер с параметром width=2
    yes_no_kb_builder.row(button_yes, button_no, width=2)
    
    # Создаем клавиатуру с кнопками "Давай!" и "Не хочу!"
    yes_no_kb = yes_no_kb_builder.as_markup(
                                    one_time_keyboard=True,
                                    resize_keyboard=True)
    
    # ------- Создаем игровую клавиатуру без использования билдера -------
    
    # Создаем кнопки игровой клавиатуры
    button_1: KeyboardButton = KeyboardButton(text=LEXICON_RU['rock'])
    button_2: KeyboardButton = KeyboardButton(text=LEXICON_RU['scissors'])
    button_3: KeyboardButton = KeyboardButton(text=LEXICON_RU['paper'])
    
    # Создаем игровую клавиатуру с кнопками "Камень 🗿",
    # "Ножницы ✂" и "Бумага 📜" как список списков
    game_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                        keyboard=[[button_1],
                                                  [button_2],
                                                  [button_3]],
                                        resize_keyboard=True)
```

У клавиатуры `yes_no_kb` добавляем параметр `one_time_keyboard=True`, потому что эта клавиатура должна сворачиваться после нажатия пользователя на кнопку с текстом "Не хочу!". А если пользователь нажмет на кнопку "Давай!" - клавиатура `yes_no_kb` будет заменена на игровую клавиатуру. 

Игровой клавиатуре `game_kb` параметр `one_time_keyboard` не нужен, потому что каждый раз, когда пользователь будет делать свой игровой выбор, бот будет сообщать о том, кто победил и присылать клавиатуру `yes_no_kb`, чтобы узнать у пользователя хочет ли он сыграть еще раз.

Вот так будет выглядеть клавиатура `yes_no_kb`:

![](https://ucarecdn.com/58182fd8-3900-4453-a2c2-0757f0655caa/-/preview/-/enhance/72/)

А вот так будет выглядеть игровая клавиатура `game_kb`:

![](https://ucarecdn.com/a043c454-e044-471d-b3ef-33a9da24450d/-/preview/-/enhance/77/)

Тексты, которые будут отображаться на кнопках клавиатуры, берем по соответствующим ключам из словаря `LEXICON_RU`, который предварительно импортируем из модуля `lexicon_ru` в пакете `lexicon`.

Вообще, если в телеграм-боте используется много разных клавиатур - они не хардкодятся как в этом примере. Они создаются на лету специальными функциями, принимающими в качестве параметров количество кнопок, количество рядов, количество кнопок в ряде, тексты, отображаемые на кнопках и т.п. Но здесь клавиатур всего две, поэтому наш подход может считаться оправданным.