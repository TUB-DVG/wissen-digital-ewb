#!/bin/sh

set -e

envsubst < /etc/nginx/default.conf.tpl > /etc/nginx/conf.d/default.conf

# run nginx in the foreground, so every logmessage is sent to stdout
nginx -g 'daemon off;'
