# Payout Service — REST API для управления заявками на выплату

Тестовое задание Backend Developer (Django + DRF + Celery)

---

## Описание проекта

Сервис предназначен для управления заявками на выплату средств.
Каждая заявка создаётся через REST API и асинхронно обрабатывается с помощью Celery.

Реализовано:

* REST API на Django + DRF
* Асинхронная обработка через Celery + Redis
* PostgreSQL
* Валидация данных
* Тесты (pytest)
* Docker + docker-compose
* Poetry
* Makefile


---

## Стек технологий

* Python 3.12
* Django 4.2
* Django REST Framework
* Celery
* Redis (broker)
* PostgreSQL
* Docker / docker-compose
* Poetry
* Pytest

---

## Запуск проекта

### 1. Клонирование репозитория

```bash
git clone <repository_url>
cd payout-service
```

---

### 2. Настройка окружения

Создать файл `.env` в корне проекта:

```env
# Django
DEBUG=1
SECRET_KEY=my-very-secret-key

# PostgreSQL
DB_NAME=payouts
DB_USER=payouts
DB_PASSWORD=payouts
DB_HOST=db
DB_PORT=5432

# Celery
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

---

### 3. Сборка и запуск контейнеров

```bash
make build
make up
```

Или напрямую:

```bash
docker-compose up --build -d
```

---

### 4. Применение миграций

```bash
make migrate
```

---

### 5. Запуск Celery worker

Worker запускается автоматически через docker-compose.

Проверка логов:

```bash
make celery
```

---

### 6. Запуск тестов

```bash
make test
```

---

### 7. Доступ к API

API доступно по адресу:

```
http://localhost:8000/api/payouts/
```

---

## Основные эндпоинты

| Метод  | URL                | Описание        |
| ------ | ------------------ | --------------- |
| GET    | /api/payouts/      | список заявок   |
| GET    | /api/payouts/{id}/ | получить заявку |
| POST   | /api/payouts/      | создать заявку  |
| PATCH  | /api/payouts/{id}/ | обновить заявку |
| DELETE | /api/payouts/{id}/ | удалить заявку  |

---

## Makefile команды

```bash
make up             # запуск контейнеров
make down           # остановка
make restart        # полный перезапуск
make test           # запуск тестов
make migrate        # миграции
make makemigrations # создание миграций
make web            # shell в web контейнере
make celery         # логи celery worker
```

---
## Документация API (Swagger / Redoc)

Для удобного изучения и тестирования API доступна интерактивная документация:

| Интерфейс       | URL                                |
| --------------- | --------------------------------- |
| OpenAPI Schema  | `/api/schema/`                     |
| Swagger UI      | `/api/schema/swagger/`             |
| Redoc           | `/api/schema/redoc/`               |

- **Swagger UI** — интерактивный веб-интерфейс для тестирования эндпоинтов прямо из браузера.  
- **Redoc** — альтернативная визуализация OpenAPI-схемы с удобной навигацией.  

Пример: после запуска проекта через `docker-compose up` можно открыть браузер по адресу:

http://localhost:8000/api/schema/swagger/

Copy code

и увидеть все эндпоинты с формами для тестирования запросов.

## Асинхронная обработка

При создании заявки автоматически запускается Celery-задача, которая:

* принимает ID заявки
* имитирует обработку
* меняет статус заявки на processed / failed

---

## Валидация

Проверяется:

* обязательность полей
* положительная сумма
* формат валюты
* длина реквизитов
* допустимые переходы статусов
* запрет изменения обработанных заявок

---

## Тесты

Реализованы:

* тест создания заявки
* тест запуска Celery-задачи (mock)
* тесты PATCH
* тесты валидации
* тест модели

Используется pytest + pytest-django.

---

## Как я представляю деплой в продакшн

### Сервисы:

* Nginx
* Django (gunicorn)
* PostgreSQL (managed)
* Redis (managed)
* Celery workers

### Архитектура:

* Nginx -> Gunicorn (Django API)
* Redis как broker
* Отдельные Celery workers
* PostgreSQL как основная БД

### Запуск:

* CI/CD (GitHub Actions)
* Docker registry
* Kubernetes / Docker Swarm
* Отдельные deployment для web и worker

### Переменные окружения:

* DEBUG=0
* SECRET_KEY
* DATABASE_URL
* CELERY_BROKER_URL

---

