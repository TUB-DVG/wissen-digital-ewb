server {
    listen ${NGINX_LISTEN_PORT};
    server_name wissen-digital-ewb.de;
    
    location /static {
        alias /vol/static;
    }
    
    location /media {
	alias /vol/static/media;
    }

    location / {
        uwsgi_pass ${APP_HOST}:${UWSGI_LISTEN_PORT};
        include /etc/nginx/uwsgi_params;
        client_max_body_size 10M;
    }
}