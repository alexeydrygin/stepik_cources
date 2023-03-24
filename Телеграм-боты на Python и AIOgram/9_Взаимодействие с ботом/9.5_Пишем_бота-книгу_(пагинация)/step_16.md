## Хэндлеры: user_handlers.py
---------------------------

Самый объемный модуль бота-книги - модуль с пользовательскими хэндлерами. Сначала посмотрите на код в общем, а потом разберем работу каждого обработчика по-отдельности.

    from copy import deepcopy
    
    from aiogram import Router
    from aiogram.filters import Command, CommandStart, Text
    from aiogram.types import CallbackQuery, Message
    from database.database import user_dict_template, users_db
    from filters.filters import IsDelBookmarkCallbackData, IsDigitCallbackData
    from keyboards.bookmarks_kb import (create_bookmarks_keyboard,
                                        create_edit_keyboard)
    from keyboards.pagination_kb import create_pagination_keyboard
    from lexicon.lexicon import LEXICON
    from services.file_handling import book
    
    router: Router = Router()
    
    
    # Этот хэндлер будет срабатывать на команду "/start" -
    # добавлять пользователя в базу данных, если его там еще не было
    # и отправлять ему приветственное сообщение
    @router.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(LEXICON['/start'])
        if message.from_user.id not in users_db:
            users_db[message.from_user.id] = deepcopy(user_dict_template)
    
    
    # Этот хэндлер будет срабатывать на команду "/help"
    # и отправлять пользователю сообщение со списком доступных команд в боте
    @router.message(Command(commands='help'))
    async def process_help_command(message: Message):
        await message.answer(LEXICON['/help'])
    
    
    # Этот хэндлер будет срабатывать на команду "/beginning"
    # и отправлять пользователю первую страницу книги с кнопками пагинации
    @router.message(Command(commands='beginning'))
    async def process_beginning_command(message: Message):
        users_db[message.from_user.id]['page'] = 1
        text = book[users_db[message.from_user.id]['page']]
        await message.answer(
                text=text,
                reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                        'forward'))
    
    
    # Этот хэндлер будет срабатывать на команду "/continue"
    # и отправлять пользователю страницу книги, на которой пользователь
    # остановился в процессе взаимодействия с ботом
    @router.message(Command(commands='continue'))
    async def process_continue_command(message: Message):
        text = book[users_db[message.from_user.id]['page']]
        await message.answer(
                    text=text,
                    reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                        'forward'))
    
    
    # Этот хэндлер будет срабатывать на команду "/bookmarks"
    # и отправлять пользователю список сохраненных закладок,
    # если они есть или сообщение о том, что закладок нет
    @router.message(Command(commands='bookmarks'))
    async def process_bookmarks_command(message: Message):
        if users_db[message.from_user.id]["bookmarks"]:
            await message.answer(
                text=LEXICON[message.text],
                reply_markup=create_bookmarks_keyboard(
                    *users_db[message.from_user.id]["bookmarks"]))
        else:
            await message.answer(text=LEXICON['no_bookmarks'])
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
    # во время взаимодействия пользователя с сообщением-книгой
    @router.callback_query(Text(text='forward'))
    async def process_forward_press(callback: CallbackQuery):
        if users_db[callback.from_user.id]['page'] < len(book):
            users_db[callback.from_user.id]['page'] += 1
            text = book[users_db[callback.from_user.id]['page']]
            await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                        'forward'))
        await callback.answer()
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
    # во время взаимодействия пользователя с сообщением-книгой
    @router.callback_query(Text(text='backward'))
    async def process_backward_press(callback: CallbackQuery):
        if users_db[callback.from_user.id]['page'] > 1:
            users_db[callback.from_user.id]['page'] -= 1
            text = book[users_db[callback.from_user.id]['page']]
            await callback.message.edit_text(
                    text=text,
                    reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                        'forward'))
        await callback.answer()
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    # с номером текущей страницы и добавлять текущую страницу в закладки
    @router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
    async def process_page_press(callback: CallbackQuery):
        users_db[callback.from_user.id]['bookmarks'].add(
            users_db[callback.from_user.id]['page'])
        await callback.answer('Страница добавлена в закладки!')
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    # с закладкой из списка закладок
    @router.callback_query(IsDigitCallbackData())
    async def process_bookmark_press(callback: CallbackQuery):
        text = book[int(callback.data)]
        users_db[callback.from_user.id]['page'] = int(callback.data)
        await callback.message.edit_text(
                    text=text,
                    reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                        'forward'))
        await callback.answer()
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    # "редактировать" под списком закладок
    @router.callback_query(Text(text='edit_bookmarks'))
    async def process_edit_press(callback: CallbackQuery):
        await callback.message.edit_text(
                    text=LEXICON[callback.data],
                    reply_markup=create_edit_keyboard(
                                    *users_db[callback.from_user.id]["bookmarks"]))
        await callback.answer()
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    # "отменить" во время работы со списком закладок (просмотр и редактирование)
    @router.callback_query(Text(text='cancel'))
    async def process_cancel_press(callback: CallbackQuery):
        await callback.message.edit_text(text=LEXICON['cancel_text'])
        await callback.answer()
    
    
    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    # с закладкой из списка закладок к удалению
    @router.callback_query(IsDelBookmarkCallbackData())
    async def process_del_bookmark_press(callback: CallbackQuery):
        users_db[callback.from_user.id]['bookmarks'].remove(
                                                        int(callback.data[:-3]))
        if users_db[callback.from_user.id]['bookmarks']:
            await callback.message.edit_text(
                        text=LEXICON['/bookmarks'],
                        reply_markup=create_edit_keyboard(
                                *users_db[callback.from_user.id]["bookmarks"]))
        else:
            await callback.message.edit_text(text=LEXICON['no_bookmarks'])
        await callback.answer()

