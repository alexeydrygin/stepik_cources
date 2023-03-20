## Диспетчер в отдельном модуле
----------------------------

Итак, идея такая. Создаем дополнительный модуль в корне проекта. Пусть он называется, например, **create\_dp.py**. Инициализируем в нем объект диспетчера. И будем его потом везде импортировать - и в точку входа, и в хэндлеры, и так далее.

### create\_dp.py

    from aiogram import Dispatcher
    
    dp: Dispatcher = Dispatcher()

Соответственно, нужно немного переделать остальные модули проекта.

### bot.py

    import asyncio
    
    from aiogram import Bot, Dispatcher
    from config_data.config import Config, load_config
    from create_dp import dp
    
    
    # Функция конфигурирования и запуска бота
    async def main(dp: Dispatcher):
    
        # Загружаем конфиг в переменную config
        config: Config = load_config()
        # Инициализируем бот
        bot: Bot = Bot(token=config.tg_bot.token)
    
        # Пропускаем накопившиеся апдейты и запускаем polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    
    
    if __name__ == '__main__':
        asyncio.run(main(dp))

### user\_handlers.py

    from aiogram.filters import Command, CommandStart
    from aiogram.types import Message
    from create_dp import dp
    from lexicon.lexicon import LEXICON_RU
    
    
    # Этот хэндлер срабатывает на команду /start
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text=LEXICON_RU['/start'])
    
    
    # Этот хэндлер срабатывает на команду /help
    @dp.message(Command(commands='help'))
    async def process_help_command(message: Message):
        await message.answer(text=LEXICON_RU['/help'])

### other\_handlers.py

    from aiogram.types import Message
    from create_dp import dp
    from lexicon.lexicon import LEXICON_RU
    
    
    # Этот хэндлер будет срабатывать на любые ваши сообщения,
    # кроме команд "/start" и "/help"
    @dp.message()
    async def send_echo(message: Message):
        try:
            await message.send_copy(chat_id=message.chat.id)
        except TypeError:
            await message.reply(text=LEXICON_RU['no_echo'])

Прекрасно. Все модули, где должен использоваться диспетчер, связаны через **create\_dp.py**, IDE не ругается. Запускаем **bot.py** иии.... Тишина. Бот запускается, но на команды снова не реагирует. Да что ж такое?

Если догадались что происходит - мой вам респект. Лично я понял далеко не сразу. А если, как и я когда-то, не догадались - сейчас объясню. Мы запускаем файл **bot.py** - в нем происходят импорты классов бота и диспетчера, затем импорты данных из модуля **config.py** пакета **config\_data**, а затем импорт объекта `dp` из модуля **create\_dp.py**. А как вы уже знаете, код в модулях, из которых хоть что-то импортируется, исполняется полностью. Ну, импортировали мы с вами `dp` в **bot.py** и чего? Код с хэндлерами как стоял нетронутым, так и остался. Чтобы он исполнился все равно ОТТУДА что-нибудь, да нужно импортировать. А мы импортируем только ТУДА :)

Возникают и еще идеи. А давайте в каждом модуле с хэндлерами заведем какую-нибудь переменную и будем ее импортировать в **bot.py**, чтобы связать, наконец, все воедино?.. А вот так, кстати, может сработать. Но как-то костыли какие-то лезут со всех щелей. Этого ли мы хотим? Мало того, что отдельный модуль для инициализации диспетчера придумали, так еще и какие-то переменные, бесполезные, в целом, заводить решили, просто для того, чтобы импорты собрать в одну кучу. Как-то такое себе.

Ну, или можно целиком модули с хэндлерами импортировать. Тоже будет работать. Правда линтеры взвоют, типа, модуль импортирован, но не используется. Линтеры же не знают, что мы модуль импортируем исключительно для того, чтобы в нем код выполнился.

![](https://ucarecdn.com/e1dcbefd-5124-4b94-a8b4-2e03a9aadb98/-/preview/-/enhance/77/)

А если все-таки мы импортируем переменные и они будут не бесполезные?.. Хм...

И, вот, теперь, когда вы прониклись и осознали всю глубину проблемы, я готов рассказать вам про роутеры :)