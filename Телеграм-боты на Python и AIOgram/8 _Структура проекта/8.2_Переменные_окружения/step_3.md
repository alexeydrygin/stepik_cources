## Библиотека environs
-------------------

Получать значения переменных окружения через `os.getenv('<имя_переменной>')` может быть не так удобно, как с помощью библиотеки `environs`, которая содержит класс `Env` с разными методами, упрощающими работу с переменными окружения. Библиотекой `environs` мы и будем, в основном, пользоваться, разрабатывая наших ботов. Она не входит в стандартные библиотеки, поэтому тоже требует отдельной установки. 

    pip install environs

Ну, и конкретный пример, как мы любим :)

### .env

    BOT_TOKEN=5424991242:AAGwomxQz1p46bRi_2m3V7kvJlt5RjK9xr0
    ADMIN_ID=173901673

### main.py

    from environs import Env
    
    
    env = Env()              # Создаем экземпляр класса Env
    env.read_env()           # Методом read_env() читаем файл .env и загружаем из него переменные в окружение 
                              
    bot_token = env('BOT_TOKEN')     # Сохраняем значение переменной окружения в переменную bot_token
    admin_id = env.int('ADMIN_ID')   # Преобразуем значение переменной окружения к типу int 
                                     # и сохраняем в переменной admin_id
    
    print(bot_token)
    print(admin_id)

Запуск файла `main.py` выводит:

    5424991242:AAGwomxQz1p46bRi_2m3V7kvJlt5RjK9xr0
    173901673