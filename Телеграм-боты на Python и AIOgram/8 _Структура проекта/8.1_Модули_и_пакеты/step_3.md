## Некоторые нюансы о модулях
--------------------------

### 1\. Поиск модулей интерпретатором Python

Иногда, в процессе освоения модульного разделения кода, возникает вопрос: "_**А ведь часто в своих программах мы импортируем сторонние модули, которые не лежат в одной директории с исполняемым файлом, откуда Python знает, где эти модули искать и где они вообще хранятся?**_" 

О том где искать модули Python знает, потому что так спроектирован :)

В первую очередь интерпретатор ищет модули среди встроенных модулей. Тех, которые непосредственно встроены в сам интерпретатор. Их список можно посмотреть так:

    import sys
    
    print(sys.builtin_module_names)

Например, установленный у меня Python 3.10.4 выдает такой список (формально, не список, а кортеж,  конечно, но я имею в виду здесь список не как структуру данных, а как перечень):

    ('_abc', '_ast', '_codecs', '_collections', '_functools', '_imp', '_io', '_locale', '_operator', '_signal', '_sre', '_stat', '_string', '_symtable', '_thread', '_tracemalloc', '_warnings', '_weakref', 'atexit', 'builtins', 'errno', 'faulthandler', 'gc', 'itertools', 'marshal', 'posix', 'pwd', 'sys', 'time', 'xxsubtype')

Список, как вы можете заметить, не очень большой, гораздо меньший, чем предоставляет нам стандартная библиотека Python. Если вы случайно назвали свой модуль также, как один из встроенных модулей, то импортируется встроенный модуль, а не ваш, т.к. сначала поиск ведется, как уже сказано выше, среди встроенных модулей.

Далее интерпретатор ищет модули в той же директории, что и исполняемый файл.

Потом, если Python не нашел импортируемый модуль в том же каталоге, где лежит исполняемый файл, он обращается к путям из переменной окружения `PYTHONPATH`, если такая переменная установлена в вашей системе.

Если предыдущие пути поиска не сработали, интерпретатор обращается к стандартной библиотеке. Поэтому, если ваш модуль, находящийся в корне или в одном из путей `PYTHONPATH`, вдруг, называется также как модули из стандартной библиотеки или как сторонние установленные модули, доступен будет именно ваш.

Посмотреть модули стандартной библиотеки можно так:

    import sys
    
    print(sys.stdlib_module_names)

