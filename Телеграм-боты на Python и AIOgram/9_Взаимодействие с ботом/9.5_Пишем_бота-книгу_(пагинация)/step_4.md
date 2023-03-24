## Файлы .env, .env.example, config.py и .gitignore
------------------------------------------------

Начнем с файла с секретами. Не забудьте вставить действующий токен вашего бота вместо недействующего моего.

### .env

    BOT_TOKEN=5424991242:AAGwomxQz1p46bRi_2m3V7kvJlt5RjK9xr0
    ADMIN_IDS=173901673

Как мы уже разбирали раньше - это текстовый файл с, так называемыми, переменными окружения. В нем мы будем хранить "секреты" нашего бота. В текущем проекте это будет только токен бота и id администратора бота. Правда, id нам в этом проекте тоже не понадобится, и здесь я его оставил лишь для того, чтобы еще раз продемонстрировать формат хранения переменных окружения. Если админов у бота несколько, то их можно записать через запятую:

    ADMIN_IDS=173901673,178876776,197177271

### .env.example

    BOT_TOKEN=5424991242:AAGwomxQz1p46bRi_2m3V7kvJlt5RjK9xr0
    ADMIN_IDS=173901673,178876776,197177271

С файлами **.env** и **.env.example** все понятно. Теперь **config.py**:

### config.py

    from dataclasses import dataclass
    
    from environs import Env
    
    
    @dataclass
    class TgBot:
        token: str            # Токен для доступа к телеграм-боту
        admin_ids: list[int]  # Список id администраторов бота
    
    
    @dataclass
    class Config:
        tg_bot: TgBot
    
    
    # Создаем функцию, которая будет читать файл .env и возвращать
    # экземпляр класса Config с заполненными полями token и admin_ids
    def load_config(path: str | None = None) -> Config:
        env = Env()
        env.read_env(path)
        return Config(tg_bot=TgBot(
                        token=env('BOT_TOKEN'),
                        admin_ids=list(map(int, env.list('ADMIN_IDS')))))

Файл **.gitignore** будет таким же простым, как и в проекте "Камень, ножницы, бумага" - только самое необходимое.

### .gitignore

    .env
    
    .mypy_cache/
    .vscode/
    venv/
    __pycache__/