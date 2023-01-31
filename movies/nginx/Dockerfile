FROM nginx:1.21

RUN rm /etc/nginx_rm/conf.d/default.conf
COPY nginx.conf /etc/nginx
COPY configs/site.conf /etc/nginx/conf.d