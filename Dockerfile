FROM nginx:alpine
COPY index.html /usr/share/nginx/html/index.html
COPY brand-campaign-registration /usr/share/nginx/html/brand-campaign-registration
