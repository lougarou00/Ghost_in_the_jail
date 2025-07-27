# Utiliser une image Python officielle
FROM python:3.10-slim

# Mettre à jour pip et installer Flask
RUN pip install --upgrade pip
RUN pip install Flask

# Copier le script Python dans le container
COPY pyjail.py /app/pyjail.py

# Définir le dossier de travail
WORKDIR /app

# Exposer le port 3000 (comme dans ton app Flask)
EXPOSE 3000

# Lancer l'application Flask
CMD ["python", "pyjail.py"]
