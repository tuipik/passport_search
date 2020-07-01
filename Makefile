req:
	@pip install -r requirements.txt
env:
	@python3.7 -m venv env && source env/bin/activate
migrate:
	@python manage.py migrate && python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')"
db:
	@python manage.py update_db
run:
	@python manage.py runserver