## Что покажет программа, если запустить файл main.py?

### Структура проекта

    📁 Packs
     |_ main.py
     |_ 📁 pack_1
         |_ file_11.py
         |_ file_12.py

### main.py

    from pack_1.file_11 import func_1
    
    
    print(func_1(3))

### file\_11.py

    from .file_12 import a
    
    
    def func_1(n: int) -> int:
        return n * n
    
    
    print(a)

### file\_12.py

    from .file_11 import func_1
    
    
    a: int = 42
    
    print(func_1(a))

---

## Выберите один вариант из списка

- 42

   9

   1764

- Ошибка относительного импорта

- **Ошибка циклического импорта**

- 1764

   42

   9

- Ошибка: модуль не найден

- 9