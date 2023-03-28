## Пример кода
-----------

А теперь давайте реализуем предыдущую схему в коде. Сначала, как обычно, будет идти весь код, а ниже я опишу работу каждого блока.

    from aiogram import Bot, Dispatcher, F
    from aiogram.filters import Command, CommandStart, StateFilter, Text
    from aiogram.filters.state import State, StatesGroup
    from aiogram.fsm.context import FSMContext
    from aiogram.fsm.state import default_state
    from aiogram.fsm.storage.memory import MemoryStorage
    from aiogram.types import (CallbackQuery, InlineKeyboardButton,
                               InlineKeyboardMarkup, Message, PhotoSize)
    
    # Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
    # полученный у @BotFather
    BOT_TOKEN = 'BOT TOKEN HERE'
    
    # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage: MemoryStorage = MemoryStorage()
    
    # Создаем объекты бота и диспетчера
    bot: Bot = Bot(BOT_TOKEN)
    dp: Dispatcher = Dispatcher(storage=storage)
    
    # Создаем "базу данных" пользователей
    user_dict: dict[int, dict[str, str | int | bool]] = {}
    
    
    # Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
    class FSMFillForm(StatesGroup):
        # Создаем экземпляры класса State, последовательно
        # перечисляя возможные состояния, в которых будет находиться
        # бот в разные моменты взаимодейтсвия с пользователем
        fill_name = State()        # Состояние ожидания ввода имени
        fill_age = State()         # Состояние ожидания ввода возраста
        fill_gender = State()      # Состояние ожидания выбора пола
        upload_photo = State()     # Состояние ожидания загрузки фото
        fill_education = State()   # Состояние ожидания выбора образования
        fill_wish_news = State()   # Состояние ожидания выбора получать ли новости
    
    
    # Этот хэндлер будет срабатывать на команду /start вне состояний
    # и предлагать перейти к заполнению анкеты, отправив команду /fillform
    @dp.message(CommandStart(), StateFilter(default_state))
    async def process_start_command(message: Message):
        await message.answer(text='Этот бот демонстрирует работу FSM\n\n'
                                  'Чтобы перейти к заполнению анкеты - '
                                  'отправьте команду /fillform')
    
    
    # Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
    # кроме состояния по умолчанию, и отключать машину состояний
    @dp.message(Command(commands='cancel'), ~StateFilter(default_state))
    async def process_cancel_command_state(message: Message, state: FSMContext):
        await message.answer(text='Вы вышли из машины состояний\n\n'
                                  'Чтобы снова перейти к заполнению анкеты - '
                                  'отправьте команду /fillform')
        # Сбрасываем состояние
        await state.clear()
    
    
    # Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
    # по умолчанию и сообщать, что эта команда доступна в машине состояний
    @dp.message(Command(commands='cancel'), StateFilter(default_state))
    async def process_cancel_command(message: Message):
        await message.answer(text='Отменять нечего. Вы вне машины состояний\n\n'
                                  'Чтобы перейти к заполнению анкеты - '
                                  'отправьте команду /fillform')
    
    
    # Этот хэндлер будет срабатывать на команду /fillform
    # и переводить бота в состояние ожидания ввода имени
    @dp.message(Command(commands='fillform'), StateFilter(default_state))
    async def process_fillform_command(message: Message, state: FSMContext):
        await message.answer(text='Пожалуйста, введите ваше имя')
        # Устанавливаем состояние ожидания ввода имени
        await state.set_state(FSMFillForm.fill_name)
    
    
    # Этот хэндлер будет срабатывать, если введено корректное имя
    # и переводить в состояние ожидания ввода возраста
    @dp.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
    async def process_name_sent(message: Message, state: FSMContext):
        # Cохраняем введенное имя в хранилище по ключу "name"
        await state.update_data(name=message.text)
        await message.answer(text='Спасибо!\n\nА теперь введите ваш возраст')
        # Устанавливаем состояние ожидания ввода возраста
        await state.set_state(FSMFillForm.fill_age)
    
    
    # Этот хэндлер будет срабатывать, если во время ввода имени
    # будет введено что-то некорректное
    @dp.message(StateFilter(FSMFillForm.fill_name))
    async def warning_not_name(message: Message):
        await message.answer(text='То, что вы отправили не похоже на имя\n\n'
                                  'Пожалуйста, введите ваше имя\n\n'
                                  'Если вы хотите прервать заполнение анкеты - '
                                  'отправьте команду /cancel')
    
    
    # Этот хэндлер будет срабатывать, если введен корректный возраст
    # и переводить в состояние выбора пола
    @dp.message(StateFilter(FSMFillForm.fill_age),
                lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
    async def process_age_sent(message: Message, state: FSMContext):
        # Cохраняем возраст в хранилище по ключу "age"
        await state.update_data(age=message.text)
        # Создаем объекты инлайн-кнопок
        male_button = InlineKeyboardButton(text='Мужской ♂',
                                           callback_data='male')
        female_button = InlineKeyboardButton(text='Женский ♀',
                                             callback_data='female')
        undefined_button = InlineKeyboardButton(text='🤷 Пока не ясно',
                                                callback_data='undefined_gender')
        # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
        keyboard: list[list[InlineKeyboardButton]] = [[male_button, female_button],
                                                      [undefined_button]]
        # Создаем объект инлайн-клавиатуры
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        # Отправляем пользователю сообщение с клавиатурой
        await message.answer(text='Спасибо!\n\nУкажите ваш пол',
                             reply_markup=markup)
        # Устанавливаем состояние ожидания выбора пола
        await state.set_state(FSMFillForm.fill_gender)
    
    
    # Этот хэндлер будет срабатывать, если во время ввода возраста
    # будет введено что-то некорректное
    @dp.message(StateFilter(FSMFillForm.fill_age))
    async def warning_not_age(message: Message):
        await message.answer(
            text='Возраст должен быть целым числом от 4 до 120\n\n'
                 'Попробуйте еще раз\n\nЕсли вы хотите прервать '
                 'заполнение анкеты - отправьте команду /cancel')
    
    
    # Этот хэндлер будет срабатывать на нажатие кнопки при
    # выборе пола и переводить в состояние отправки фото
    @dp.callback_query(StateFilter(FSMFillForm.fill_gender),
                       Text(text=['male', 'female', 'undefined_gender']))
    async def process_gender_press(callback: CallbackQuery, state: FSMContext):
        # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
        # по ключу "gender"
        await state.update_data(gender=callback.data)
        # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото
        # чтобы у пользователя не было желания тыкать кнопки
        await callback.message.delete()
        await callback.message.answer(text='Спасибо! А теперь загрузите, '
                                           'пожалуйста, ваше фото')
        # Устанавливаем состояние ожидания загрузки фото
        await state.set_state(FSMFillForm.upload_photo)
    
    
    # Этот хэндлер будет срабатывать, если во время выбора пола
    # будет введено/отправлено что-то некорректное
    @dp.message(StateFilter(FSMFillForm.fill_gender))
    async def warning_not_gender(message: Message):
        await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                                  'при выборе пола\n\nЕсли вы хотите прервать '
                                  'заполнение анкеты - отправьте команду /cancel')
    
    
    # Этот хэндлер будет срабатывать, если отправлено фото
    # и переводить в состояние выбора образования
    @dp.message(StateFilter(FSMFillForm.upload_photo),
                F.photo[-1].as_('largest_photo'))
    async def process_photo_sent(message: Message,
                                 state: FSMContext,
                                 largest_photo: PhotoSize):
        # Cохраняем данные фото (file_unique_id и file_id) в хранилище
        # по ключам "photo_unique_id" и "photo_id"
        await state.update_data(photo_unique_id=largest_photo.file_unique_id,
                                photo_id=largest_photo.file_id)
        # Создаем объекты инлайн-кнопок
        secondary_button = InlineKeyboardButton(text='Среднее',
                                                callback_data='secondary')
        higher_button = InlineKeyboardButton(text='Высшее',
                                             callback_data='higher')
        no_edu_button = InlineKeyboardButton(text='🤷 Нету',
                                             callback_data='no_edu')
        # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
        keyboard: list[list[InlineKeyboardButton]] = [
                            [secondary_button, higher_button],
                            [no_edu_button]]
        # Создаем объект инлайн-клавиатуры
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        # Отправляем пользователю сообщение с клавиатурой
        await message.answer(text='Спасибо!\n\nУкажите ваше образование',
                             reply_markup=markup)
        # Устанавливаем состояние ожидания выбора образования
        await state.set_state(FSMFillForm.fill_education)
    
    
    # Этот хэндлер будет срабатывать, если во время отправки фото
    # будет введено/отправлено что-то некорректное
    @dp.message(StateFilter(FSMFillForm.upload_photo))
    async def warning_not_photo(message: Message):
        await message.answer(text='Пожалуйста, на этом шаге отправьте '
                                  'ваше фото\n\nЕсли вы хотите прервать '
                                  'заполнение анкеты - отправьте команду /cancel')
    
    
    # Этот хэндлер будет срабатывать, если выбрано образование
    # и переводить в состояние согласия получать новости
    @dp.callback_query(StateFilter(FSMFillForm.fill_education),
                       Text(text=['secondary', 'higher', 'no_edu']))
    async def process_education_press(callback: CallbackQuery, state: FSMContext):
        # Cохраняем данные об образовании по ключу "education"
        await state.update_data(education=callback.data)
        # Создаем объекты инлайн-кнопок
        yes_news_button = InlineKeyboardButton(text='Да',
                                               callback_data='yes_news')
        no_news_button = InlineKeyboardButton(text='Нет, спасибо',
                                              callback_data='no_news')
        # Добавляем кнопки в клавиатуру в один ряд
        keyboard: list[list[InlineKeyboardButton]] = [
                                        [yes_news_button,
                                         no_news_button]]
        # Создаем объект инлайн-клавиатуры
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        # Редактируем предыдущее сообщение с кнопками, отправляя
        # новый текст и новую клавиатуру
        await callback.message.edit_text(text='Спасибо!\n\n'
                                              'Остался последний шаг.\n'
                                              'Хотели бы вы получать новости?',
                                         reply_markup=markup)
        # Устанавливаем состояние ожидания выбора получать новости или нет
        await state.set_state(FSMFillForm.fill_wish_news)
    
    
    # Этот хэндлер будет срабатывать, если во время выбора образования
    # будет введено/отправлено что-то некорректное
    @dp.message(StateFilter(FSMFillForm.fill_education))
    async def warning_not_education(message: Message):
        await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                                  'при выборе образования\n\nЕсли вы хотите '
                                  'прервать заполнение анкеты - отправьте '
                                  'команду /cancel')
    
    
    # Этот хэндлер будет срабатывать на выбор получать или
    # не получать новости и выводить из машины состояний
    @dp.callback_query(StateFilter(FSMFillForm.fill_wish_news),
                       Text(text=['yes_news', 'no_news']))
    async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
        # C помощью менеджера контекста сохраняем данные о
        # получении новостей по ключу "wish_news"
        await state.update_data(wish_news=callback.data == 'yes_news')
        # Добавляем в "базу данных" анкету пользователя
        # по ключу id пользователя
        user_dict[callback.from_user.id] = await state.get_data()
        # Завершаем машину состояний
        await state.clear()
        # Отправляем в чат сообщение о выходе из машины состояний
        await callback.message.edit_text(text='Спасибо! Ваши данные сохранены!\n\n'
                                              'Вы вышли из машины состояний')
        # Отправляем в чат сообщение с предложением посмотреть свою анкету
        await callback.message.answer(text='Чтобы посмотреть данные вашей '
                                           'анкеты - отправьте команду /showdata')
    
    
    # Этот хэндлер будет срабатывать, если во время согласия на получение
    # новостей будет введено/отправлено что-то некорректное
    @dp.message(StateFilter(FSMFillForm.fill_wish_news))
    async def warning_not_wish_news(message: Message):
        await message.answer(text='Пожалуйста, воспользуйтесь кнопками!\n\n'
                                  'Если вы хотите прервать заполнение анкеты - '
                                  'отправьте команду /cancel')
    
    
    # Этот хэндлер будет срабатывать на отправку команды /showdata
    # и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
    @dp.message(Command(commands='showdata'), StateFilter(default_state))
    async def process_showdata_command(message: Message):
        # Отправляем пользователю анкету, если она есть в "базе данных"
        if message.from_user.id in user_dict:
            await message.answer_photo(
                photo=user_dict[message.from_user.id]['photo_id'],
                caption=f'Имя: {user_dict[message.from_user.id]["name"]}\n'
                        f'Возраст: {user_dict[message.from_user.id]["age"]}\n'
                        f'Пол: {user_dict[message.from_user.id]["gender"]}\n'
                        f'Образование: {user_dict[message.from_user.id]["education"]}\n'
                        f'Получать новости: {user_dict[message.from_user.id]["wish_news"]}')
        else:
            # Если анкеты пользователя в базе нет - предлагаем заполнить
            await message.answer(text='Вы еще не заполняли анкету. '
                                      'Чтобы приступить - отправьте '
                                      'команду /fillform')
    
    
    # Этот хэндлер будет срабатывать на любые сообщения, кроме тех
    # для которых есть отдельные хэндлеры, вне состояний
    @dp.message(StateFilter(default_state))
    async def send_echo(message: Message):
        await message.reply(text='Извините, моя твоя не понимать')
    
    
    # Запускаем поллинг
    if __name__ == '__main__':
        dp.run_polling(bot)

