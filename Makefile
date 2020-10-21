DOCKER_SHELL:=docker-compose run --rm app
DOCKER_SHELL_WITH_DB:=docker-compose run --rm --no-deps -e WAIT_FOR_POSTGRES=TRUE app
DOCKER_DB_SHELL:=docker-compose run --rm db
MIGRATE_CMD:=alembic -c migrations/alembic.ini
PSQL_CMD:=PGPASSWORD=admin psql -h db -U admin -d mobilewallet

# Shells

shell:
	$(DOCKER_SHELL) bash

db-shell:
	$(DOCKER_DB_SHELL) bash -c '$(PSQL_CMD)'


# DB utilities

db-start: # Starts DB server
	docker-compose up -d db

db-migrate: db-start # Creates missing migrations
	$(DOCKER_SHELL_WITH_DB) "$(MIGRATE_CMD) revision --autogenerate"

db-populate: db-start # Populates DB with fixture data
	$(DOCKER_SHELL_WITH_DB) "$(PSQL_CMD) -f /app/migrations/fixtures.sql"

db-upgrade: db-start # Migrate DB according to latest migrations
	$(DOCKER_SHELL_WITH_DB) "$(MIGRATE_CMD) upgrade head"

db-drop: # Empty and removes db
	docker-compose stop db
	docker-compose rm -f db
	rm -rf .data

db-init: db-start db-upgrade db-populate # Initialise DB with structure and data


# Development server

create-dotenv:
	[[ -f .env ]] || echo "DEBUG=True\nSECRET=$$( date +%s | sha256sum | base64 | head -c 32 )" > .env

init: create-dotenv db-init

run: db-start
	docker-compose up app


# Tests

test: db-start
	$(DOCKER_SHELL_WITH_DB) "pytest tests -v -W ignore::DeprecationWarning"

