# Garantix 

Site de gestion de garanties 

---

## 1. Créer un dossier pour le projet

```
mkdir garantix
cd garantix
```

## 2. Cloner le dépôt distant

- Cloner dans le dossier courant : `git clone https://github.com/Melissa-code/Garantix.git .`

## 3. Créer et activer l’environnement virtuel

```
# Windows
python -m venv env
env\Scripts\activate
# ou macOS/Linux
source env/bin/activate  
```

## 4. Installer les dépendances

- Pour récupérer les dépendances mises dans requirements.txt : `pip install -r requirements.txt`

## Shoelace 

Attention: input dans Shoelace n'ont pas d'image ! 

## 5. Base de données

`cd "C:/Program Files/PostgreSQL/17/bin"`

(env) PS C:\Program Files\PostgreSQL\17\bin> `./psql -U username`

## 6. Tests 

- dans Docker: `docker-compose exec web python manage.py test`
- local: dans `src` : `python manage.py test`

Dans DOcker
```
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py test

docker-compose build --no-cache

docker exec -it garantix_web python manage.py collectstatic --noinput 
```

- `factory-boy` : Génération de données de test: `docker exec -it garantix_web pip install whitenoise`
- puis `docker exec -it garantix_web pip freeze > requirements.txt` et `docker-compose build web`

et idem en local  


## 7. Servir les fichiers statiques en production sans serveur externe Nginx 

- installer la bilbiothèque WhiteNoise `docker exec -it garantix_web pip install whitenoise`
- mettre à jour requirements.txt `docker exec -it garantix_web pip freeze > requirements.txt`
- reconstruit l'image `docker-compose build web`
- idem en local 

- ajouter whitenoise dans `settings.py` :
```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # DOIT ÊTRE ICI
    # ... le reste ...
]
...
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
```
Voir pour prod: 
STORAGES = {
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        if IS TEST else
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"
    },
}

