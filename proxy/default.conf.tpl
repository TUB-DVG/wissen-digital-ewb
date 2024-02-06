server {
	listen ${NGINX_LISTEN_PORT} ssl http2;
	listen [::]:${NGINX_LISTEN_PORT} ssl http2;
	server_name wissen-digital-ewb.de;
	add_header Strict-Transport-Security "max-age=31536; includeSubDomains" always;
	server_tokens off;
	ssl_certificate /etc/nginx/ssl/${NGINX_SSL_CERTIFICATE_FILENAME};
	ssl_certificate_key /etc/nginx/ssl/${NGINX_SSL_CERTIFICATE_KEY_FILENAME};
    ssl_session_timeout 1d;
    ssl_session_cache shared:MozSSL:10m;  # about 40000 sessions
    ssl_session_tickets off;

	ssl_buffer_size 8k;
    # intermediate configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384:DHE-RSA-CHACHA20-POLY1305;
    ssl_prefer_server_ciphers off;

    # OCSP stapling
    #ssl_stapling on;
    #ssl_stapling_verify on;
	#ssl_trusted_certificate /etc/nginx/ssl/rootCA;
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


