## Обновление и перезапуск бота
----------------------------

Вот, наконец, мы с вами переселили бота в отдельное жилище. Надеюсь, ему там хорошо :) Но что если мы захотели как-то его переделать?

Если проект живой, то, скорее всего, его нужно будет обновлять. Очень редко бывает так, что бот просто работает, и при этом не требует никаких дополнительных улучшений или исправлений неожиданных багов. Да и вообще, если применять подход - сначала запускаем сервис "на коленке", а потом, если он оказывается востребованным, доводим "до ума", он изначально подразумевает, что вы его будете дописывать/переписывать.

Вообще, думаю, из предыдущих шагов уже понятно как происходит обновление и перезапуск бота, живущего на сервере, но для полноты картины, привожу последовательность действий в отдельном шаге, чтобы можно было обратиться, если нужна возможность куда-то быстро подсмотреть.

1.  Вносим какие-то изменения в проект, проверяем, что все работает (как правило это происходит на локальной машине, где вы ведете разработку) - коммитим и пушим на GitHub.
2.  Запускаем терминал и подключаемся к удаленному серверу по SSH, выполняя команду
    
        ssh <имя_пользователя>@<ip_адрес_сервера>
    
    В качестве примера, в моем случае это будет:
    
        ssh mike@188.124.51.136
    
    Результатом должно быть приглашение типа такого:
    
        Welcome to Ubuntu 22.04.1 LTS (GNU/Linux 5.15.0-58-generic x86_64)
        
         * Documentation:  https://help.ubuntu.com
         * Management:     https://landscape.canonical.com
         * Support:        https://ubuntu.com/advantage
        
        0 updates can be applied immediately.
        
        
        Last login: Sun Jan 22 22:36:57 2023 from <тут_был_ip_адрес>
    
3.  Заходим на сервере в директорию с вашим проектом. Либо последовательно перемещаясь по папкам, либо сразу указав нужный путь для команды `cd`.
    
        cd /home/<имя_пользователя>/<название_проекта>
    
    В моем случае команда будет выглядеть так:
    
        cd /home/mike/FSM_example_bot
    
4.  Убеждаемся, что находимся в директории с проектом (на всякий случай можно выполнить команду `pwd`) и выполняем команду на получение обновлений с GitHub
    
        git pull
    
    В случае успеха, в терминале будет сообщение типа такого:
    
        remote: Enumerating objects: 5, done.
        remote: Counting objects: 100% (5/5), done.
        remote: Compressing objects: 100% (1/1), done.
        remote: Total 3 (delta 2), reused 3 (delta 2), pack-reused 0
        Unpacking objects: 100% (3/3), 324 bytes | 12.00 KiB/s, done.
        From https://github.com/kmsint/FSM_example_bot
           e65cd1f..9f89118  master     -> origin/master
        Updating e65cd1f..9f89118
        Fast-forward
         bot.py | 2 ++
         1 file changed, 2 insertions(+)
    
5.  Перезапускаем юнит **systemd**
    
        sudo systemctl restart FSM_example_bot