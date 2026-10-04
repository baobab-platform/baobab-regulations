.PHONY: sync test lint typecheck security run example

sync:
	uv sync --all-groups

test:
	uv run pytest -m "not live_opa"

lint:
	uv run ruff check src tests

typecheck:
	uv run mypy

security:
	uv run bandit -r src -q
	uv run pip-audit

run:
	uv run uvicorn baobab_regulations.api.app:create_app --factory --host 0.0.0.0 --port 8080

example:
	uv run python examples/ug_za_coffee_reference.py
