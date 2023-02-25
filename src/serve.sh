poetry run alembic upgrade head
poetry run uvicorn --host 0.0.0.0 --port 80 api.main:app