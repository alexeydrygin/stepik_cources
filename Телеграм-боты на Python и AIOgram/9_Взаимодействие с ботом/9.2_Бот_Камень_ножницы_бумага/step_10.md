## Файл user_handlers.py
----------------------

В этом файле прописана вся основная логика взаимодействия бота с пользователем. Здесь мы храним все обработчики всех доступных, в рамках задумки проекта, действий пользователя. Исходя из замысла, нужно уметь обрабатывать следующие действия пользователя:

*   Отправка в чат команды /start
*   Отправка в чат команды /help
*   Нажатие на кнопку "Давай!"
*   Нажатие на кнопку "Не хочу!"
*   Нажатие на кнопку выбора среди вариантов (камень, ножницы или бумага)

Вот такой может быть реализация хэндлеров:

### user\_handlers.py

    from aiogram import Router
    from aiogram.filters import Command, CommandStart, Text
    from aiogram.types import Message
    from keyboards.keyboards import game_kb, yes_no_kb
    from lexicon.lexicon_ru import LEXICON_RU
    from services.services import get_bot_choice, get_winner
    
    router: Router = Router()
    
    
    # Этот хэндлер срабатывает на команду /start
    @router.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)
    
    
    # Этот хэндлер срабатывает на команду /help
    @router.message(Command(commands=['help']))
    async def process_help_command(message: Message):
        await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)
    
    
    # Этот хэндлер срабатывает на согласие пользователя играть в игру
    @router.message(Text(text=LEXICON_RU['yes_button']))
    async def process_yes_answer(message: Message):
        await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)
    
    
    # Этот хэндлер срабатывает на отказ пользователя играть в игру
    @router.message(Text(text=LEXICON_RU['no_button']))
    async def process_no_answer(message: Message):
        await message.answer(text=LEXICON_RU['no'])
    
    
    # Этот хэндлер срабатывает на любую из игровых кнопок
    @router.message(Text(text=[LEXICON_RU['rock'],
                               LEXICON_RU['paper'],
                               LEXICON_RU['scissors']]))
    async def process_game_button(message: Message):
        bot_choice = get_bot_choice()
        await message.answer(text=f'{LEXICON_RU["bot_choice"]} '
                                  f'- {LEXICON_RU[bot_choice]}')
        winner = get_winner(message.text, bot_choice)
        await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)

Чуть более детально пробежимся по хэндлерам, чтобы было понятнее.

    # Этот хэндлер срабатывает на команду /start
    @router.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text=LEXICON_RU['/start'], reply_markup=yes_no_kb)

Тут все просто. Пользователь присылает в чат команду /start, а бот ему в ответ сообщение с текстом из словаря `LEXICON_RU` по ключу `'/start'` и клавиатурой `yes_no_kb` с обычными кнопками. Как вы, возможно, помните, у этой клавиатуры есть дополнительный параметр `one_time_keyboard=True`, чтобы она сворачивалась после того, как пользователь нажмет на одну из кнопок. И хотя она должна сворачиваться по нажатию на любую кнопку, нам важно, чтобы она сворачивалась на отрицательный ответ пользователя, потому что если ответ будет положительный - бот просто пришлет другую клавиатуру - с игровыми кнопками и нам уже не важно, что будет с клавиатурой `yes_no_kb`, потому что ее не будет видно.