Для Python 3.10.8 результат такой:

    frozenset({'zlib', 'nntplib', 'time', 'argparse', 'trace', 'math', '_codecs_hk', 'heapq', '_heapq', 'os', 'ssl', 'pwd', 'plistlib', 'enum', 'telnetlib', 'ctypes', 'struct', '__future__', '_crypt', '_blake2', 'json', '_codecs', 'sre_parse', 'difflib', '_sha256', 'sysconfig', 'contextlib', 'genericpath', 'socketserver', 'tempfile', '_weakref', 'contextvars', 'rlcompleter', 'linecache', '_pydecimal', 'pickle', '_curses', '_uuid', 'cgitb', 'colorsys', 'getopt', 'concurrent', 'pydoc', 'subprocess', 'distutils', '_bz2', '_multibytecodec', '_sre', '_stat', 'imp', 'keyword', '_datetime', 'bisect', 'idlelib', 'pickletools', 'queue', 'secrets', 'shelve', 'errno', 'sqlite3', 'turtle', 'msvcrt', '_functools', '_codecs_kr', '_contextvars', 'ensurepip', '_codecs_iso2022', '_strptime', 'calendar', 'copy', 'threading', 'inspect', 'importlib', 'tarfile', 'sched', 'sre_constants', 'mailcap', 'urllib', 'asyncio', 'signal', 'pty', '_compression', 'antigravity', 'resource', '_string', '_collections_abc', '_csv', 'io', '_ssl', 'fnmatch', 'imaplib', 'tracemalloc', 'zoneinfo', 'dis', '_pickle', '_thread', 'tokenize', 'code', '_dbm', 'quopri', 'atexit', 'html', 'functools', 'wave', 'reprlib', 'readline', 'runpy', 'ipaddress', '_elementtree', 'py_compile', '_lzma', 'bz2', '_sha1', 'gettext', '_queue', 'nis', 'operator', 'timeit', 'fcntl', '_winapi', 'mmap', 'textwrap', 'fileinput', 'asyncore', 'pathlib', '_frozen_importlib', 'array', '_ast', 'bdb', 'binhex', 'posix', '_locale', 'uu', '_operator', 'statistics', '_osx_support', '_statistics', 'unicodedata', 'tkinter', 'warnings', 'wsgiref', 'asynchat', '_sitebuiltins', '_posixsubprocess', 'hmac', 'lib2to3', 'sre_compile', 'types', 'sndhdr', '_frozen_importlib_external', '_lsprof', 'pyclbr', 'termios', 'zipapp', '_imp', '_io', 'selectors', 'crypt', '_bisect', 'gc', 'graphlib', 'unittest', 'optparse', '_asyncio', 'base64', 'copyreg', 'multiprocessing', 'netrc', 'configparser', 'filecmp', 'curses', 'shlex', 'this', '_overlapped', '_struct', '_codecs_cn', 'glob', 'mimetypes', 'string', '_pyio', 'fractions', 'traceback', '_tracemalloc', 'cgi', 'csv', 'spwd', 'tabnanny', 'posixpath', 'cProfile', '_codecs_jp', '_gdbm', 'smtpd', 'nturl2path', 'sunau', 'pprint', 'numbers', 'xml', '_compat_pickle', 'locale', '_opcode', 'datetime', 'dataclasses', 'token', '_decimal', 'opcode', 'marshal', 'venv', 'cmd', '_sha512', '_hashlib', 'hashlib', 'msilib', 'ossaudiodev', '_ctypes', 'socket', 'zipfile', '_zoneinfo', 're', 'profile', 'sys', '_sqlite3', '_collections', 'select', 'doctest', 'abc', 'tty', 'aifc', '_scproxy', 'syslog', 'compileall', '_random', 'xdrlib', 'pydoc_data', 'codeop', 'itertools', 'binascii', 'lzma', 'mailbox', 'pyexpat', '_abc', '_symtable', 'pkgutil', '_md5', '_signal', 'pdb', 'turtledemo', '_aix_support', '_sha3', 'ntpath', 'getpass', 'http', 'weakref', 'cmath', 'poplib', 'random', '_posixshmem', 'nt', 'chunk', 'zipimport', 'shutil', '_markupbase', '_msi', 'encodings', 'imghdr', '_weakrefset', 'dbm', 'winreg', 'stat', 'uuid', '_tkinter', 'faulthandler', 'grp', '_multiprocessing', '_py_abc', 'pstats', '_threading_local', 'pipes', '_codecs_tw', 'ftplib', 'platform', 'typing', 'webbrowser', 'gzip', 'site', 'builtins', 'collections', 'smtplib', 'winsound', 'xmlrpc', '_json', 'audioop', '_bootsubprocess', 'decimal', 'logging', 'symtable', '_warnings', 'ast', 'codecs', 'modulefinder', '_socket', '_curses_panel', 'email', 'stringprep'})

 И в самую последнюю очередь Python будет искать модули среди установленных сторонних библиотек - в папке `site-packages`. В эту папку по умолчанию устанавливаются модули и пакеты, не входящие в стандартную библиотеку. Когда мы устанавливали `aiogram` - он был установлен именно в `site-packages`.

Вообще, все пути, в которых Python будет искать модули (кроме встроенных), можно посмотреть так:

    import sys
    
    print(sys.path)

### 2\. Однократное подключение модулей

Другой нюанс. Модули подключаются в исполняемый файл один раз, даже если импорт в коде прописан дважды, трижды и т.д. Интерпретатор загружает модуль в кэш и, в процессе работы программы, обращается к кэшу. Если же для какой-то необходимости все-таки требуется загрузить модуль еще раз - для этого можно воспользоваться функцией `reload` из библиотеки `importlib`. Но лично я на практике с такой необходимостью не сталкивался и, в каких случаях такое может понадобиться, представляю очень смутно.

### 3\. Поиск не только модулей, но и пакетов

Немного забегая вперед надо отметить, что по указанному маршруту интерпретатор будет искать не только модули, но и пакеты. А в чем разница между ними - поговорим дальше.