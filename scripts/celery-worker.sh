#!/bin/bash
# Instala wait-for-it si aún no está instalado
apt-get update && apt-get install -y wait-for-it

# Espera a que Redis esté listo
wait-for-it redis:6379 -t 30 -- celery -A back_emergencyApp worker --loglevel=info
