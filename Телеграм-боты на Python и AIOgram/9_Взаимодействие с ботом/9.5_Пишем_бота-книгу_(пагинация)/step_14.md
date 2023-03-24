## Хэндлеры: other_handlers.py
----------------------------

Здесь код очень простой, похожий на тот, что мы использовали в Эхо-боте:

### other\_handlers.py

    from aiogram import Router
    from aiogram.types import Message
    
    router: Router = Router()
    
    
    # Этот хэндлер будет реагировать на любые сообщения пользователя,
    # не предусмотренные логикой работы бота
    @router.message()
    async def send_echo(message: Message):
        await message.answer(f'Это эхо! {message.text}')

Я не стал заморачиваться с каким-то осмысленным ответом бота на любые текстовые сообщения пользователя. Если хотите - напишите что-нибудь свое поинтереснее.