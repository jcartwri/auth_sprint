# Сервис аутентификации на Flask

## Документация OpenAPI
После запуска приложения документация API Auth Service доступна по ссылке: http://127.0.0.1/apidocs.

После запуска приложения документация API Movies Service доступна по ссылке: http://127.0.0.1/api/openapi.

## Трассировка

После запуска приложения результаты трассировки (Jaeger) доступны по адресу: http://127.0.0.1:16686.

## Миграция БД
```
flask db init
flask db migrate -m "user table"

# Обновление данных в БД
flask db uprgade
```

## Запуск сервиса
В файлах env.example (auth/movies) находятся точные параметры, которые должны находиться в файлах .env соответствующих директорий для запуска докера.
```
docker-compose up -d
```

## Тестирование
Для запуска тестов необходимо выполнить docker-compose.yml в папке tests/functional каждого из сервисов (auth/movies).

```
docker-compose up -d
```

## Создание суперпользователя

```
export FLASK_APP=app.py
flask create_admin username password email last_name first_name
```


