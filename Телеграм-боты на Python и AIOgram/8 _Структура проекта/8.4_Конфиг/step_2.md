## config.py
---------

На предыдущем шаге мы научились создавать экземпляр класса `Config` и наполнять его данными из переменных окружения. В принципе, в рабочем проекте бота, можно оставить все так, потому что при импорте экземпляра класса `Config` из модуля `config.py` в точку входа - весь код этого модуля все равно выполнится и данные будут доступны. Но хорошей практикой считается все-таки выполнять код не в модуле, а там, где его выполнение реально требуется, то есть в нашем случае, если обратиться к шаблону проекта, в исполняемом файле `bot.py`. А в модуле `config.py` организовать в виде функции наполнение экземпляра класса `Config` данными из переменных окружения. В `bot.py`, соответственно, импортировать эту функцию и вызвать ее, передав в качестве параметра путь к файлу `.env`.

Если не очень понятно, попробую еще раз. В модуле `config.py` создаем функцию, которая в качестве аргумента принимает путь до файла `.env`, из которого загружаются переменные окружения для работы бота, а возвращает функция экземпляр класса `Config` с уже заполненными данными, которые мы будем использовать в исполняемом файле `bot.py` при инициализации нашего бота. Вот так будет выглядеть функция:

    def load_config(path: str | None) -> Config:
    
        env: Env = Env()
        env.read_env(path)
    
        return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                                   admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                      db=DatabaseConfig(database=env('DATABASE'),
                                        db_host=env('DB_HOST'),
                                        db_user=env('DB_USER'),
                                        db_password=env('DB_PASSWORD')))

Ну, а весь файл `config.py` может быть примерно таким:

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
    
    
    def load_config(path: str | None) -> Config:
    
        env: Env = Env()
        env.read_env(path)
    
        return Config(tg_bot=TgBot(token=env('BOT_TOKEN'),
                                   admin_ids=list(map(int, env.list('ADMIN_IDS')))),
                      db=DatabaseConfig(database=env('DATABASE'),
                                        db_host=env('DB_HOST'),
                                        db_user=env('DB_USER'),
                                        db_password=env('DB_PASSWORD')))

Теперь в исполняемом модуле `bot.py` мы можем создать экземпляр класса `Config` и использовать данные из него.

### bot.py

    # ...
    
    from config_data.config import load_config
    
    
    config = load_config('<путь к файлу .env>')
    
    # ...

И уже переменную `config` используем там, где нужно подставить какие-либо данные в процессе инициализации бота, подключения к базе данных и так далее.

    # ...
    
    bot_token = config.tg_bot.token           # Сохраняем токен в переменную bot_token
    superadmin = config.tg_bot.admin_ids[0]   # Сохраняем ID админа в переменную superadmin
    
    # ...