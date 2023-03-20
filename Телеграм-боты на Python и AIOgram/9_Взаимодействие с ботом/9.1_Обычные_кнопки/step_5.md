## Специальные обычные кнопки
--------------------------

Существует 6 типов специальных обычных кнопок:

*   Для отправки своего телефона (параметр `request_contact`)
*   Для отправки своей геопозиции (параметр `request_location`)
*   Для создания опроса/викторины (параметр `request_poll`)
*   Для запуска Web-приложений прямо в Телеграм (параметр `web_app`)
*   (параметр `request_user`)
*   (параметр `request_chat`)

Параметры `request_user` и `request_chat` сейчас рассматривать не будем, они появились буквально пару недель назад (на момент правки этого шага) и я еще не успел с ними разобраться. Остановимся на остальных четырех.

Создаются кнопки этих типов точно также, как и обычные кнопки-шаблоны, только с дополнительными аргументами. Для отправки телефона - `request_contact=True`, для отправки геопозиции - `request_location=True`, для создания викторины - `request_poll=KeyboardButtonPollType()`, а для запуска Web-приложения - `web_app=WebAppInfo()`. Сначала давайте рассмотрим как работают первые три типа, а web\_app рассмотрим отдельно, потому что это целый отдельный новый мир. Итак, отправка контактных данных, геопозиции и создание опросов/викторин:

    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
    from aiogram.utils.keyboard import ReplyKeyboardBuilder
    
    
    # Инициализируем билдер
    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    
    # Создаем кнопки
    contact_btn: KeyboardButton = KeyboardButton(
                                    text='Отправить телефон',
                                    request_contact=True)
    geo_btn: KeyboardButton = KeyboardButton(
                                    text='Отправить геолокацию',
                                    request_location=True)
    poll_btn: KeyboardButton = KeyboardButton(
                                    text='Создать опрос/викторину',
                                    request_poll=KeyboardButtonPollType())
    
    # Добавляем кнопки в билдер
    kb_builder.row(contact_btn, geo_btn, poll_btn, width=1)
    
    # Создаем объект клавиатуры
    keyboard: ReplyKeyboardMarkup = kb_builder.as_markup(
                                        resize_keyboard=True,
                                        one_time_keyboard=True)
    
    
    # Этот хэндлер будет срабатывать на команду "/start"
    @dp.message(CommandStart())
    async def process_start_command(message: Message):
        await message.answer(text='Экспериментируем со специальными кнопками',
                             reply_markup=keyboard)

Результат:

![](https://ucarecdn.com/2e5dc51f-55da-459f-9297-068f75e7b259/-/preview/-/enhance/82/)

Если нажать на кнопку "Отправить телефон" - Телеграм спросит у вас подтверждения.

![](https://ucarecdn.com/78db8b66-2a5a-44dd-9908-2670347a46cc/)

В случае вашего согласия - отправит ваши контактные данные в чат:

![](https://ucarecdn.com/b5709b5e-129c-4f1c-b857-619bc426594a/-/preview/-/enhance/87/)

С геолокацией такая же история

![](https://ucarecdn.com/43dde95b-0fa5-46e8-ad5c-c5d5e353388c/-/preview/-/enhance/78/)

Скриншот геолокации прикладывать не буду, думаю, итак все понятно. Осталось разобраться с викторинами/опросами. При нажатии на соответствующую кнопку, появляется окно для создания опроса/викторины

![](https://ucarecdn.com/f9f9c0c2-3a88-48dd-b4fa-af536c190913/-/preview/-/enhance/80/)

Можно конкретизировать, что именно (опрос или викторина) будет создаваться по кнопке, если в `KeyboardButtonPollType` передать соответствующий тип:

*   `type='quiz'` - викторина
    
*   `type='regular'` - опрос
    

    # Создаем кнопки
    poll_btn_2: KeyboardButton = KeyboardButton(
                                    text='Создать опрос',
                                    request_poll=KeyboardButtonPollType(
                                                            type='regular'))
    
    quiz_btn: KeyboardButton = KeyboardButton(
                                    text='Создать викторину',
                                    request_poll=KeyboardButtonPollType(
                                                            type='quiz'))
    
    # Инициализируем билдер
    poll_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
    
    # Добавляем кнопки в билдер
    poll_kb_builder.row(poll_btn_2, quiz_btn, width=1)
    
    # Создаем объект клавиатуры
    poll_keyboard: ReplyKeyboardMarkup = poll_kb_builder.as_markup(
                                            resize_keyboard=True)
    
    
    # Этот хэндлер будет срабатывать на команду "/poll"
    @dp.message(Command(commands='poll'))
    async def process_poll_command(message: Message):
        await message.answer(text='Экспериментируем с кнопками опрос/викторина',
                             reply_markup=poll_keyboard)

Результат:

![](https://ucarecdn.com/1c632b4d-40c6-4f63-8223-cc299c45b465/-/preview/-/enhance/75/)

В первом случае будет недоступен режим викторины:

![](https://ucarecdn.com/996cadf9-3deb-49bd-b871-29411e0c4f8c/-/preview/-/enhance/84/)

А во втором наоборот - будет недоступен режим опроса:

![](https://ucarecdn.com/b549a966-7252-4973-9a68-936fcdfe717b/-/preview/-/enhance/85/)

И немного давайте поговорим про Telegram Web Apps. В 2022-м году в Телеграм появилась возможность запускать веб-приложения прямо внутри самого Телеграм. По задумке они открываются в отдельном окне и должны сильно расширять возможности телеграм-ботов. У Телеграм есть, по этому поводу, красочная презенташка [@DurgerKingBot](https://t.me/durgerkingbot). Сейчас мы не будем углубляться в то, как там все устроено, просто посмотрим как открывается отдельное окно при нажатии на специальную обычную кнопку.

    from aiogram.types.web_app_info import WebAppInfo
    
    
    # Создаем кнопку
    web_app_btn: KeyboardButton = KeyboardButton(
                                    text='Start Web App',
                                    web_app=WebAppInfo(url="https://stepik.org/"))
    
    # Создаем объект клавиатуры
    web_app_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                                keyboard=[[web_app_btn]],
                                                resize_keyboard=True)
    
    
    # Этот хэндлер будет срабатывать на команду "/web_app"
    @dp.message(Command(commands='web_app'))
    async def process_web_app_command(message: Message):
        await message.answer(text='Экспериментируем со специальными кнопками',
                             reply_markup=web_app_keyboard)

![](https://ucarecdn.com/d0b4caf3-9289-42af-9f6b-7ef0c38412bf/-/preview/-/enhance/82/)

![](https://ucarecdn.com/49a11d08-fbb6-4ebc-abd7-59ecf73975a9/-/preview/-/enhance/81/)

Web-приложения открываются только по защищенному протоколу (https). Как я уже сказал Web Apps - это отдельная большая тема, позволяющая с помощью инструментов фронтенда (базово HTML, CSS и JavaScript) создавать приложения для Телеграм с гораздо более разнообразным интерфейсом.

**Примечание.** Код к этому и остальным урокам доступен на GitHub по [ссылке](https://github.com/kmsint/aiogram3_stepik_course).