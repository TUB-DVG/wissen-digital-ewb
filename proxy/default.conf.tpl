#server {
#    listen ${NGINX_LISTEN_PORT};
#    server_name wissen-digital-ewb.de;
#    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
	# Redirect http to https:
#    location / {
#	return 301 https://wissen-digital-ewb.de$request_uri;
#    }
    
}
server {
	listen 443 ssl http2;
	server_name wissen-digital-ewb.de;
	add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
	server_tokens off;
	ssl_certificate /etc/nginx/ssl/stratoCert.crt;
	ssl_certificate_key /etc/nginx/ssl/wissen-digital-ewb_de.key;
	
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


