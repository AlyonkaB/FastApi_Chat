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
	docker-compose exec $(DB_CONTAINER_NAME) alembic revision --autogenerate -m "Initial migration"

logs:
	docker-compose logs -f $(DB_CONTAINER_NAME)

rebuild: down build up

rebuild: down build up
