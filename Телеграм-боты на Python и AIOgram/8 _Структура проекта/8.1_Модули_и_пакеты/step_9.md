## Запуск модуля как исполняемого файла
------------------------------------

Довольно часто бывает необходимость запустить какой-нибудь модуль, внутри проекта, как исполняемый файл. Например, чтобы протестировать его работу. И если в этом модуле прописаны относительные импорты, то, как мы выяснили на предыдущих шагах, мы будем получать ошибки импорта. Это еще одна причина не использовать относительные импорты без крайней необходимости.

Кроме того, даже если внутри модуля, который нужно запустить на исполнение, прописаны только абсолютные импорты, он все равно может не запускаться, потому что пути поиска модулей строятся от файла `__main__`, а любой питоновский модуль, который мы запускаем на исполнение, автоматически получает это имя и, соответственно, те абсолютные пути, которые работали для файла с точкой входа в проект, теперь не работают для модуля.

Как обычно, давайте смотреть на конкретном примере. Возьмем простую файловую структуру проекта.

    📁 Packs
     |_ main.py
     |_ 📁 pack_1
         |_ file_11.py
         |_ file_12.py

И пусть мы хотим протестировать работу какой-нибудь функции в модуле `file_12.py`. 

### main.py

    from pack_1.file_11 import func_1
    from pack_1.file_12 import a
    
    
    print(func_1(a))

### file\_11.py

    a: int = 42
    
    
    def func_1(n: int) -> int:
        return n * n

### file\_12.py

    from pack_1.file_11 import a
    
    
    print(a)
    
    
    def func_2(n: int) -> int:
        return n + n
    
    
    print(func_2(a))

Сначала запустим `main.py` и убедимся, что все работает. В терминале ожидаемый вывод:

    42
    84
    1764

Но если мы запустим на исполнение модуль `file_12.py`, то получим ошибку:

    from pack_1.file_11 import a
    ModuleNotFoundError: No module named 'pack_1'

То есть модуль `file_12.py` не знает, где искать pack\_1, потому что в его путях такого нет. Давайте в этом убедимся. Для этого добавим вывод путей в модуль `file_12.py`. А еще воспользуемся функцией `pprint` из библиотеки `pprint`, чтобы получить пути в более читаемом формате.

### file\_12.py

    import sys
    from pprint import pprint
    
    
    pprint(sys.path)
    
    
    from pack_1.file_11 import a
    
    
    print(a)
    
    
    def func_2(n: int) -> int:
        return n + n
    
    
    print(func_2(a))

Запустим модуль. Прежде чем программа упадет с ошибкой будут напечатаны пути, где интерпретатор ищет модули и пакеты:

    ['/<здесь_путь_до_проекта>/pack_1',
     '/usr/local/Cellar/python@3.10/3.10.8/Frameworks/Python.framework/Versions/3.10/lib/python310.zip',
     '/usr/local/Cellar/python@3.10/3.10.8/Frameworks/Python.framework/Versions/3.10/lib/python3.10',
     '/usr/local/Cellar/python@3.10/3.10.8/Frameworks/Python.framework/Versions/3.10/lib/python3.10/lib-dynload',
     '/usr/local/lib/python3.10/site-packages']

В первом элементе списка с путями видим путь, который заканчивается папкой pack\_1, соответственно, и модули ищутся внутри этой папки. А вот этот импорт в модуле `file_12.py` - `from pack_1.file_11 import a` подразумевает, что мы находимся на одном уровне с папкой `pack_1`, а не внутри нее, поэтому и возникает ошибка импорта. У нас просто нет нужного пути в путях, доступных интерпретатору.

Логичным выходом из ситуации кажется добавление такого пути. Это довольно костыльное решение, но оно работает, когда модуль нужно протестировать отдельно от всего проекта. Добавим в переменную `sys.path` путь с уровнем выше. Надеюсь, вы имеете хотя бы поверхностное представление о библиотеке `os`. Но если, вдруг, не все поймете - пишите, расскажу более подробно, что мы делаем.

### file\_12.py

    import sys
    import os
    from pprint import pprint
    
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
    pprint(sys.path)
    
    
    from pack_1.file_11 import a
    
    
    print(a)
    
    
    def func_2(n: int) -> int:
        return n + n
    
    
    print(func_2(a))

Запустим `file_12.py`

    ['/<здесь_путь_до_проекта>/pack_1/..',
     '/<здесь_путь_до_проекта>/pack_1',
     '/usr/local/Cellar/python@3.10/3.10.8/Frameworks/Python.framework/Versions/3.10/lib/python310.zip',
     '/usr/local/Cellar/python@3.10/3.10.8/Frameworks/Python.framework/Versions/3.10/lib/python3.10',
     '/usr/local/Cellar/python@3.10/3.10.8/Frameworks/Python.framework/Versions/3.10/lib/python3.10/lib-dynload',
     '/usr/local/lib/python3.10/site-packages']
    42
    84

Все работает! Отлично! А работает потому, что в `sys.path` появился путь `/<здесь_путь_до_проекта>/pack_1/..`, в котором две точки (`..`) говорят интерпретатору искать на один уровень выше, чем директория, в которой находится исполняемый модуль, которым сейчас является `file_12.py`. Это как, когда мы набираем в командной строке `cd ..` и поднимаемся на уровень выше по пути, из которого вызываем эту команду.

_**Семь бед - один ответ - костыль и велосипед!**_ (с)