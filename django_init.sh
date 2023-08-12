#!/bin/bash
checkdb=$(nc -zv db 5432 2>&1)
echo $checkdb
while [[ $checkdb == *'failed'* ]]
do
  echo 'Waiting for data base to connect...'
  sleep 1
  checkdb=$(nc -zv db 5432 2>&1)
done

# Make migrations if required
if [ $MAKE_MIGRATIONS = "True" ]; then
  echo "Making migrations..."
  python3 /code/$DJANGO_PROJECT/manage.py makemigrations
fi

if [ $MIGRATE = "True" ]; then
  echo "Migrating database..."
  python3 /code/$DJANGO_PROJECT/manage.py migrate
fi

if [ $COLLECT_STATIC = "True" ]; then
  echo "Collecting static files..."
  python3 /code/$DJANGO_PROJECT/manage.py collectstatic --no-input

fi

#Does a superuser need to be created?
echo "Check for superuser..."
python3 /code/$DJANGO_PROJECT/manage.py createsuperuser --noinput

# start development server
python3 /code/$DJANGO_PROJECT/manage.py runserver 0.0.0.0:8000
