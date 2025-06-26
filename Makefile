include .env

build:
	docker-compose build

up:
	docker-compose up --build

up-no-build:
	docker-compose up

down:
	docker-compose down

restart:
	docker-compose down && docker-compose up --build

migrate:
	docker-compose exec $(DB_CONTAINER_NAME) alembic upgrade head

makemigrations:
	docker compose exec $(DB_CONTAINER_NAME) alembic revision --autogenerate -m "Initial migration"

logs:
	docker-compose logs -f $(DB_CONTAINER_NAME)

rebuild: down build up

# Консоль psql усередині контейнера
psql:
	docker compose exec db \
	psql -U $(POSTGRES_USER) -d $(POSTGRES_DB)

# Показати всі таблиці
db-tables:
	docker compose exec db \
	psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c '\dt'

# Структура однієї таблиці: make db-desc TABLE=users
db-desc:
	docker compose exec db \
	psql -U $(POSTGRES_USER) -d $(POSTGRES_DB) -c '\d $(TABLE)'

# Бекап (dump) у файл dumps/backup.sql
db-dump:
	docker compose exec db \
	pg_dump -U $(POSTGRES_USER) $(POSTGRES_DB) > dumps/backup.sql
