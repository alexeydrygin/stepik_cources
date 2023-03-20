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

    from file_12 import a
    
    
    def func_1(n: int) -> int:
        return n * n
    
    
    print(a)

### file\_12.py

    a: int = 42

---
Выберите один вариант из списка

- Ошибка циклического импорта

- 9

  42

- **Ошибка: модуль не найден**

- 42

  9

- 9

- Ошибка относительного импорта