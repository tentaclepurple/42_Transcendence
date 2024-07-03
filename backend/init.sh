#!/bin/bash

cd /app/backend/

while ! nc -z postgres 5432; do
    sleep 1
done
echo "PostgreSQL started"


echo "---------------------------------------------------------------------------------------\n"
# Ejecutar migraciones
echo "Migraciones de apps\n"

python manage.py makemigrations
python manage.py makemigrations users
python manage.py makemigrations statistic
python manage.py makemigrations tournament
python manage.py makemigrations pong
python manage.py makemigrations twofa
python manage.py makemigrations chat
python manage.py migrate
echo "---------------------------------------------------------------------------------------\n"

echo "Creando superusuario\n"

# Crear superusuario
python manage.py createsuperuser --noinput --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL --nickname $DJANGO_SUPERUSER_NICKNAME

echo "---------------------------------------------------------------------------------------\n"
echo "Iniciando servidor\n"

cd blchain/truffle && truffle migrate --network development
cd /app/backend/

# Iniciar servidor
python manage.py runserver 0.0.0.0:8000

