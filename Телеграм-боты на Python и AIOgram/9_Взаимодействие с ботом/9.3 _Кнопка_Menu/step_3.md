## Удаление кнопки Menu
--------------------

Иногда нужно не просто изменить команды, доступные по нажатию на кнопку Menu, а нужно полное их удаление вместе с кнопкой. Для этого тоже есть метод у объекта типа `Bot` - `delete_my_commands()`

То есть, если вы хотите удалить кнопку Menu - достаточно просто вызвать данный метод в нужном месте программы, не забывая о том, что он асинхронный. Например, можно написать хэндлер, который будет удалять кнопку по команде /delmenu:

    # Этот хэндлер будет срабатывать на команду "/delmenu"
    # и удалять кнопку Menu c командами
    @dp.message(Command(commands='delmenu'))
    async def del_main_menu(message: Message, bot: Bot):
        await bot.delete_my_commands()
        await message.answer(text='Кнопка "Menu" удалена')

**Примечание.** Иногда кнопка Menu может удалиться не сразу. Возможно, даже понадобится перезапуск клиента, то есть приложения Telegram.