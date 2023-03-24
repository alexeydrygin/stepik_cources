## Модуль filters.py
-----------------

Для примера того, как можно пользоваться своими фильтрами и где они могут храниться в шаблоне - напишем отдельный модуль **filters.py**. Первый фильтр будет просто проверять `callback_data` у объекта `CallbackQuery` на то, что он состоит из цифр. Так мы будем понимать, что нажата кнопка с закладкой - номером страницы, на которую нужно перейти. А второй фильтр будет ловить `callback_data` от кнопок-закладок, которые нужно удалить в режиме редактирования закладок.

### filters.py

    from aiogram.filters import BaseFilter
    from aiogram.types import CallbackQuery
    
    
    class IsDigitCallbackData(BaseFilter):
        async def __call__(self, callback: CallbackQuery) -> bool:
            return isinstance(callback.data, str) and callback.data.isdigit()
    
    
    class IsDelBookmarkCallbackData(BaseFilter):
        async def __call__(self, callback: CallbackQuery) -> bool:
            return isinstance(callback.data, str) and 'del'         \
                in callback.data and callback.data[:-3].isdigit()

Фильтры записаны через классы, наследуемые от класса `BaseFilter`, c переопределенным методом `__call__`. Подробно принцип их работы я объяснял в уроке про [фильтры](https://stepik.org/lesson/891577/step/1?unit=896427).