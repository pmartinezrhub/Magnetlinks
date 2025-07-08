#!/bin/sh

set -e  # Exit on any error

CERTBOT_WEBROOT="/var/www/certbot"
mkdir -p $CERTBOT_WEBROOT

# Substitute environment variables in Nginx config
envsubst '${SERVER_NAME}' < /etc/nginx/conf.d/template/default.conf.template > /etc/nginx/conf.d/default.conf

# Obtain certificates if they don't exist
# if [ ! -f /etc/letsencrypt/live/${DOMAIN}/fullchain.pem ]; then
#     echo "Obtaining certificates for ${DOMAIN}..."
# certbot certonly --webroot -w $CERTBOT_WEBROOT \
#      -d ${DOMAIN} \
#      --email ${CERTBOT_EMAIL} \
#         --agree-tos \
#         --non-interactive \
#         --force-renewal
# fi

# Start Nginx
echo "Starting Nginx..."
nginx -g "daemon off;"