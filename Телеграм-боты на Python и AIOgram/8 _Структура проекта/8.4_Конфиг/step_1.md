## Конфигурационный файл
---------------------

Мы с вами выяснили, что чувствительные данные, которые используются в проекте, лучше хранить в переменных окружения. А чтобы использовать их в наших проектах - будем их загружать через файл конфигурации бота `config.py`. В уроках про аннотацию типов я уже показывал как примерно может выглядеть конфигурационный файл проекта с использованием датаклассов.

### config.py

    from dataclasses import dataclass
    
    
    @dataclass
    class DatabaseConfig:
        database: str         # Название базы данных
        db_host: str          # URL-адрес базы данных
        db_user: str          # Username пользователя базы данных
        db_password: str      # Пароль к базе данных
        
    
    @dataclass
    class TgBot:
        token: str            # Токен для доступа к телеграм-боту
        admin_ids: list[int]  # Список id администраторов бота
    
    
    @dataclass
    class Config:
        tg_bot: TgBot
        db: DatabaseConfig

Сейчас в этом файле не хватает только кода, который будет создавать экземпляр класса `Config` с данными из переменных окружения. Исправим это. Пусть файл `.env`, для этого примера, лежит в той же директории, что и файл `config.py`.

### .env

    BOT_TOKEN=5424991242:AAGwomxQz1p46bRi_2m3V7kvJlt5RjK9xr0
    ADMIN_IDS=173901673,124543434,143343455
    
    DATABASE=someDatabaseName
    DB_HOST=127.0.0.1
    DB_USER=dbUser
    DB_PASSWORD=dbPassword

### config.py

    from dataclasses import dataclass
    from environs import Env
    
    
    @dataclass
    class DatabaseConfig:
        database: str         # Название базы данных
        db_host: str          # URL-адрес базы данных
        db_user: str          # Username пользователя базы данных
        db_password: str      # Пароль к базе данных
    
    
    @dataclass
    class TgBot:
        token: str            # Токен для доступа к телеграм-боту
        admin_ids: list[int]  # Список id администраторов бота
    
    
    @dataclass
    class Config:
        tg_bot: TgBot
        db: DatabaseConfig
    
    
    # Создаем экземпляр класса Env
    env: Env = Env()
    
    # Добавляем в переменные окружения данные, прочитанные из файла .env 
    env.read_env()
    
    # Создаем экземпляр класса Config и наполняем его данными из переменных окружения
    config = Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                                 admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                    db=DatabaseConfig(database=env('DATABASE'),
                                      db_host=env('DB_HOST'),
                                      db_user=env('DB_USER'),
                                      db_password=env('DB_PASSWORD')))
    
    
    # Выводим значения полей экземпляра класса Config на печать, 
    # чтобы убедиться, что все данные, получаемые из переменных окружения, доступны
    print('BOT_TOKEN:', config.tg_bot.token)
    print('ADMIN_IDS:', config.tg_bot.admin_ids)
    print()
    print('DATABASE:', config.db.database)
    print('DB_HOST:', config.db.db_host)
    print('DB_USER:', config.db.db_user)
    print('DB_PASSWORD:', config.db.db_password)

 Если теперь запустить файл `config.py` в терминале получим результат:

    BOT_TOKEN: 5424991242:AAGwomxQz1p46bRi_2m3V7kvJlt5RjK9xr0
    ADMIN_IDS: [173901673, 124543434, 143343455]
    
    DATABASE: someDatabaseName
    DB_HOST: 127.0.0.1
    DB_USER: dbUser
    DB_PASSWORD: dbPassword

А, значит, все работает, как задумано.