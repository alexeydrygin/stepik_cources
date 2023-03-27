## Выберите варианты с кодом, который приведет к форматированию сообщения как на скриншоте:

![](https://ucarecdn.com/66e21a8d-c2fb-4796-a78a-bcde7ee5a20a/-/preview/-/enhance/77/)

1.      await bot.send_message(chat_id=chat_id,
                               text='___Пример форматированного текста_\r__',
                               parse_mode='HTML')
    
2.      bot: Bot = Bot(BOT_TOKEN, parse_mode='MarkdownV2')
        
        # ...
        
        await bot.send_message(chat_id=chat_id,
                               text='___Пример форматированного текста_\r__')
        
    
3.      await bot.send_message(chat_id=chat_id,
                               text='___Пример форматированного текста___',
                               parse_mode='MarkdownV2')
    
4.      await bot.send_message(chat_id=chat_id,
                               text='<i><u>Пример форматированного текста</i></u>',
                               parse_mode='HTML')
    
5.      bot: Bot = Bot(BOT_TOKEN, parse_mode='HTML')
        
        # ...
        
        await bot.send_message(chat_id=chat_id,
                               text='<i><u>Пример форматированного текста</u></i>')
    
6.      await bot.send_message(chat_id=chat_id,
                               text='<ins><i>Пример форматированного текста</i></ins>',
                               parse_mode='HTML')
    

**Примечание.** Очень желательно, чтобы вы не просто гадали, а брали, запускали этот код, и смотрели, что происходит. 

Еще раз скриншот форматированного текста для удобства:

![](https://ucarecdn.com/66e21a8d-c2fb-4796-a78a-bcde7ee5a20a/-/preview/-/enhance/77/)

**Чтобы решить это задание откройте [https://stepik.org/lesson/870035/step/5](https://stepik.org/lesson/870035/step/5)**



 1  
 **2**  
 3  
 4  
 **5**  
 **6**

