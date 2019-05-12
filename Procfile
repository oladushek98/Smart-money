release: python manage.py migrate
web: gunicorn Diplom.wsgi --log-file -
worker: celery worker --app=stlab-diplom --loglevel=debug --concurrency=4 -B