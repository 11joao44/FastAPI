run:
	@uvicorn workout_api.main:app --reload

create-migrations:
	@export PYTHONPATH=$$PYTHONPATH:$(pwd) && alembic revision --autogenerate -m "$(d)"

run-migrations:
	@export PYTHONPATH=$$PYTHONPATH:$(pwd) && alembic upgrade head
