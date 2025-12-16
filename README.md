# Biblioteca Async con Flask + Celery + KeyDB

## Ejecutar KeyDB
keydb-server

## Instalar dependencias
pip install -r requirements.txt

## Iniciar Flask
flask run

## Iniciar Celery
celery -A celery_app.celery worker --loglevel=info