

pm2 stop 0 
netstat -ntlp|grep 19000  | awk '{print $7}'| awk -F '/' '{print $1}' | xargs kill -9         

#pm2 start "/usr/SSO/sso_front/app.js"
#cd /usr/SSO/sso_back/
#nohup python3 manage.py runserver 0.0.0.0:19000 &
