# vladrunk WebApp

Для накатывания миграций, если файла `alembic.ini` ещё нет, нужно запустить в терминале команду:
```sh
alembic init migrations
```
После этого будет создана папка `migrations` с миграциями и конфигурационный файл `alembic.ini` для алембика.
1) B `alembic.ini` (_58 строка_) нужно задать адрес базы данных, в которую будем катать миграции. Пример:
```python
sqlalchemy.url = postgresql://postgres:postgres@0.0.0.0:5432/postgres
```
2) Дальше идём в папку с миграциями `migrations` и открываем `env.ру`. Вносим изменения в блок (_19-20 строка_):
```python
from db.models import Base
target_metadata = Base.metadata
```

3) После этого (_и после внесений изменений в моделях_) вводим: 
```sh
alembic revision --autogenerate -m "comment"
``` 
Будет создана миграция.

4) Затем применяем миграции в БД:    
```sh
alembic upgrade heads
```