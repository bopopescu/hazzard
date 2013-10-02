HOW TO DJANGO

create new db
remove hazzard.db first
python manage.py sql app
python manage.py syncdb
create user that are admin so you can login to admin section

GO to admin section

127.0.0.1:8000/admin


RUN 
python manage.py runserver

TEST WITH Model
python manage.py shell

WHY can't register 

no Role declare on db setup so go into admin section and create Role with name='non_autherize_member','autherize_member','officer'


CAN not find template file

template file is in app/template/main/ create the file to help the work is good :)