Весь код в одном файле здесь просто для наглядности, думаю, вы уже привыкли. Давайте теперь посмотрим на него детально. Во-первых, появилось несколько новых импортов.

    from aiogram.filters import StateFilter

Из фильтров импортируем класс `StateFilter` - фильтр, отвечающий, как понятно из названия, за состояния. То есть апдейты будут проходить не только через фильтры команд или фильтры callback.data, или фильтры на наличие определенного текста в сообщениях, но еще и через фильтры состояний. Когда мы не пишем никаких фильтров состояний для хэндлеров, подразумевается, что хэндлеры будут срабатывать в любых состояниях.

    from aiogram.filters.state import State, StatesGroup

Здесь мы импортируем еще два класса - `StatesGroup`, отвечающий за группу состояний и `State`, отвечающий за сами состояния. Внутри бота мы можем запускать машину состояний столько раз, сколько нам это необходимо и состояния могут относиться к разной логике. Например, в первом случае машина состояний запущена, как в нашем примере, для сбора анкетных данных, а где-то в другом месте бота мы захотим реализовать через машину состояний, например, настройки бота. И, вот, такие связанные по смыслу состояния принято группировать - объединять в группы состояний, чтобы легче было среди них ориентироваться. В коде выше у нас всего одна группа состояний, потому что не очень логично было бы разделять на группы то, что по смыслу должно быть в одной. Но, в принципе, ничто, кроме здравого смысла, не запрещает сделать хоть на каждое состояние по отдельной группе.

    from aiogram.fsm.context import FSMContext

