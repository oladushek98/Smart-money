release: python manage.py migrate
web: gunicorn Diplom.wsgi --log-file -
worker: celery worker --app=Diplom --loglevel=debug --concurrency=4 -B