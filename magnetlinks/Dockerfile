# Usar una imagen base de Debian con Python 3.9
FROM python:3.11

# Establecer el directorio de trabajo
WORKDIR /magnetlinks

# Crear el usuario celeryuser
RUN useradd -ms /bin/bash celeryuser
#RUN echo "8.8.8.8" > /etc/resolv.conf
# Copiar el archivo de requerimientos y luego instalar las dependencias de Python
COPY requirements.txt /magnetlinks/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos de la aplicación
COPY magnetlinks/ /magnetlinks/

# Cambiar al usuario celeryuser una vez funcione todo descomentar!!!
USER celeryuser

# Exponer el puerto 8000 para Django
EXPOSE 8000

# Comando predeterminado
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--insecure"]

