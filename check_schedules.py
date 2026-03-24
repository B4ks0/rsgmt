import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from hospital.models import Doctor, DoctorSchedule

doctors = Doctor.objects.filter(full_name__icontains='Olfi')
print('Doctors matching "Olfi":', doctors.count())
for doc in doctors:
    schedules = doc.schedules.filter(is_active=True)
    print(f'  Doctor: {doc.full_name} (ID: {doc.id})')
    print(f'  Active schedules: {schedules.count()}')
    for s in schedules:
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        print(f'    - {days[s.day_of_week]}: {s.start_time} - {s.end_time}')

print('\n' + '='*50 + '\n')
print('All doctors with schedule count:')
for doc in Doctor.objects.all()[:10]:
    count = doc.schedules.filter(is_active=True).count()
    print(f'  {doc.full_name}: {count}')