Первая команда, которую пользователь отправляет боту, как всегда /start. Начнем рассмотрение обработчиков с хэндлера этой команды.

    # Этот хэндлер будет срабатывать на команду "/start" -
    # добавлять пользователя в базу данных, если его там еще не было
    # и отправлять ему приветственное сообщение
    @router.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(LEXICON['/start'])
        if message.from_user.id not in users_db:
            users_db[message.from_user.id] = deepcopy(user_dict_template)

Когда бот получает от пользователя команду /start - он отправляет в чат сообщение, которое хранится у нас в словаре `LEXICON` под ключом `"/start"`. Дальше идет проверка есть ли такой пользователь уже в базе данных бота. Если нет - в словаре нашей "игрушечной" базы данных создается новая запись, в которой ключом будет ID пользователя (напоминаю, что его можно получить из апдейта типа `Message` инструкцией `message.from_user.id`), а значением - словарь - шаблон для новых пользователей `user_dict_template`. Для того, чтобы ключ ссылался не просто на уже существующий объект словаря `user_dict_template`, а на новый объект такой же структуры - понадобится функция `deepcopy` из библиотеки `copy`. Если не очень понятно, что за `deepcopy` - можно почитать про то, как устроены переменные в Python и про поверхностные и глубокие копии объектов. Здесь на этом заострять внимание не буду. С регистрацией обработчика команды /start, думаю, вопросов возникнуть не должно. Мы так уже делали не один раз в других ботах.

Следующая команда, которую должен уметь обрабатывать наш бот - /help. 

    # Этот хэндлер будет срабатывать на команду "/help"
    # и отправлять пользователю сообщение со списком доступных команд в боте
    @router.message(Command(commands='help'))
    async def process_help_command(message: Message):
        await message.answer(LEXICON['/help'])

Тут никаких сложностей нет. По команде /help от пользователя, бот отправляет в чат сообщение, которое хранится в словаре `LEXICON` по ключу `"/help"`.

Следующий обработчик - обработчик команды /beginning.

    # Этот хэндлер будет срабатывать на команду "/beginning"
    # и отправлять пользователю первую страницу книги с кнопками пагинации
    @router.message(Command(commands='beginning'))
    async def process_beginning_command(message: Message):
        users_db[message.from_user.id]['page'] = 1
        text = book[users_db[message.from_user.id]['page']]
        await message.answer(
                text=text,
                reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                        'forward'))

