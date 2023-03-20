## Какой код, из примеров ниже, позволит создать такую клавиатуру с обычными кнопками?

![](https://ucarecdn.com/b9c7968c-c6be-4e49-bac5-228f4dc1ed59/-/preview/-/enhance/85/)

**Примечание.** Очень желательно, чтобы вы не просто гадали, а брали, запускали этот код, и смотрели, что происходит.

1.      # Создаем список списков с кнопками
        keyboard: list[list[KeyboardButton]] = [
            [KeyboardButton(text=str(i)) for i in range(1, 4)],
            [KeyboardButton(text=str(i)) for i in range(4, 7)]]
        
        keyboard.append(KeyboardButton(text='7'))
        
        # Создаем объект клавиатуры, добавляя в него кнопки
        my_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True)
    
2.      # Создаем список списков с кнопками
        keyboard: list[KeyboardButton] = [
            KeyboardButton(text=str(i)) for i in range(1, 8)]
        
        # Инициализируем билдер
        builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
        
        builder.row(*keyboard)
        
        # Создаем объект клавиатуры, добавляя в него кнопки
        my_keyboard: ReplyKeyboardMarkup = builder.as_markup(resize_keyboard=True)
    
3.      # Создаем список списков с кнопками
        keyboard: list[list[KeyboardButton]] = [[KeyboardButton(
            text=str(i)) for i in range(1, 8)]]
        
        # Создаем объект клавиатуры, добавляя в него кнопки
        my_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True)
    
4.      # Создаем список списков с кнопками
        keyboard: list[KeyboardButton] = [
            KeyboardButton(text=str(i)) for i in range(1, 8)]
        
        # Инициализируем билдер
        builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()
        
        # Добавляем кнопки в билдер
        builder.row(*keyboard, width=3)
        
        # Создаем объект клавиатуры, добавляя в него кнопки
        my_keyboard: ReplyKeyboardMarkup = builder.as_markup(resize_keyboard=True)
    
5.      # Создаем список списков с кнопками
        keyboard: list[list[KeyboardButton]] = [
            [KeyboardButton(text=str(i)) for i in range(1, 4)],
            [KeyboardButton(text=str(i)) for i in range(4, 7)],
            [KeyboardButton(text=str(i)) for i in range(7, 9)]]
        
        # Создаем объект клавиатуры, добавляя в него кнопки
        my_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True)
    
6.      # Создаем список списков с кнопками
        keyboard: list[list[KeyboardButton]] = [
            [KeyboardButton(text=str(i)) for i in range(1, 4)],
            [KeyboardButton(text=str(i)) for i in range(4, 7)]]
        
        keyboard.append([KeyboardButton(text='7')])
        
        # Создаем объект клавиатуры, добавляя в него кнопки
        my_keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True)
    

Еще раз клавиатура, которая должна получиться:

![](https://ucarecdn.com/b9c7968c-c6be-4e49-bac5-228f4dc1ed59/-/preview/-/enhance/85/)

---

Выберите все подходящие ответы из списка


- 1

- 2

- 3

- **4**--

- 5

- **6**--