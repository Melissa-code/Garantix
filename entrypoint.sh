#!/bin/bash 
# Ce script s'exécute au démarrage du conteneur Docker

# Arrête le script si une commande échoue
set -e

cd /app

python manage.py migrate --noinput

if [ $1 == 'gunicorn' ]; then 
    echo "🚀 Lancement du serveur Django sur 0.0.0.0:8000"
    exec gunicorn garantix_config.wsgi:application --bind 0.0.0.0:8000    #serveur de prod (dr/fichier/variable application)
else 
    exec python manage.py runserver 0.0.0.0:8000                          #serveur de dév
fi 