`FSMContext` - это класс для хранения контекста, в котором находятся пользователи при работе с машиной состояний. Через него мы будем в хэндлеры передавать информацию о состояниях и получать доступ к хранилищу `MemoryStorage` прямо внутри хэндлеров.

    from aiogram.fsm.state import default_state

`default_state` - это состояние по умолчанию, то есть такое состояние, которое установлено, пока мы явно не установили какое-то другое. Во всех наших с вами предыдущих ботах было только одно состояние - как раз `default_state`. Мы его никогда не импортировали раньше, потому что нам не надо было различать состояния. Состояние было только одно. А в этом боте, помимо дефолтного, будут и другие, и нам нужно будет их различать.

    from aiogram.fsm.storage.memory import MemoryStorage

Данной строкой мы импортируем класс `MemoryStorage`, в котором будут храниться все данные состояний всех пользователей во время работы FSM. Здесь надо понимать, что объект класса `MemoryStorage` хранится исключительно в оперативной памяти и при перезапуске бота все данные из него стираются. Его удобно использовать в учебных целях, во время демонстрации работы машины состояний, но не в продакшне, где при перезапуске бота могут потеряться важные данные о состояниях, в которых находились пользователи перед тем, как бот ушел в перезагрузку. На практике `aiogram` поддерживает базы данных типа, Redis, Mongo и т.п. в качестве таких хранилищ, но мы пока останемся в рамках `MemoryStorage`.

