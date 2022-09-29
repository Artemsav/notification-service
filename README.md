# Сервис уведомлений

Сервис разработан на django rest framework + celery + redis


## Установка и запуск

Скачайте код:
```sh
git clone https://gitlab.com/Artemsav/testing_task_mailing/
```

Перейдите в каталог проекта:
```sh
cd testing_task_mailing
```

[Установите Python](https://www.python.org/), если этого ещё не сделали.

Проверьте, что `python` установлен и корректно настроен. Запустите его в командной строке:
```sh
python --version
```
**Важно!** Версия Python должна быть не ниже 3.8.

Возможно, вместо команды `python` здесь и в остальных инструкциях этого README придётся использовать `python3`. Зависит это от операционной системы и от того, установлен ли у вас Python старой второй версии. 

В каталоге проекта создайте виртуальное окружение:
```sh
python -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:

- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```

Создать файл `.env` в каталоге `testing_task_mailing/` и положите туда следующие переменные окружения используемые в проекте:
```sh
SECRET_KEY=django-insecure-0if40nf4nf93n4 - секретный ключ джанго
API_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9 - токен конечного сервиса
DEBUG=False - режим для отладки
END_POINT_URL=https://probe.fbrq.cloud/ - url конечного сервиса 
```

Создайте файл базы данных SQLite и отмигрируйте её следующей командой:

```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```

Откройте сайт в браузере по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

