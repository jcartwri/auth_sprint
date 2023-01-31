FROM nginx:1.21

RUN rm /etc/nginx_rm/conf.d/default.conf && rm /etc/nginx_rm/nginx_rm.conf
COPY auth_movies.conf /etc/nginx/conf.d
COPY nginx.conf /etc/nginx