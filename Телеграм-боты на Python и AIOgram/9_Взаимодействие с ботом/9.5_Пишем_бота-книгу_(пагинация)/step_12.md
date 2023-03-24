## Клавиатуры: pagination\_kb.py
-----------------------------

Модуль **pagination\_kb.py** отвечает за кнопки под сообщением со страницей книги.

![](https://ucarecdn.com/6478d720-5d61-4740-bb95-b048422cb0fd/-/preview/-/enhance/85/)

### pagination\_kb.py

    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from lexicon.lexicon import LEXICON
    
    
    # Функция, генерирующая клавиатуру для страницы книги
    def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
        # Инициализируем билдер
        kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        # Добавляем в билдер ряд с кнопками
        kb_builder.row(*[InlineKeyboardButton(
            text=LEXICON[button] if button in LEXICON else button,
            callback_data=button) for button in buttons])
        # Возвращаем объект инлайн-клавиатуры
        return kb_builder.as_markup()

Модуль состоит из необходимых импортов и одной функции. Функция принимает строки, а возвращает объект клавиатуры, где в качестве текстов на кнопках - значения из словаря `LEXICON`, если соответствующие ключи есть в словаре. А если ключа в словаре нет, то текст остается таким же, каким был передан в функцию. В качестве `callback_data` передаются значения аргументов функции.

То есть, если мы передаем в функцию аргументы: `'backward'`, `f'{page_number}'`, `'forward'`, то они проверяются на то, являются ли они ключами в словаре `LEXICON`. Если являются, то генерируются кнопки с текстом из значений по этим ключам.

Еще раз. В словаре `LEXICON` у нас есть какие-то ключи и соответствующие им значения:

    LEXICON = {'backward': '<<',
               'forward': '>>'}

В функцию `create_pagination_keyboard` приходит кнопка `'backward'`. Генерируется кнопка с текстом `LEXICON['backward']`, то есть `'<<'` и с `callback_data='backward'`. А когда в функцию приходит кнопка, которая не является ключом в словаре, например, `f'{page_number}'` - генерируется кнопка с текстом `f'{page_number}'` и `callback_data=f'{page_number}'`

Т.к. кнопок для пагинации, в рамках нашего проекта, всего 3 - все они красиво выстраиваются друг за другом в одну строку:

![](https://ucarecdn.com/f0243832-0f37-4267-b916-3aa106e14615/-/preview/-/enhance/80/)