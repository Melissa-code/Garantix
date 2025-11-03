FROM python:3.11-slim

# évite utilisation de la mémoire cache
ENV PYTHONUNBUFFERED=1
# évite écriture des fichiers byte qui surchargent conteneur
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Installe dépendances système pour psycopg2 
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# copie fichiers de requirements d'abord pour le cache Docker
COPY requirements.txt /app/ 

# Installe les dépendances Python (pas besoin de venv car conteneur est isolé)
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# Copie le reste de l'application
COPY ./src/ /app/

# fichier: script shell que Docker exécute automatiquement au démarrage du conteneur
# prépare l’environnement avant de lancer Django, par ex: faire les migrations...
# lance le vrai processus: Gunicorn ou le serveur de dev Django
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

# Commande par défaut (peut être surchargée)
CMD ["runserver"]