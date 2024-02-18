startserver:
	python manage.py run
init-migrations:
	python manage.py alembic revision --autogenerate -m "initial" 
migrate:
	python manage.py alembic upgrade head
createdb:
	python manage.py createdb