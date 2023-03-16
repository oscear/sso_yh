pm2 start "/usr/SSO/sso_front/app.js"
cd /usr/SSO/sso_back/
nohup python3 manage.py runserver 0.0.0.0:19000 &
tail -f nohup.out
