# RSG Umato — Hospital Website (Django)

## Run locally

```bash
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open:
- Site: `http://127.0.0.1:8000/`
- Admin: `http://127.0.0.1:8000/admin/`

## What’s included
- Public pages: Home, About, Services, Doctors, Contact
- Appointment request form (stored in DB, manageable in admin)
- Contact messages (stored in DB, manageable in admin)

