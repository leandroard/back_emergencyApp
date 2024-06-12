# Usamos una imagen base oficial de Python.
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    binutils  \
    libproj-dev \
        libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    curl \
    gettext \
 && rm -rf /var/lib/apt/lists/*

# Setup workdir
RUN mkdir /src
WORKDIR /src

# Copiar el archivo requirements.txt y dar permisos de lectura y escritura
COPY requirements.txt /src/
RUN chmod 644 /src/requirements.txt

# Python dependencies
RUN pip install -r /src/requirements.txt

COPY . /src

# Exponemos el puerto en el que correrá la aplicación.
EXPOSE 8000

# Comando para correr la aplicación.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "back_emergencyApp.wsgi:application"]
