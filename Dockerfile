FROM python:3.13.2-alpine3.21

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos necesarios al contenedor
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código (incluye app.py y otros)
COPY . .

# Expone el puerto de la aplicación Flask/Gunicorn
EXPOSE 5000

# Comando para ejecutar la app con Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]