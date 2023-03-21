## Точка входа bot.py
------------------

Начнем сразу с исполняемого файла, тем более, что от проекта к проекту он будет меняться не сильно.

### bot.py

    import asyncio
    import logging
    
    from aiogram import Bot, Dispatcher
    from config_data.config import Config, load_config
    from handlers import other_handlers, user_handlers
    
    # Инициализируем логгер
    logger = logging.getLogger(__name__)
    
    
    # Функция конфигурирования и запуска бота
    async def main():
        # Конфигурируем логирование
        logging.basicConfig(
            level=logging.INFO,
            format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
                   u'[%(asctime)s] - %(name)s - %(message)s')
    
        # Выводим в консоль информацию о начале запуска бота
        logger.info('Starting bot')
    
        # Загружаем конфиг в переменную config
        config: Config = load_config()
    
        # Инициализируем бот и диспетчер
        bot: Bot = Bot(token=config.tg_bot.token, 
                       parse_mode='HTML')
        dp: Dispatcher = Dispatcher()
    
        # Регистриуем роутеры в диспетчере
        dp.include_router(user_handlers.router)
        dp.include_router(other_handlers.router)
    
        # Пропускаем накопившиеся апдейты и запускаем polling
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    
    
    if __name__ == '__main__':
        try:
            # Запускаем функцию main в асинхронном режиме
            asyncio.run(main())
        except (KeyboardInterrupt, SystemExit):
            # Выводим в консоль сообщение об ошибке,
            # если получены исключения KeyboardInterrupt или SystemExit
            logger.error('Bot stopped!')

Добавилась инструкция, которой мы еще не пользовались ранее `await bot.delete_webhook(drop_pending_updates=True)`. Это способ пропустить накопившиеся апдейты за то время, пока бот их не получал. Так можно делать, если апдейты, которые могут прийти во время отсутствия бота в сети, не критичные. И так делать не рекомендуется, если ваш бот уже в продакшне, особенно, если вы работаете с платежами. Но так как наш игровой бот с платежами не работает - не страшно, если мы будем пропускать апдейты.

Еще обратите внимание на параметр `parse_mode`, в который мы передаем строку `'HTML'`, тем самым мы даем понять боту, что некоторые HTML-теги, поддерживаемые API Telegram, нужно воспринимать именно как HTML-теги. Для примера:

*   <b>жирный текст</b> - **жирный текст**
*   <i>курсив</i> - _курсив_

Подробно про форматирование сообщений будет дальше в [модуле](https://stepik.org/lesson/870035/step/1?unit=874213) "Работа с сообщениями".