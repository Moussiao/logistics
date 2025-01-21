# Backend и frontend для приложения "Бот логистика"

![CI](https://github.com/traffic-light-official/logistics/actions/workflows/ci.yml/badge.svg) [![Maintainability]
Django-based production project, integrated with telegram. Frontend is built on vue.js in the [folder](https://github.com/traffic-light-official/logistics/tree/master/frontend).

## Configuration

Переменные окружения (.env) лежит тут `backend/core/.env`, для примера используйте `backend/core/.env.example`

## Installing on a local machine

Для проекта необходим python 3.12. Зависимости управляются при помощи [Poetry](https://python-poetry.org/).

Install requirements:

```bash
poetry install --no-root
```

Конфигурация MariaDB и Redis, а также запуск django-приложения:

```bash
docker compose up
```

Миграции и другие django команды запускать в таком формате:

```bash
docker compose run --rm web python manage.py migrate
```

Testing:

```bash
docker compose run --rm web pytest
```