С остальными импортами мы уже встречались, поэтому на них останавливаться не будем.

    # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage: MemoryStorage = MemoryStorage()

`MemoryStorage`, как я уже говорил, это некоторое хранилище информации о том, что происходит с пользователями. В каком состоянии они находятся, какие данные они вводили и т.п. Через него хэндлеры могут "общаться" между собой с сохранением нужной, для реализации логики бота, информации. Чаще всего в хэндлеры мы передаем только апдейты - конкретные действия пользователей в конкретный момент времени, но иногда нам нужно передавать еще и дополнительную информацию о пользователях. Ее можно получить либо из базы данных, либо из такого хранилища.

    dp: Dispatcher = Dispatcher(storage=storage)

При инициализации диспетчера, мы указываем, что именно мы будем использовать в качестве такого хранилища.

    # Создаем "базу данных" пользователей
    user_dict: dict[int, dict[str, str | int | bool]] = {}

Ту информацию, которую мы получим от пользователя, в процессе его взаимодействия с машиной состояний, нужно где-то сохранить в удобном для дальнейшей работы формате. В общем случае - это должна быть какая-нибудь база данных. Но так как мы еще до работы с базами данных не дошли, у нас снова в качестве такой "игрушечной" БД будет использоваться словарь. В качестве ключей у такого словаря будут `id` пользователей, а в качестве значений - словари с данными, полученными от пользователей. В процессе работы бота, этот словарь может выглядеть, например, так.

    user_dict = {173901673: {
                      "name": "Арнольд",
                      "age": 45,
                      "gender": "undefined_gender",
                      "photo_unique_id": "AQADfL8xGyZXcEl4",
                      "photo_id": "AgACAgIAAxkBAAIR82OtqD4CMSbFTvitRQNgwhuzf1y1AAJ8vzEbJldwSSpk2bs2OF4_AQADAgADcwADLAQ",
                      "education": "no_edu",
                      "wish_news": False}}

Потом можно будет посмотреть анкету пользователя, которая будет сформирована из данных, хранящихся в этой "базе данных".

    # Cоздаем класс StatesGroup для нашей машины состояний
    class FSMFillForm(StatesGroup):
        # Создаем экземпляры класса State, последовательно
        # перечисляя возможные состояния, в которых будет находиться
        # бот в разные моменты взаимодейтсвия с пользователем
        fill_name = State()        # Состояние ожидания ввода имени
        fill_age = State()         # Состояние ожидания ввода возраста
        fill_gender = State()      # Состояние ожидания выбора пола
        upload_photo = State()     # Состояние ожидания загрузки фото
        fill_education = State()   # Состояние ожидания выбора образования
        fill_wish_news = State()   # Состояние ожидания выбора получать ли новости

Далее мы создаем свой класс `FSMFillForm`, наследуемый от класса `StatesGroup`, в котором будем хранить группу наших состояний. Название класса может быть любым, но обычно принято начинать его с FSM, чтобы было понятно, что он относится к машине состояний. Внутри класса перечисляем все состояния, создавая экземпляры класса `State`. Имеет смысл располагать их последовательно так же, как пользователь будет по ним перемещаться в процессе общения с ботом. Но логика такого общения, конечно, может быть более сложной, чем линейная. Могут быть ветвления, возвраты в предыдущие состояния, перескакивания через несколько состояний, переход в другие группы состояний и т.п. Поэтому последовательное расположение состояний - это просто рекомендация. Для каждого пользователя будет создаваться свой экземпляр класса `FSMFillForm`, поэтому нет опасности, что данные пользователей как-то перемешаются или наложатся.

Далее идут хэндлеры.

    # Этот хэндлер будет срабатывать на команду /start вне состояний
    # и предлагать перейти к заполнению анкеты, отправив команду /fillform
    @dp.message(CommandStart(), StateFilter(default_state))
    async def process_start_command(message: Message):
        await message.answer(text='Этот бот демонстрирует работу FSM\n\n'
                                  'Чтобы перейти к заполнению анкеты - '
                                  'отправьте команду /fillform')

Это стартовый хэндлер, самый первый. Он будет срабатывать на команду /start. Такие хэндлеры есть в каждом нашем боте, потому что любой бот начинается с запуска командой /start. Но теперь появился дополнительный фильтр `StateFilter(default_state)`, который пропустит апдейт в хэндлер только, если команда /start будет отправлена в состоянии "по умолчанию", то есть, пока нами не установлены какие-то другие состояния.

