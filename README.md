**Server Configuration for SuperPig**

The SuperPig application is hosted in a remote server in a traditional web server
configuration where the backend program and the databse resides on the same host.
No docker containers, no CI/CD, just one click deployment to the changes 
to the serve.r 

---

## Project structure
1. The SuperPig app is divided into 3 repositories;
    - pig_ops           # FastAPI backend
    - pig_ops_db        # Stored procedures and migration scripts for any changes of the database
    - pig_ops_ui_mob    # Front end javascript codes 

2. Directory structure
root@prod-pig-ops:~/projects/jsys# ls -l
total 56
-rw-r--r-- 1 root root     7 Apr 10 23:22 app.pid
drwxr-xr-x 2 root root  4096 Apr 10 23:22 deploy_logs
-rwxr-xr-x 1 root root 19974 Mar 29 10:58 deploy.sh
drwxr-xr-x 4 root root  4096 Mar 27 05:23 pig_ops
drwxr-xr-x 5 root root  4096 Apr  7 06:59 pig_ops_db
drwxr-xr-x 6 root root  4096 Mar 19 02:57 pig_ops_ui_mob
drwxr-xr-x 2 root root  4096 Mar 28 04:19 restart_logs
-rwxr-xr-x 1 root root  5603 Mar 23 00:49 restart.sh
-rw-r--r-- 1 root root    10 Apr 10 23:22 version.txt

app.pid - generated; current PID of the FastApi program
deploy.sh - script to one click update server codes; This is copied from 
    root@prod-pig-ops:~/projects/jsys/pig_ops/webroot/scripts/deploy.sh
    
    Any changes of this script should be also manually overwrite  
        ~/projects/jsys/deploy.sh
        
        
version.txt - generated; This is updated in every execution of deploy.sh
---

## Server Updates

1.  No manual git pull; Just execute ./deploy.sh  


---

## Nginx Config

1. Location of Nginx config

root@prod-pig-ops:/etc/nginx/sites-available# ls -lt
total 8
-rw-r--r-- 1 root root 1936 Mar 20 06:06 superpig
-rw-r--r-- 1 root root 2412 Nov 30  2023 default

2. Static file links

root@prod-pig-ops:/var/www/superpig# ls -lt
total 0
lrwxrwxrwx 1 www-data www-data 45 Mar 16 08:47 static_m -> /root/projects/jsys/pig_ops_ui_mob/src/static
lrwxrwxrwx 1 www-data www-data 41 Mar 16 08:47 static -> /root/projects/jsys/pig_ops_ui_mob/static

3. cat /etc/nginx/sites-available/superpig

root@prod-pig-ops:/etc/nginx/sites-available# cat /etc/nginx/sites-available/superpig
# Redirect jsysdev.com to superpig.jsysdev.com
server {
    listen 80;
    listen [::]:80;
    server_name jsysdev.com www.jsysdev.com;
    return 301 https://superpig.jsysdev.com$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name jsysdev.com www.jsysdev.com;
    ssl_certificate /etc/letsencrypt/live/superpig.jsysdev.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/superpig.jsysdev.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    return 301 https://superpig.jsysdev.com$request_uri;
}

server {
    server_name superpig.jsysdev.com www.superpig.jsysdev.com;
    
    # Error pages
    error_page 502 503 504 /maintenance.html;
    location = /maintenance.html {
        root /root/projects/jsys/pig_ops/webroot/templates;
        internal;
    }
    
    location /static/ {
        alias /root/projects/jsys/pig_ops_ui_mob/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
    
    location /static_m/ {
        alias /root/projects/jsys/pig_ops_ui_mob/src/static/;
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/superpig.jsysdev.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/superpig.jsysdev.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = superpig.jsysdev.com) {
        return 301 https://$host$request_uri;
    }
    listen 80;
    server_name superpig.jsysdev.com www.superpig.jsysdev.com;
    return 404;
}

