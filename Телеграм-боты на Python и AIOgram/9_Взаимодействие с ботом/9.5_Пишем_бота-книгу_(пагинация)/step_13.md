## Клавиатуры: bookmarks_kb.py
----------------------------

Модуль **bookmarks\_kb.py** отвечает за клавиатуры для работы с закладками пользователя.

### bookmarks\_kb.py

    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
    from aiogram.utils.keyboard import InlineKeyboardBuilder
    from lexicon.lexicon import LEXICON
    from services.file_handling import book
    
    
    def create_bookmarks_keyboard(*args: int) -> InlineKeyboardMarkup:
        # Создаем объект клавиатуры
        kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        # Наполняем клавиатуру кнопками-закладками в порядке возрастания
        for button in sorted(args):
            kb_builder.row(InlineKeyboardButton(
                text=f'{button} - {book[button][:100]}',
                callback_data=str(button)))
        # Добавляем в клавиатуру в конце две кнопки "Редактировать" и "Отменить"
        kb_builder.row(InlineKeyboardButton(
                            text=LEXICON['edit_bookmarks_button'],
                            callback_data='edit_bookmarks'),
                       InlineKeyboardButton(
                            text=LEXICON['cancel'],
                            callback_data='cancel'),
                       width=2)
        return kb_builder.as_markup()
    
    
    def create_edit_keyboard(*args: int) -> InlineKeyboardMarkup:
        # Создаем объект клавиатуры
        kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
        # Наполняем клавиатуру кнопками-закладками в порядке возрастания
        for button in sorted(args):
            kb_builder.row(InlineKeyboardButton(
                text=f'{LEXICON["del"]} {button} - {book[button][:100]}',
                callback_data=f'{button}del'))
        # Добавляем в конец клавиатуры кнопку "Отменить"
        kb_builder.row(InlineKeyboardButton(
                            text=LEXICON['cancel'],
                            callback_data='cancel'))
        return kb_builder.as_markup()

Функция `create_bookmarks_keyboard` генерирует список закладок формата `{номер страницы} - {Начальный текст страницы}` в виде инлайн-кнопок (каждая кнопка на новой строке), а также еще две кнопки - "Редактировать" и "Отменить":

![](https://ucarecdn.com/3d589b8d-6e3c-4d16-a0e1-bd36d460dd46/-/preview/-/enhance/79/)

Функция `create_edit_keyboard` генерирует список закладок к удалению и кнопку "Отменить":

![](https://ucarecdn.com/bcd9f562-2ee4-4191-9bcb-840e4c463657/-/preview/-/enhance/81/)

В качестве аргументов в обе функции приходят целые числа - номера страниц, которые пользователь сохранил в закладки. В первой функции эти же числа (строковое их представление) используются для `callback_data`, а во второй - к числам добавляется текст `'del'`, чтобы можно было отловить нажатия на них соответствующими хэндлерами.

От текста страницы, при генерации кнопок, берем первые сто символов страницы с помощью среза `book[button][:100]`, но по факту телеграм использует меньше, чем 100, сам обрезая текст по размеру кнопки и добавляя многоточие в конце.