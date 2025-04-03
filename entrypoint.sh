#!/bin/bash

# Set default values for superuser credentials
SUPERUSER_EMAIL="thiru_admin@example.com"
SUPERUSER_USERNAME="thiru_admin"
SUPERUSER_PASSWORD="adminThiru006)^"

# Run migrations
echo "Running make migrations..."
python manage.py makemigrations --noinput
echo "Running migrate..."
python manage.py migrate --noinput

# Run Django shell command to create superuser
echo "Creating superuser..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='$SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')
    print("Superuser created successfully.")
else:
    print("Superuser already exists.")
EOF

# Start server
echo "Starting server..."
exec python manage.py runserver 0.0.0.0:8000
