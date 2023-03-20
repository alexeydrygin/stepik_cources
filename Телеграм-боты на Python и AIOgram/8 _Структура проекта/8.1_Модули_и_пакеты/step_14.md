## Что покажет программа, если запустить файл main.py?

### Структура проекта

    📁 Packs
     |_ main.py
     |_ 📁 pack_1
         |_ __init__.py
         |_ file_11.py
         |_ file_12.py

### main.py

    import pack_1
    
    
    print(pack_1.func_1(3))

### file\_11.py

    from .file_12 import a
    
    
    def func_1(n: int) -> int:
        return n * n
    
    
    print(a)

### file\_12.py

    a: int = 42

### \_\_init\_\_.py

    from .file_11 import *
    from .file_12 import *

---

Выберите один вариант из списка


- **42**

   **9**

- 42

- Ошибка относительного импорта

- Ошибка циклического импорта

- 9

   42

- Ошибка: модуль не найден