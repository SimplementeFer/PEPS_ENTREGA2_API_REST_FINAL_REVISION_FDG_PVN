FROM httpd:2.4.33-alpine

# Copiar los archivos HTML al directorio raíz de Apache
COPY . /usr/local/apache2/htdocs/

# Exponer el puerto 80 para servir la aplicación

EXPOSE 80


RUN apk update; \
    apk upgrade;
# Copy apache vhost file to proxy php requests to php-fpm container
COPY demo.apache.conf /usr/local/apache2/conf/demo.apache.conf
RUN echo "Include /usr/local/apache2/conf/demo.apache.conf" \
    >> /usr/local/apache2/conf/httpd.conf