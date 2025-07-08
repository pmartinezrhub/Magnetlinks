# Usar la imagen de Nginx oficial
FROM nginx:alpine

# Instalar Certbot
RUN apk add --no-cache certbot

# Copiar el archivo de configuración como plantilla
RUN mkdir -p /etc/nginx/conf.d/template
COPY default.conf.template /etc/nginx/conf.d/template/default.conf.template
# Crear el directorio para Certbot
RUN mkdir -p /var/www/certbot

# Copiar el script de inicio
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Establecer el script como punto de entrada
ENTRYPOINT ["/start.sh"]