По этой команде в "базе данных" для пользователя, отправившего команду, ключу `'page'` присваивается значение 1, то есть ссылка на 1-ю страницу книги. Переменная `text` ссылается на эту страницу и текст отравляется ботом в чат вместе с кнопками пагинации (с помощью функции `create_pagination_keyboard`. В качестве аргументов в функцию передаются значения `'backward'`, значение по ключу `'page'`, то есть номер страницы пользователя, вместе с общим количеством страниц книги через разделитель `/` и значение `'forward'`. Функция `create_pagination_keyboard`, которую мы разбирали, когда рассматривали модуль `pagination_kb.py`, возвращает объект клавиатуры (`InlineKeyboardMarkup`), в котором в качестве отображаемого текста для кнопок значения по ключам из словаря `LEXICON` `'backward'` и `'forward'`, а `callback_data` для этих кнопок соответственно также `'backward'` и `'forward'`. Для центральной кнопки с номером страницы отображаемый текст вида `{номер страницы}/{всего страниц в книге}`, а `callback_data` для этой кнопки в этом же формате, то есть `{номер страницы}/{всего страниц в книге}`. 

![](https://ucarecdn.com/0aaadc91-f8b0-4dd9-b266-3e50abc770e5/-/preview/-/enhance/83/)

Следующий обработчик - обработчик команды /сontinue.

    # Этот хэндлер будет срабатывать на команду "/continue"
    # и отправлять пользователю страницу книги, на которой пользователь
    # остановился в процессе взаимодействия с ботом
    @router.message(Command(commands='continue'))
    async def process_continue_command(message: Message):
        text = book[users_db[message.from_user.id]['page']]
        await message.answer(
                    text=text,
                    reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{users_db[message.from_user.id]["page"]}/{len(book)}',
                        'forward'))

По сути хэндлер команды /continue мало чем отличается от хэндлера команды /beginning. Разница лишь в том, что в "базе данных" ключу `'page'` не присваивается значение 1, а текст берется из словаря `book` по ключу, который как раз и хранится в базе данных по ключу `'page'`. То есть, если пользователь остановился на 30-й странице книги, то бот отправит в чат сообщение с текстом из словаря `book` по ключу 30, а не 1, как в случае команды /beginning. Клавиатура пагинации, под сообщением с текстом страницы книги, формируется аналогичным предыдущему хэндлеру образом.

Далее идет обработчик команды /bookmarks.

    # Этот хэндлер будет срабатывать на команду "/bookmarks"
    # и отправлять пользователю список сохраненных закладок,
    # если они есть или сообщение о том, что закладок нет
    @router.message(Command(commands='bookmarks'))
    async def process_bookmarks_command(message: Message):
        if users_db[message.from_user.id]["bookmarks"]:
            await message.answer(
                text=LEXICON[message.text],
                reply_markup=create_bookmarks_keyboard(
                    *users_db[message.from_user.id]["bookmarks"]))
        else:
            await message.answer(text=LEXICON['no_bookmarks'])

Сначала проверяется наличие элементов в множестве по ключу `'bookmarks'` базы данных, то есть наличие сохраненных закладок у пользователя. Если множество не пустое - в чат отправляется сообщение из словаря `LEXICON` по ключу `'/bookmarks'` с клавиатурой, которую формирует функция `create_bookmarks_keyboard`. Кнопки закладок в формате `{номер закладки} - {первые сколько-то символов страницы}`. Телеграм сам обрезает текст под размер кнопки и добавляет в конце многоточие. А в качестве `callback_data` для таких кнопок выступают просто номера страниц, на которые указывают эти закладки. На всякий случай, закладки - это и есть номера сохраненных страниц. Также после списка кнопок с закладками добавляются еще 2 кнопки - "Редактировать" и "Отменить", `callback_data` для которых, соответственно, `'edit_bookmarks'` и `'cancel'`. 

![](https://ucarecdn.com/fb963184-6a1d-4634-8a7c-e508eb41e8a1/-/preview/-/enhance/82/)

Если же множество по ключу `'bookmarks'` базы данных пустое - бот отправляет в чат сообщение из словаря `LEXICON` по ключу `'no_bookmarks'`.

С обработчиками команд разобрались. Теперь нужно разобраться с обработчиками callback-запросов. Первым идет обработчик запроса `'forward'`, то есть нажатия на кнопку "Вперед" с обозначением, в нашем случае, ">>".

    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "вперед"
    # во время взаимодействия пользователя с сообщением-книгой
    @router.callback_query(Text(text='forward'))
    async def process_forward_press(callback: CallbackQuery):
        if users_db[callback.from_user.id]['page'] < len(book):
            users_db[callback.from_user.id]['page'] += 1
            text = book[users_db[callback.from_user.id]['page']]
            await callback.message.edit_text(
                text=text,
                reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                        'forward'))
        await callback.answer()

Сначала проверяется номер текущей страницы в базе данных пользователя. Если он меньше длины словаря `book`, то текущий номер страницы пользователя увеличивается на 1 и по этому номеру, как ключу словаря `book`, текст сохраняется в переменную `text`. Бот отправляет в чат отредактированное сообщение с новой страницей книги и такой же инлайн-клавиатурой пагинации, где в средней кнопке текущий номер страницы увеличен на 1. Если текущая страница уже равна длине словаря с книгой `book` - ничего не меняется. В конце работы хэндлера отправляется пустой `callback.answer()`, чтобы сообщить Телеграму, что хэндлер успешно отработал и пропали часики на кнопке. В качестве фильтра для срабатывания хэндлера - полное совпадение по тексту - `Text(text='forward')`.

По точно такому же принципу работает обработчик запроса `'backward'`:

    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки "назад"
    # во время взаимодействия пользователя с сообщением-книгой
    @router.callback_query(Text(text='backward'))
    async def process_backward_press(callback: CallbackQuery):
        if users_db[callback.from_user.id]['page'] > 1:
            users_db[callback.from_user.id]['page'] -= 1
            text = book[users_db[callback.from_user.id]['page']]
            await callback.message.edit_text(
                    text=text,
                    reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                        'forward'))
        await callback.answer()

