SERVICE_WEB = payout_web
SERVICE_WORKER = payout_worker

.PHONY: help
help:
	@echo "Доступные команды:"
	@echo "  make up         - Запуск docker-compose"
	@echo "  make down       - Остановка docker-compose"
	@echo "  make restart    - Полный перезапуск всех сервисов"
	@echo "  make build      - Сборка контейнеров"
	@echo "  make logs       - Логи всех сервисов"
	@echo "  make web        - Shell в web контейнере"
	@echo "  make test       - Запуск тестов"
	@echo "  make migrate    - Применить миграции"
	@echo "  make makemigrations - Создать миграции"
	@echo "  make celery     - Логи Celery worker"

.PHONY: up
up:
	docker-compose up -d

.PHONY: down
down:
	docker-compose down

.PHONY: restart
restart:
	docker-compose down
	docker-compose up -d

.PHONY: build
build:
	docker-compose build

.PHONY: logs
logs:
	docker-compose logs -f

.PHONY: web
web:
	docker-compose exec -it web bash

.PHONY: test
test:
	docker-compose exec web poetry run pytest -v

.PHONY: migrate
migrate:
	docker-compose exec web poetry run python manage.py migrate

.PHONY: makemigrations
makemigrations:
	docker-compose exec web poetry run python manage.py makemigrations

.PHONY: celery
celery:
	docker-compose logs -f celery
