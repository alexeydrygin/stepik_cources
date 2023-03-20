## Модуль user\_handlers.py
------------------------

Как договаривались - оставим в модуле два простых хэндлера - на команду /start и на команду /help.

### user\_handlers.py

    from aiogram.types import Message
    from aiogram.filters import Command, CommandStart
    from lexicon.lexicon import LEXICON_RU
    
    
    # Этот хэндлер срабатывает на команду /start
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text=LEXICON_RU['/start'])
    
    
    # Этот хэндлер срабатывает на команду /help
    @dp.message(Command(commands='help'))
    async def process_help_command(message: Message):
        await message.answer(text=LEXICON_RU['/help'])

Сообщения для отправки пользователям будем брать из словаря `LEXICON_RU` по соответствующим ключам `'/start'` для хэндлера `process_start_command` и `'/help'` для хэндлера `process_help_command`. Для этого нужно импортировать словарь из соответствующего модуля соответствующего пакета:

    from lexicon.lexicon import LEXICON_RU

Возможно, вы уже на этом этапе заметили, что IDE подчеркивает `dp`.

![](https://ucarecdn.com/ed806091-501d-4660-bfe3-65f75b94e0b0/-/preview/-/enhance/77/)

Пока не будем обращать на это внимание. Продолжаем.