С той лишь разницей, что проверяется номер текущей страницы на то, что он больше 1. И если это так, то номер текущей страницы в базе данных уменьшается на 1, по этому новому номеру в качестве ключа словаря `book` текст сохраняется в переменную `text` и отправляется ботом в чат с клавиатурой пагинации. В средней кнопке текущая страница, соответственно, уменьшается на 1. Если же текущий номер страницы равен 1, то ничего не происходит. В конце работы хэндлера отправляется пустой `callback.answer()`. В качестве фильтра для срабатывания хэндлера - также полное совпадение по тексту - `Text(text='backward')`.

Далее идет обработчик нажатия на центральную кнопку пагинации с текущим номером страницы.

    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    # с номером текущей страницы и добавлять текущую страницу в закладки
    @router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
    async def process_page_press(callback: CallbackQuery):
        users_db[callback.from_user.id]['bookmarks'].add(
            users_db[callback.from_user.id]['page'])
        await callback.answer('Страница добавлена в закладки!')

Т.к. в качестве `callback_data` отправляется строка вида `{текущий номер страницы}/{всего страниц в книге}`, то отловить его легко по наличию символа "/" и проверки на то, что все остальные символы, кроме "/" являются числами. Разумеется, можно и через регулярное выражение, но в данном случае не буду усложнять. При срабатывании этого хэндлера текущий номер страницы, хранящийся в базе данных `users_db` по ключу `'page'`, добавляется в множество в этой же базе данных по ключу `'bookmarks'`. Множество здесь выбрано для того, чтобы при нескольких нажатиях на одну и ту же страницу она не добавлялась больше одного раза. Конечно, можно было бы использовать другую структуру данных и предварительно проверять есть ли уже такая страница в ней, но, мне кажется, с множеством проще, потому что все задуманное происходит автоматически - если в множестве страницы нет - она добавляется, если есть - не добавляется. В качестве фильтра я здесь для примера оставил анонимную функцию - `lambda x: '/' in x.data and x.data.replace('/', '').isdigit()`, хотя и можно было бы ее вынести в модуль **filters.py**, как сделано для других фильтров.

Следующий хэндлер отрабатывает нажатие инлайн-кнопки с закладкой из списка закладок, который появляется после того, как пользователь отправит команду /bookmarks.

    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    # с закладкой из списка закладок
    @router.callback_query(IsDigitCallbackData())
    async def process_bookmark_press(callback: CallbackQuery):
        text = book[int(callback.data)]
        users_db[callback.from_user.id]['page'] = int(callback.data)
        await callback.message.edit_text(
                    text=text,
                    reply_markup=create_pagination_keyboard(
                        'backward',
                        f'{users_db[callback.from_user.id]["page"]}/{len(book)}',
                        'forward'))
        await callback.answer()

