server {
    listen ${NGINX_LISTEN_PORT};
    server_name wissen-digital-ewb.de;
    location ~ /.well-known/acme-challenge {
    	allow all;
	root /usr/share/nginx/html/letsencrypt;
    }
    location /static {
        alias /vol/static;
    }
    
    location /media {
	alias /vol/static/media;
    }

    location / {
	return 301 https://h3002249.stratoserver.net$request_uri;
        #uwsgi_pass ${APP_HOST}:${UWSGI_LISTEN_PORT};
        #include /etc/nginx/uwsgi_params;
        #client_max_body_size 10M;
    }
    
    # Redirect http to https:
}
server {
	listen 443 ssl http2;
	server_name wissen-digital-ewb.de;
	
	ssl on;
	server_tokens off;
	ssl_certificate /etc/nginx/ssl/live/h3002249.stratoserver.net/fullchain.pem;
	ssl_certificate_key /etc/nginx/ssl/live/h3002249.stratoserver.net/privkey.pem;
	ssl_dhparam /etc/nginx/dhparam/dhparam-2048.pem;
	
	ssl_buffer_size 8k;
	ssl_protocols TLSv1.2 TLSv1.1 TLSv1;
	ssl_prefer_server_ciphers on;
	ssl_ciphers ECDH+AESGCM:ECDH+AES256:ECDH+AES256:ECDH+AES128:DH+3DES:!ADH:!AECDH:!MD5;

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