![](https://ucarecdn.com/1faf3a67-b31f-4934-9a42-23d68c5422a8/-/crop/636x271/0,0/-/preview/-/enhance/81/)

Хэндлер, срабатывающий на команду /help, не сложнее предыдущего.

    # Этот хэндлер срабатывает на команду /help
    @router.message(Command(commands=['help']))
    async def process_help_command(message: Message):
        await message.answer(text=LEXICON_RU['/help'], reply_markup=yes_no_kb)

Когда пользователь присылает в чат эту команду, бот отвечает текстом из словаря `LEXICON_RU` по ключу `'/help'` и с той же клавиатурой `yes_no_kb`.

![](https://ucarecdn.com/4dbb4371-82ec-4d5c-890d-bf331fc6d284/-/preview/-/enhance/79/)

Далее необходимо обработать нажатие на одну из кнопок выбора играть или нет. Сначала согласие.

    # Этот хэндлер срабатывает на согласие пользователя играть в игру
    @router.message(Text(text=LEXICON_RU['yes_button']))
    async def process_yes_answer(message: Message):
        await message.answer(text=LEXICON_RU['yes'], reply_markup=game_kb)

Когда пользователь нажимает на кнопку согласия, то есть отправляет в чат текст с этой кнопки, который хранится в словаре `LEXICON_RU` по ключу `'yes_button'`, срабатывает хэндлер, настроенный на этот текст и бот присылает пользователю сообщение, которое хранится в том же словаре по ключу `'yes'`, а также игровую клавиатуру `game_kb` с игровыми кнопками. У этой клавиатуры, если вы помните, нет параметра `one_time_keyboard=True`, потому что он не нужен. По задумке, бот после нажатия пользователя на одну из кнопок этой клавиатуры, выводит результат игры и сразу отправляет клавиатуру `yes_no_kb` с предложением сыграть еще раз.

![](https://ucarecdn.com/31ab70cd-afc2-4b37-b2f6-f95eafb5c31d/-/preview/-/enhance/79/)

Следующим идет хэндлер, обрабатывающий нажатие кнопки "Не хочу!"

    # Этот хэндлер срабатывает на отказ пользователя играть в игру
    @router.message(Text(text=LEXICON_RU['no_button']))
    async def process_no_answer(message: Message):
        await message.answer(text=LEXICON_RU['no'])

Если пользователь нажимает на кнопку с текстом отказа (текст отказа хранится в словаре `LEXICON_RU` по ключу `'no_button'`), бот отправляет сообщение в чат из словаря `LEXICON_RU` по ключу `'no'`, а клавиатуру никакую не отправляет. А так как перед срабатыванием этого хэндлера была активна клавиатура `yes_no_kb` с параметром `one_time_keyboard=True`, то эта клавиатура просто сворачивается.

![](https://ucarecdn.com/aba5475b-5b82-446f-b8ce-a7e366a4a996/-/preview/-/enhance/78/)

Ну, и последний хэндлер в модуле **user\_handlers.py**, отвечающий за нажатие пользователем одной из игровых кнопок.

    # Этот хэндлер срабатывает на любую из игровых кнопок
    @router.message(Text(text=[LEXICON_RU['rock'],
                               LEXICON_RU['paper'],
                               LEXICON_RU['scissors']]))
    async def process_game_button(message: Message):
        bot_choice = get_bot_choice()
        await message.answer(text=f'{LEXICON_RU["bot_choice"]} '
                                  f'- {LEXICON_RU[bot_choice]}')
        winner = get_winner(message.text, bot_choice)
        await message.answer(text=LEXICON_RU[winner], reply_markup=yes_no_kb)

По сути, в этом хэндлере реализована вся игровая логика бота, или как ее называют в общем случае - бизнес-логика, но не напрямую, а путем обращения к функциям из модуля **services.py**. Модуль **services.py** у нас описан в следующем шаге, поэтому подробно функции из него разберем там, а здесь опишу работу хэндлера.

При нажатии на одну из игровых кнопок, в чат боту отправляется текст с этой кнопки. Тексты кнопок хранятся в словаре `LEXICON_RU` по ключам `'rock'`, `'paper'` и `'scissors'`. Хэндлер срабатывает на эти тексты, потому что они указаны в декораторе хэндлера в фильтре `Text`. Как только хэндлер срабатывает - происходит вызов функции `get_bot_choice` из модуля **services.py**, которая генерирует ответ бота в игре. Этот ответ сохраняется в переменной `bot_choice`. Далее пользователю отправляется сообщение с выбором бота и после этого вызывается функция `get_winner` также из модуля **services.py**, результат работы которой сохраняется в переменной `winner`. Функция `get_winner` принимает 2 аргумента - выбор пользователя - текст, который отправляется в чат при нажатии на кнопку выбора и выбор бота - результат вызова функции `get_bot_choice`. После этого бот отправляет пользователю сообщение из словаря `LEXICON_RU` по ключу, который хранится в переменной `winner`, а также клавиатуру `yes_no_kb`. Цикл замкнулся :)

![](https://ucarecdn.com/ebf0080e-9db3-4088-9d5e-2bd19c7c7605/-/preview/-/enhance/79/)