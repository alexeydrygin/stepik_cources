## Выберите варианты с правильным вызовом функции `create_inline_kb`, чтобы была сформирована инлайн-клавиатура вида:

![](https://ucarecdn.com/2776a01f-153b-4c4c-9dcc-358fa3003445/-/preview/-/enhance/77/)

### Функция `create_inline_kb`:

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

### Словарь `LEXICON`:

    LEXICON: dict[str, str] = {'but_1': '1',
                               'but_2': '2',
                               'but_3': '3',
                               'but_4': '4',
                               'but_5': '5'}

### Словарь `BUTTONS`:

    BUTTONS: dict[str, str] = {'btn_1': '1',
                               'btn_2': '2',
                               'btn_3': '3',
                               'btn_4': '4',
                               'btn_5': '5'}

**Примечание.** Очень желательно, чтобы вы не просто гадали, а брали, запускали этот код, и смотрели, что происходит.

Еще раз картинка для удобства.

![](https://ucarecdn.com/2776a01f-153b-4c4c-9dcc-358fa3003445/-/preview/-/enhance/77/)

---

### Выберите все подходящие ответы из списка

---

keyboard = create_inline_kb(2, last_btn='Последняя кнопка', BUTTONS)

keyboard = create_inline_kb(2, last_btn=None, b_1='1', b_2='2', b_3='3', b_4='4', b_5='5', b_6='Последняя кнопка')

keyboard = create_inline_kb(2, last_btn='Последняя кнопка', *BUTTONS)

**keyboard = create_inline_kb(2, last_btn='Последняя кнопка', \*\*BUTTONS)**

**keyboard = create_inline_kb(2, last_btn='Последняя кнопка', b_1='1', b_2='2', b_3='3', b_4='4', b_5='5')**

keyboard = create_inline_kb(3, 'but_1', 'but_2', 'but_3', 'but_4', 'but_5', last_btn='Последняя кнопка')