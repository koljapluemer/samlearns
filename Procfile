web: gunicorn samlearns.wsgi --log-file -
release: python manage.py collectstatic --noinput && python manage.py migrate 