![](https://ucarecdn.com/d9c2a6a0-bc0b-47ce-ac05-315090c6ce78/-/preview/-/enhance/77/)

Следующий хэндлер - это хэндлер на команду /cancel в состоянии "по умолчанию".

    # Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
    # по умолчанию и сообщать, что эта команда работает внутри машины состояний
    @dp.message(Command(commands='cancel'), StateFilter(default_state))
    async def process_cancel_command(message: Message):
        await message.answer(text='Отменять нечего. Вы вне машины состояний\n\n'
                                  'Чтобы перейти к заполнению анкеты - '
                                  'отправьте команду /fillform')

В процессе заполнения анкеты, то есть внутри машины состояний, можно будет через отправку команды /cancel выходить из FSM и удалять все данные, накопленные в процессе ее работы. Но в состоянии "по умолчанию" нет никаких данных, поэтому сбрасывать нечего и логика работы этой команды внутри FSM и вне ее должна отличаться. Вне состояний мы просто сообщаем пользователю, что здесь использование команды ни к чему не приведет.

![](https://ucarecdn.com/6bac92f1-5c4f-4fe4-a24b-a60a355b5bd4/-/preview/-/enhance/77/)

Затем идет хэндлер, срабатывающий на команду /cancel в любых состояниях, кроме состояния "по умолчанию".

    # Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
    # кроме состояния по умолчанию, и отключать машину состояний
    @dp.message(Command(commands='cancel'), ~StateFilter(default_state))
    async def process_cancel_command_state(message: Message, state: FSMContext):
        await message.answer(text='Вы вышли из машины состояний\n\n'
                                  'Чтобы снова перейти к заполнению анкеты - '
                                  'отправьте команду /fillform')
        # Сбрасываем состояние и очищаем данные, полученные внутри состояний
        await state.clear()

В процессе заполнения анкеты пользователь может передумать продолжать ее заполнять. У него должна быть возможность выйти из машины состояний. Команда /cancel призвана ему в этом помочь. Чтобы отловить команду в любом состоянии, кроме дефолтного - ставят дополнительный фильтр `~StateFilter(default_state)`, где `~` выполняет функцию логического отрицания. То есть фильтр пропускает апдейты в хэндлер в любом состоянии, кроме состояния "по умолчанию".

Если пользователь отправляет /cancel, находясь внутри машины состояний - ему приходит сообщение о том, что он вышел из FSM и контекст очищается - `await state.clear()`. То есть стирается информация о состоянии и данные, полученные внутри состояний от пользователя. Другими словами, состояние переходит в состояние по умолчанию, а данные обнуляются.

 ![](https://ucarecdn.com/967e7bfb-ed8b-4872-a5a5-985a135dde56/-/preview/-/enhance/80/)

Далее идет хэндлер, срабатывающий на команду /fillform в дефолтном состоянии.

    # Этот хэндлер будет срабатывать на команду /fillform
    # и переводить бота в состояние ожидания ввода имени
    @dp.message(Command(commands='fillform'), StateFilter(default_state))
    async def process_fillform_command(message: Message, state: FSMContext):
        await message.answer(text='Пожалуйста, введите ваше имя')
        # Устанавливаем состояние ожидания ввода имени
        await state.set_state(FSMFillForm.fill_name)

Когда пользователь отправит в чат команду /fillform - будет установлено первое состояние - `await state.set_state(FSMFillForm.fill_name)` и бот зависнет в ожидании ввода имени.

![](https://ucarecdn.com/7b0855fd-5ad4-4de4-a773-98cd43622c81/-/preview/-/enhance/79/)

Следующим хэндлером идет хэндлер, обрабатывающий корректно введенное имя.

    # Этот хэндлер будет срабатывать, если введено корректное имя
    # и переводить в состояние ожидания ввода возраста
    @dp.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
    async def process_name_sent(message: Message, state: FSMContext):
        # Cохраняем введенное имя в хранилище по ключу "name"
        await state.update_data(name=message.text)
        await message.answer(text='Спасибо!\n\nА теперь введите ваш возраст')
        # Устанавливаем состояние ожидания ввода возраста
        await state.set_state(FSMFillForm.fill_age)

Мы с вами договорились, что корректным будем считать текстовое сообщение, которое состоит из букв, поэтому для проверки мы используем магический фильтр `F.text.isalpha()`, который, во-первых, проверяет, чтобы у апдейта поле "text" не было пустым, а во-вторых, чтобы оно содержало только буквы. Второй фильтр у хэндлера - это фильтр состояния, которое мы устанавливаем, когда пользователь отправляет команду /fillname - `StateFilter(FSMFillForm.fill_name)`.

Как только, находясь в состоянии `FSMFillForm.fill_name`, пользователь отправит корректное имя - непустой текст, состоящий только из букв, сработает этот хэндлер. В него, помимо апдейта `message: Message`, будут переданы данные о текущем состоянии пользователя - контекст `state: FSMContext`. У объекта `state` есть асинхронные методы `get_data()` и `get_state()`, по которым можно получить данные пользователя внутри машины состояний, а также текущее состояние, в котором находится пользователь. Если вывести принтом в терминал результат этих методов:

    # ...
    
    @dp.message(StateFilter(FSMFillForm.fill_name), F.text.isalpha())
    async def process_name_sent(message: Message, state: FSMContext):
        print(await state.get_data())
        print(await state.get_state())
    
    # ...

То можно увидеть в терминале этот самый контекст:

    {}
    FSMFillForm:fill_name

Данных пока нет, потому что мы их еще не успели сохранить, а, вот, состояние ровно то, которое мы ожидаем.

Так как в хэндлер пришел апдейт с предполагаемым именем пользователя - это имя нужно сохранить. Можно, конечно, сразу сохранять его в базу, но есть вероятность, что пользователь прервет заполнение анкеты, а нам, допустим нужны либо все данные от него, либо никакие. Поэтому временно, пока пользователь внутри FSM, можно сохранять данные внутри контекста. Делается это асинхронным методом у объекта `state` - `update_data()`, которому в качестве аргументов передаются ключи и их значения:

    await state.update_data(name=message.text)

То есть по ключу `'name'` мы сохраняем сообщение с именем пользователя из апдейта. Если теперь вывести в терминал результат метода `get_data()` у объекта `state`,

    # ...
    
    # Cохраняем введенное имя в хранилище по ключу "name"
        await state.update_data(name=message.text)
        print(await state.get_data())
    
    # ...

то увидим введенные пользователем данные:

    {'name': 'Эдгар'}

Далее в хэндлере мы отправляем пользователю сообщение с предложением ввести возраст и устанавливаем следующее состояние машины состояний `await state.set_state(FSMFillForm.fill_age)`. Бот зависает в ожидании ввода возраста от пользователя.

![](https://ucarecdn.com/cd0e02cd-f0f4-4871-811c-879ce3cfbbed/-/preview/-/enhance/77/)

Далее по коду идет хэндлер `warning_not_name`. 

    # Этот хэндлер будет срабатывать, если во время ввода имени
    # будет введено что-то некорректное
    @dp.message(StateFilter(FSMFillForm.fill_name))
    async def warning_not_name(message: Message):
        await message.answer(text='То, что вы отправили не похоже на имя\n\n'
                                  'Пожалуйста, введите ваше имя\n\n'
                                  'Если вы хотите прервать заполнение анкеты - '
                                  'отправьте команду /cancel')

Обратите внимание, что этот хэндлер идет после хэндлера `process_name_sent`, потому что если он будет идти до, то до `process_name_sent` очередь никогда не дойдет, ведь фильтр у `warning_not_name` настроен только на состояние и будет забирать все апдейты в состоянии `FSMFillForm.fill_name`. А нам, все-таки в этом состоянии еще нужно ловить корректно введенное имя.

Подразумевается, что если в состоянии `FSMFillForm.fill_name` введено что-то отличное от имени (а также команды /cancel, которая тоже доступна внутри машины состояний) - нужно сообщить пользователю о том, что ожидается именно имя или команда отмены.

![](https://ucarecdn.com/94e02592-13bc-4942-8419-3aba57015c1a/-/preview/-/enhance/79/)

Следующим по коду идет хэндлер `process_age_sent`, который будет срабатывать на корректно введенный возраст, то есть целое число от 4 до 120 включительно.

    # Этот хэндлер будет срабатывать, если введен корректный возраст
    # и переводить в состояние выбора пола
    @dp.message(StateFilter(FSMFillForm.fill_age),
                lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120)
    async def process_age_sent(message: Message, state: FSMContext):
        # Cохраняем возраст в хранилище по ключу "age"
        await state.update_data(age=message.text)
        # Создаем объекты инлайн-кнопок
        male_button = InlineKeyboardButton(text='Мужской ♂',
                                           callback_data='male')
        female_button = InlineKeyboardButton(text='Женский ♀',
                                             callback_data='female')
        undefined_button = InlineKeyboardButton(text='🤷 Пока не ясно',
                                                callback_data='undefined_gender')
        # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
        keyboard: list[list[InlineKeyboardButton]] = [[male_button, female_button],
                                                      [undefined_button]]
        # Создаем объект инлайн-клавиатуры
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        # Отправляем пользователю сообщение с клавиатурой
        await message.answer(text='Спасибо!\n\nУкажите ваш пол',
                             reply_markup=markup)
        # Устанавливаем состояние ожидания выбора пола
        await state.set_state(FSMFillForm.fill_gender)

Фильтры пропустят апдейт в этот хэндлер, если состояние будет `FSMFillForm.fill_age`, а текстовое поле у апдейта будет содержать целое число из желаемого диапазона. Здесь я не стал заморачиваться и писать фильтр-класс, а воспользовался анонимной функцией `lambda x: x.text.isdigit() and 4 <= int(x.text) <= 120`.

Так же как мы сохраняли имя - сохраняем возраст - `await state.update_data(age=message.text)`, после чего формируем инлайн-клавиатуру для следующего пункта анкеты - выбор пола. Отправляем сообщение с клавиатурой и устанавливаем состояние ожидания нажатия на кнопку с выбором пола.

![](https://ucarecdn.com/806c0198-3a62-4ae6-8e47-d2f1c711023c/-/preview/-/enhance/76/)

Если же в состоянии ожидания ввода возраста будет введено что-то отличное от целого числа из диапазона \[4; 120\] - сработает хэндлер  `warning_not_age`.

    # Этот хэндлер будет срабатывать, если во время ввода возраста
    # будет введено что-то некорректное
    @dp.message(StateFilter(FSMFillForm.fill_age))
    async def warning_not_age(message: Message):
        await message.answer(
            text='Возраст должен быть целым числом от 4 до 120\n\n'
                 'Попробуйте еще раз\n\nЕсли вы хотите прервать '
                 'заполнение анкеты - отправьте команду /cancel')

Его смысл точно такой же, как и у хэндлера `warning_not_name`, который мы разбирали ранее. `warning_not_age` будет срабатывать на сообщение любого типа от пользователя в состоянии ввода возраста, и точно также он должен идти по коду позже, чем хэндлер, срабатывающий на корректно введенный возраст.

![](https://ucarecdn.com/2b6f3dae-412b-4585-9552-cee9509b52e5/-/preview/-/enhance/80/)

Далее идет хэндлер `process_gender_press`.

    # Этот хэндлер будет срабатывать на нажатие кнопки при
    # выборе пола и переводить в состояние отправки фото
    @dp.callback_query(StateFilter(FSMFillForm.fill_gender),
                       Text(text=['male', 'female', 'undefined_gender']))
    async def process_gender_press(callback: CallbackQuery, state: FSMContext):
        # Cохраняем пол (callback.data нажатой кнопки) в хранилище,
        # по ключу "gender"
        await state.update_data(gender=callback.data)
        # Удаляем сообщение с кнопками, потому что следующий этап - загрузка фото
        # чтобы у пользователя не было желания тыкать кнопки
        await callback.message.delete()
        await callback.message.answer(text='Спасибо! А теперь загрузите, '
                                           'пожалуйста, ваше фото')
        # Устанавливаем состояние ожидания загрузки фото
        await state.set_state(FSMFillForm.upload_photo)

Его задача обрабатывать апдейты в состоянии `FSMFillForm.fill_gender`, генерируемые нажатием на кнопки выбора пола в инлайн-клавиатуре.

Как именно обрабатывать нажатие на инлайн-кнопки мы с вами уже знаем. Нужно фильтровать апдейты типа `CallbackQuery` по `callack.data`. После сохранения данных о нажатии кнопки с выбором пола `await state.update_data(gender=callback.data)`, нужно удалить сообщение с клавиатурой `await callback.message.delete()`, чтобы оно не смущало пользователя, потому что на следующем шаге ему нужно будет загрузить фото. Сообщаем об этом пользователю, отправляя сообщение с предложением загрузки фотографии, и устанавливаем состояние `FSMFillForm.upload_photo`. 

![](https://ucarecdn.com/d2ba26b9-891d-4850-a3b8-963e22704d8f/-/preview/-/enhance/81/)

На хэндлере `warning_not_gender` подробно останавливаться не будем, думаю, вы уже представляете зачем он нужен по аналогии с похожими, разобранными выше.

    # Этот хэндлер будет срабатывать, если во время выбора пола
    # будет введено/отправлено что-то некорректное
    @dp.message(StateFilter(FSMFillForm.fill_gender))
    async def warning_not_gender(message: Message):
        await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                                  'при выборе пола\n\nЕсли вы хотите прервать '
                                  'заполнение анкеты - отправьте команду /cancel')

Он сработает на любое сообщение от пользователя в состоянии `fill_gender`, но не сработает, при нажатии на инлайн-кнопки, потому что идет в коде позже, чем хэндлер `process_gender_press`, который и будет перехватывать нажатие кнопок в состоянии `FSMFillForm.fill_gender`.

![](https://ucarecdn.com/1a7c8438-bf05-44df-9b93-62a173ad6fd4/-/preview/-/enhance/78/)

Следующий хэндлер `process_photo_sent` будет срабатывать, если пользователь отправит в чат с ботом фото в состоянии ожидания отправки фото `FSMFillForm.upload_photo`.

    # Этот хэндлер будет срабатывать, если отправлено фото
    # и переводить в состояние выбора образования
    @dp.message(StateFilter(FSMFillForm.upload_photo),
                F.photo[-1].as_('largest_photo'))
    async def process_photo_sent(message: Message,
                                 state: FSMContext,
                                 largest_photo: PhotoSize):
        # Cохраняем данные фото (file_unique_id и file_id) в хранилище
        # по ключам "photo_unique_id" и "photo_id"
        await state.update_data(photo_unique_id=largest_photo.file_unique_id,
                                photo_id=largest_photo.file_id)
        # Создаем объекты инлайн-кнопок
        secondary_button = InlineKeyboardButton(text='Среднее',
                                                callback_data='secondary')
        higher_button = InlineKeyboardButton(text='Высшее',
                                             callback_data='higher')
        no_edu_button = InlineKeyboardButton(text='🤷 Нету',
                                             callback_data='no_edu')
        # Добавляем кнопки в клавиатуру (две в одном ряду и одну в другом)
        keyboard: list[list[InlineKeyboardButton]] = [
                            [secondary_button, higher_button],
                            [no_edu_button]]
        # Создаем объект инлайн-клавиатуры
        markup = InlineKeyboardMarkup(inline_keyboard=keyboard)
        # Отправляем пользователю сообщение с клавиатурой
        await message.answer(text='Спасибо!\n\nУкажите ваше образование',
                             reply_markup=markup)
        # Устанавливаем состояние ожидания выбора образования
        await state.set_state(FSMFillForm.fill_education)

С помощью магического фильтра `F.photo[-1].as_('largest_photo')` мы не только фильтруем апдейт по типу контента `'photo'`, но и сразу передаем в хэндлер объект фото типа `PhotoSize` с максимальным разрешением - по ключу `'largest_photo'`. Мы уже рассматривали возможность передачи дополнительных данных из фильтров в хэндлеры в [уроке](https://stepik.org/lesson/891577/step/10?unit=896427), посвященном фильтрам. Сохраняем данные о фото как обычно, с помощью асинхронного метода `update_data()`. Сохраним, на всякий случай и `'file_id'` и `'file_unique_id'`. Затем сформируем инлайн-клавиатуру с кнопками выбора образования, отправим ее пользователю с предложением указать образование, после чего установим состояние ожидания `FSMFillForm.fill_education`.

![](https://ucarecdn.com/b2f893f6-b556-4509-8d87-169237c81e23/-/preview/-/enhance/78/)

Следующий хэндлер уже привычного нам типа `warning_not_photo`  - срабатывает на все подряд в состоянии `upload_photo`, кроме, собственно, фото, которое перехватывает предыдущий хэндлер `process_photo_sent`.

    # Этот хэндлер будет срабатывать, если во время отправки фото
    # будет введено/отправлено что-то некорректное
    @dp.message(StateFilter(FSMFillForm.upload_photo))
    async def warning_not_photo(message: Message):
        await message.answer(text='Пожалуйста, на этом шаге отправьте '
                                  'ваше фото\n\nЕсли вы хотите прервать '
                                  'заполнение анкеты - отправьте команду /cancel')

Логика его работы точно такая же, как у других подобных хэндлеров.

![](https://ucarecdn.com/63eaefa6-2ca5-4fab-b65c-94d51d2285a9/-/preview/-/enhance/78/)

Как работают следующие хэндлеры - `process_education_press`, `warning_not_education` и `warning_not_wish_news` подробно рассматривать не буду. Думаю, их работа понятна по аналогии - рассмотрите их сами. Остановлюсь подробнее на хэндлере `process_wish_news_press`, потому что в этом хэндлере завершается работа машины состояний с сохранением данных пользователя в нашу "игрушечную" базу данных.

    # Этот хэндлер будет срабатывать на выбор получать или не получать новости
    # и выводить пользователя из машины состояний
    @dp.callback_query(StateFilter(FSMFillForm.fill_wish_news),
                       Text(text=['yes_news', 'no_news']))
    async def process_wish_news_press(callback: CallbackQuery, state: FSMContext):
        # Cохраняем данные о получении новостей по ключу "wish_news"
        await state.update_data(wish_news=callback.data == 'yes_news')
        # Добавляем в "базу данных" анкету пользователя
        # по ключу id пользователя
        user_dict[callback.from_user.id] = await state.get_data()
        # Завершаем машину состояний
        await state.clear()
        # Отправляем в чат сообщение о выходе из машины состояний
        await callback.message.edit_text(text='Спасибо! Ваши данные сохранены!\n\n'
                                              'Вы вышли из машины состояний')
        # Отправляем в чат сообщение с предложением посмотреть свою анкету
        await callback.message.answer(text='Чтобы посмотреть данные вашей '
                                           'анкеты - отправьте команду /showdata')

Сначала, при срабатывании хэндлера, как всегда сохраняем новые данные `await state.update_data(wish_news=callback.data == 'yes_news')`, в виде булева значения `True`/`False` и, так как состояние `FSMFillForm.fill_wish_news` - это последнее состояние машины состояний - нужно сохранить все собранные данные в нашу "базу данных", чтобы иметь возможность потом ими как-то манипулировать. Для этого в словарь "базы данных" `user_dict` по ключу <id пользователя>, в качестве значения, сохраняем получившийся словарь с данными пользователя из хранилища. Доступ к нему, как вы уже знаете, можно получить с помощью асинхронного метода `await state.get_data()`. Затем сбрасываем/завершаем машину состояний  - `await state.clear()`. Сообщаем пользователю, что он вышел из машины состояний, а также отправляем еще одно сообщение с предложением посмотреть получившуюся анкету, отправив команду /showdata. 

![](https://ucarecdn.com/d4963398-7930-4410-9a83-0368ffcfd039/-/preview/-/enhance/81/)

Осталось рассмотреть два хэндлера - `process_showdata_command` и `send_echo`. Первый отвечает за показ анкеты пользователю, если он заполнял данные анкеты, а во второй попадают все апдейты, которые не попали в предыдущие хэндлеры. С первым должно быть все понятно.

    # Этот хэндлер будет срабатывать на отправку команды /showdata
    # и отправлять в чат данные анкеты, либо сообщение об отсутствии данных
    @dp.message(Command(commands='showdata'), StateFilter(default_state))
    async def process_showdata_command(message: Message):
        # Отправляем пользователю анкету, если она есть в "базе данных"
        if message.from_user.id in user_dict:
            await message.answer_photo(
                photo=user_dict[message.from_user.id]['photo_id'],
                caption=f'Имя: {user_dict[message.from_user.id]["name"]}\n'
                        f'Возраст: {user_dict[message.from_user.id]["age"]}\n'
                        f'Пол: {user_dict[message.from_user.id]["gender"]}\n'
                        f'Образование: {user_dict[message.from_user.id]["education"]}\n'
                        f'Получать новости: {user_dict[message.from_user.id]["wish_news"]}')
        else:
            # Если анкеты пользователя в базе нет - предлагаем заполнить
            await message.answer(text='Вы еще не заполняли анкету. '
                                      'Чтобы приступить - отправьте '
                                      'команду /fillform')

Данные, если они там есть, берутся из "базы данных", форматируются и отправляются пользователю в виде фото с подписью. Если данных нет - отправляется сообщение, что пользователь еще анкету не заполнял. Данный хэндлер **не** должен срабатывать **в любых состояниях**, кроме дефолтного, поэтому вешаем дополнительный фильтр `StateFilter(default_state)`.

![](https://ucarecdn.com/43e8401b-71cd-4a2b-b000-b8b34a00317c/-/preview/-/enhance/80/)

Ну, и последний хэндлер - это уже знакомое нам "эхо".

    # Этот хэндлер будет срабатывать на любые сообщения, кроме тех
    # для которых есть отдельные хэндлеры, вне состояний
    @dp.message(StateFilter(default_state))
    async def send_echo(message: Message):
        await message.reply(text='Извините, моя твоя не понимать')

Его задача обрабатывать те апдейты, для которых не нашлось других хэндлеров в состоянии "по умолчанию". Это просто "заглушка", чтобы бот не зависал, когда в чат приходит что-то, что он не знает как обработать.

Вот и все по коду. Запустите его и поиграйтесь с ним. Посмотрите как ведет себя бот в разных состояниях, когда вы пытаетесь отправить не то, что он ожидает.

Вот так и работает FSM. В целом, ничего сложного. В процессе взаимодействия с пользователем у бота могут быть какие-то конкретные состояния (например, состояние ожидания фото). Они могут быть изменены какими-то событиями (пользователь прислал фото и мы переводим его в состояние выбора получать или нет новости). В каждый конкретный момент состояние бота может быть только одно (состояние ожидания фото), но всего состояний может быть столько, сколько потребуется (ожидание фото, ожидание возраста, ожидание выбора пола и т.п.). Надеюсь, теперь смысл этой фразы стал понятнее :)