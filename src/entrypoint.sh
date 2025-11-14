#!/bin/bash
set -e

echo "=== Démarrage de l'application Garantix ==="

# Attendre que la base de données soit disponible si PostgreSQL
if [ -n "$DB_HOST" ]; then
    echo "Attente de la base de données sur $DB_HOST..."
    timeout 30 bash -c 'until nc -z $DB_HOST ${DB_PORT:-5432}; do sleep 1; done' || echo "Timeout - continuation..."
fi

echo "Application des migrations..."
python manage.py migrate --noinput

# Collecte  fichiers statiques en prod seulement
if [ "$DJANGO_ENV" = "production" ]; then
    echo "Collection des fichiers statiques..."
    python manage.py collectstatic --noinput --clear
fi

# Crée un superuser si les variables sont définies (optionnel)
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Vérification du superuser..."
    python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists():
    User.objects.create_superuser('$DJANGO_SUPERUSER_USERNAME', '$DJANGO_SUPERUSER_EMAIL', '$DJANGO_SUPERUSER_PASSWORD')
    print('Superuser créé')
else:
    print('Superuser existe déjà')
END
fi

echo "=== Application prête ==="

# Lance la commande appropriée selon l'environnement
if [ "$1" = "runserver" ] || [ "$DJANGO_ENV" = "development" ]; then
    echo "Démarrage du serveur de développement..."
    exec python manage.py runserver 0.0.0.0:8000
elif [ "$1" = "gunicorn" ] || [ "$DJANGO_ENV" = "production" ]; then
    echo "Démarrage de Gunicorn..."
    exec gunicorn garantix_config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 120 \
        --access-logfile - \
        --error-logfile -
else
    # Permet d'exécuter n'importe quelle commande
    exec "$@"
fi