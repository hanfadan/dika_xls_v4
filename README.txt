Install Python3:
https://www.python.org/downloads/

- Buka Terminal
- Ketik perintah berikut:
    pip install -r requirements.txt
    python manage.py migrate
- Run Server, dengan perintah berikut
    python manage.py runserver


buat user awal :
python manage.py shell
from myapp.models import CustomUser

# Buat pengguna supervisor
supervisor = CustomUser.objects.create_user(username='supervisor', password='password123', role='supervisor')
supervisor.save()

# Buat pengguna production staff
production_staff = CustomUser.objects.create_user(username='production', password='password123', role='production')
production_staff.save()

# Buat pengguna warehouse staff
warehouse_staff = CustomUser.objects.create_user(username='warehouse', password='password123', role='warehouse')
warehouse_staff.save()
exit()

Supervisor:

Username: supervisor
Password: password123
Production Staff:

Username: production
Password: password123
Warehouse Staff:

Username: warehouse
Password: password123