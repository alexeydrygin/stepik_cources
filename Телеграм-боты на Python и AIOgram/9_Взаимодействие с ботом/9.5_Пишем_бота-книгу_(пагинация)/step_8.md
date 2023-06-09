## Вспомогательная функция \_get\_part\_text()
-------------------------------------------

Перед тем, как отправлять пользователям в чат страницы книги, нужно привести текст книги к удобному для работы формату. Мы будем хранить страницы книги в словаре, где ключом будет номер страницы, а значением - строка с текстом этой страницы, как показано на предыдущем шаге. И прежде, чем написать основную функцию, которая подготовит такой словарь из текстового файла, нам потребуется написать вспомогательную функцию `_get_part_text()`, которая будет получать на вход текст из файла, указатель на начало страницы в тексте и максимальный размер страницы, которую нужно вернуть. А возвращать функция должна текст страницы и ее размер (в символах). При этом, получившаяся страница, обязательно должна заканчиваться на какой-нибудь знак препинания, чтобы текст страницы не обрывался на полуслове.

Реализуйте функцию `_get_part_text()`, которая принимает три аргумента в следующем порядке:

*   `text` - строка с полным текстом, из которого нужно получить страницу не больше заданного размера
*   `start` - номер первого символа в тексте, с которого должна начинаться страница (нумерация идет с нуля)
*   `page_size` - максимальный размер страницы, которая должна получиться на выходе

Функция должна вернуть текст страницы (тип `str`) и ее получившийся размер в символах (тип `int`).

Список знаков препинания, которые могут быть окончанием текста страницы, состоит из знаков:

*   `,` - запятая
*   `.` - точка
*   `!` - восклицательный знак
*   `:` - двоеточие
*   `;` - точка с запятой
*   `?` - вопросительный знак

**Примечание 1.** Гарантируется, что подаваемый в функцию текст, не пустой, а в тексте страницы обязательно встретятся знаки препинания из списка выше

**Примечание 2.** Также гарантируется, что стартовый символ будет меньше, чем длина подаваемого в функцию текста.

**Примечание 3.** Если в тексте встречается многоточие - оно либо целиком должно попасть в текущую страницу, либо не попасть в страницу вообще. Нельзя разорвать многоточие, потому что следующая страница книги тогда начнется с точки/точек, что для пользователя будет смотреться, как неправильное форматирование текста.

**Примечание 4.** Обрезать невидимые символы (перенос строки, пробел и т.п.), получившиеся слева от текста, не надо. Мы это будем делать внутри следующей функции.

**Примечание 5.** В тестирующую систему сдайте программу, содержащую только необходимую функцию `_get_part_text()`, но не код, вызывающий ее.


---
```python
import re


def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]:
    edit_text = re.sub(r'[.,!?:;]\.+$', '', text[start:start+size])
    edit_text = re.findall(r'(?s).+[.,!?:;]', edit_text)
    return *edit_text, len(*edit_text)



#3 of 9. Wrong answer
#Test input:
text = '— Я всё очень тщательно проверил, — сказал компьютер, — и со всей определённостью заявляю, что это и есть ответ. Мне кажется, если уж быть с вами абсолютно честным, то всё дело в том, что вы сами не знали, в чём вопрос.'
print(*_get_part_text(text, 54, 70), sep='\n')
# Correct output:
# — и со всей определённостью заявляю, что это и есть ответ.
# 58

#2 of 3.
#Test input:
text = 'Да? Вы точно уверены? Может быть, вам это показалось?.. Ну, хорошо, приходите завтра, тогда и посмотрим, что можно сделать. И никаких возражений! Завтра, значит, завтра!'
print(*_get_part_text(text, 22, 145), sep='\n')
# Correct output:
# Может быть, вам это показалось?.. Ну, хорошо, приходите завтра, тогда и посмотрим, что можно сделать. И никаких возражений! Завтра, значит,
# 139

#3 of 3.
#Test input:
text = 'Да? Вы точно уверены? Может быть, вам это показалось?.. Ну, хорошо, приходите завтра, тогда и посмотрим, что можно сделать. И никаких возражений! Завтра, значит, завтра!'
print(*_get_part_text(text, 0, 54), sep='\n')
# Correct output:
# Да? Вы точно уверены? Может быть,
# 33
```

Данный код определяет функцию _get_part_text, которая принимает на вход три аргумента: строку text, целочисленное значение start и целочисленное значение size, и возвращает кортеж, содержащий два элемента: отредактированный текст и его длину.

import re - импортирование модуля re для работы с регулярными выражениями.

def _get_part_text(text: str, start: int, size: int) -> tuple[str, int]: - определение функции _get_part_text, которая принимает на вход три аргумента: строку text, целочисленное значение start и целочисленное значение size, и возвращает кортеж, содержащий два элемента: отредактированный текст и его длину.

edit_text = re.sub(r'[.,!?:;]\.+$', '', text[start:start+size]) - отредактирование строки text таким образом, чтобы она начиналась с символа с индексом start и имела длину size, а затем удаление точек и других знаков препинания, следующих непосредственно за другим знаком препинания.

edit_text = re.findall(r'(?s).+[.,!?:;]', edit_text) - поиск в строке edit_text любых символов, за которыми следует знак препинания, и сохранение всех найденных подстрок в edit_text. Флаг (?s) означает, что точка в регулярном выражении должна совпадать с любым символом, включая символ перевода строки.

return *edit_text, len(*edit_text) - возврат кортежа, содержащего все подстроки, найденные в строке edit_text, и длина текста