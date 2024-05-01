.PHONY: build run format test check
build:
	poetry install

format:
	poetry run autoflake --in-place --remove-all-unused-imports --remove-unused-variables --recursive .
	poetry run isort . --profile black
	poetry run black .

test:
	poetry run coverage run --branch --source agnostic_migrations -m pytest -rP tests/ 
	poetry run coverage html
	poetry run coverage report --fail-under=100

check: test
	poetry run autoflake --recursive . --check
	poetry run isort . --profile black --check-only
	poetry run black . --check
