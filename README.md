# vladrunk WebApp

Для накатывания миграций, если файла alembic.ini ещё нет, нужно запустить в терминале команду:

```
alembic init migrations
```

После этого будет создана лапка с миграциями и конфигурационный файл для алембика.
 - B alembic.ini (58 строка) нужно задать адрес базы данных, в которую будем катать миграции.
 - Дальше идём в лалку с миграциями и открываем env. ру, там вносим изменения в блок (19-20 строка), где написано

```
from myapp import mymodel
```

- Дальше вводим: ```alembic revision --autogenerate -m "comment"```
- Будет создана миграция
- Дальше вводим: ```alembic upgrade heads```