В данный хэндлер попадают числа - номера страниц, которые пользователь сохранил в закладки, то есть в фильтре нужно проверить, чтобы только цифры были в `callback_data`. В переменную `text` сохраняется текст страницы из словаря `book`, а в базу данных, в качестве текущей страницы, записывается страница из нажатой закладки. Далее бот отправляет сообщение со страницей книги по номеру закладки и клавиатуру пагинации. В конце работы хэндлера отправляется пустой  `callback.answer()`.

Следующий хэндлер срабатывает на нажатие кнопки "Редактировать" с `callback_data='edit_bookmarks'`. 

    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    # "редактировать" под списком закладок
    @router.callback_query(Text(text='edit_bookmarks'))
    async def process_edit_press(callback: CallbackQuery):
        await callback.message.edit_text(
                    text=LEXICON[callback.data],
                    reply_markup=create_edit_keyboard(
                                    *users_db[callback.from_user.id]["bookmarks"]))
        await callback.answer()

Бот отправляет в чат сообщение из словаря `LEXICON` по ключу `'edit_bookmarks'` с клавиатурой, сгенерированной функцией `create_edit_keyboard`. Работу этой функции мы разбирали, когда рассматривали модуль **bookmarks\_kb.py**. Генерируется список закладок для удаления. Перед номером страницы закладки добавляется крестик. В качестве `callback_data` для закладок к удалению  служит строка формата `'{номер закладки (страницы)}del'`. Также под списком инлайн-кнопок с закладками добавляется еще кнопка "Отменить" с `callback_data='cancel'`.

![](https://ucarecdn.com/49e76f13-806e-470a-b24b-31c7458b23d2/-/preview/-/enhance/82/)

В конце работы хэндлера отправляется пустой `callback.answer()`.

Далее идет хэндлер, который отрабатывает нажатие на кнопку "Отменить". Такая кнопка появляется в двух местах во время взаимодействия пользователя с ботом. При просмотре списка закладок и при его редактировании.

    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    # "отменить" во время работы со списком закладок (просмотр и редактирование)
    @router.callback_query(Text(text='cancel'))
    async def process_cancel_press(callback: CallbackQuery):
        await callback.message.edit_text(text=LEXICON['cancel_text'])
        await callback.answer()

При срабатывании этого хэндлера, бот редактирует сообщение со списком закладок, отправляя текст из словаря `LEXICON` по ключу `'cancel_text'`. В конце работы хэндлера отправляется пустой `callback.answer()`.

И последний хэндлер этого модуля служит для удаления закладок.

    # Этот хэндлер будет срабатывать на нажатие инлайн-кнопки
    # с закладкой из списка закладок к удалению
    @router.callback_query(IsDelBookmarkCallbackData())
    async def process_del_bookmark_press(callback: CallbackQuery):
        users_db[callback.from_user.id]['bookmarks'].remove(
                                                        int(callback.data[:-3]))
        if users_db[callback.from_user.id]['bookmarks']:
            await callback.message.edit_text(
                        text=LEXICON['/bookmarks'],
                        reply_markup=create_edit_keyboard(
                                *users_db[callback.from_user.id]["bookmarks"]))
        else:
            await callback.message.edit_text(text=LEXICON['no_bookmarks'])
        await callback.answer()

В качестве фильтра для этого хэндлера служит фильтр `IsDelBookmarkCallbackData` из модуля **filters.py**, который проверяет наличие подстроки `'del'` в `callback_data`, а также чтобы остальная часть `callback_data` (без `'del'`) была числовой. При нажатии на кнопку с закладкой для удаления, строка, содержащая `callback_data`, обрезается - удаляются три последних символа (как раз `'del'`), а оставшееся число (номер страницы) приводится к типу `int` и удаляется из множества по ключу `'bookmarks'`базы данных для текущего пользователя. Далее идет проверка есть ли еще сохраненные закладки в базе данных для текущего пользователя. Если они есть, бот редактирует в чате сообщение с закладками для удаления, отправляя клавиатуру с оставшимися закладками. Если закладок больше нет - сообщение заменяется новым из словаря `LEXICON` по ключу `'no_bookmarks'`. В конце работы хэндлера отправляется пустой `callback.answer()`.