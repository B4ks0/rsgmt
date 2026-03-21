import os
import django
from datetime import date, time
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from hospital.models import (
    Specialization, Department, Doctor, Patient, DoctorSchedule,
    ScheduleException, Appointment, AppointmentHistory,
    Payment, Notification, Review, ContactMessage
)

def create_dummy_data():
    print("Mempersiapkan penghapusan data lama...")
    Specialization.objects.all().delete()
    Department.objects.all().delete()
    Patient.objects.all().delete()
    ContactMessage.objects.all().delete()
    
    print("Memasukkan data dummy untuk QA testing...")

    # 1. Specializations
    s1 = Specialization.objects.create(name="Kardiologi", description="Spesialis Jantung")
    s2 = Specialization.objects.create(name="Neurologi", description="Spesialis Saraf")
    s3 = Specialization.objects.create(name="Pediatri", description="Spesialis Anak")
    
    print("✓ Specialization berhasil")

    # 2. Departments
    d1 = Department.objects.create(name="Poliklinik Jantung", location="Gedung Blok A - Lt 1", phone="101", floor_number=1)
    d2 = Department.objects.create(name="Poliklinik Saraf", location="Gedung Blok B - Lt 2", phone="102", floor_number=2)
    d3 = Department.objects.create(name="Poliklinik Anak", location="Gedung Anak - Lt 1", phone="103", floor_number=1)
    
    print("✓ Department berhasil")

    # 3. Doctors
    doc1 = Doctor.objects.create(full_name="Dr. Haris Jantung", email="haris@rs.com", phone="081111", specialization=s1, department=d1, experience_years=12, title="Sp.JP", bio="Ahli jantung RS Gunung Maria")
    doc2 = Doctor.objects.create(full_name="Dr. Sinta Saraf", email="sinta@rs.com", phone="082222", specialization=s2, department=d2, experience_years=8, title="Sp.S", bio="Spesialis saraf berpengalaman")
    doc3 = Doctor.objects.create(full_name="Dr. Fajar Anak", email="fajar@rs.com", phone="083333", specialization=s3, department=d3, experience_years=5, title="Sp.A", bio="Sangat ramah pada anak")
    
    print("✓ Doctor berhasil")

    # 4. Patients
    p1 = Patient.objects.create(full_name="Bapak Dedi", email="dedi@mail.com", phone="084444", date_of_birth=date(1980, 5, 20), gender="Laki-laki", blood_type="O", address="Jl. Tomohon Raya No 1", national_id="710123456789")
    p2 = Patient.objects.create(full_name="Ibu Eka", email="eka@mail.com", phone="085555", date_of_birth=date(1992, 10, 10), gender="Perempuan", blood_type="A", address="Jl. Minahasa No 2", national_id="712345678901")
    
    print("✓ Patient berhasil")

    # 5. DoctorSchedules
    for doc in [doc1, doc2, doc3]:
        DoctorSchedule.objects.create(doctor=doc, day_of_week=1, start_time=time(9, 0), end_time=time(13, 0)) # Senin
        DoctorSchedule.objects.create(doctor=doc, day_of_week=3, start_time=time(9, 0), end_time=time(13, 0)) # Rabu
    
    print("✓ DoctorSchedule berhasil")

    # 6. ScheduleExceptions
    ScheduleException.objects.create(doctor=doc1, exception_date=date.today(), reason="Sedang Simposium Keluar Kota", is_available=False)
    
    print("✓ ScheduleException berhasil")

    # 7. Appointments
    a1 = Appointment.objects.create(patient=p1, doctor=doc1, appointment_date=date.today(), appointment_time=time(10, 0), queue_number="A01", status="confirmed", type="offline", chief_complaint="Dada berdebar cepat")
    a2 = Appointment.objects.create(patient=p2, doctor=doc3, appointment_date=date.today(), appointment_time=time(11, 0), queue_number="C02", status="completed", type="offline", chief_complaint="Anak demam", notes="Sudah ditangani dengan baik")
    a3 = Appointment.objects.create(full_name="Pasien Tanpa Akun", phone="086666", department=d2, doctor=doc2, preferred_date=date.today(), status="requested", message="Ingin konsultasi masalah tulang belakang")
    
    print("✓ Appointment berhasil")

    # 8. AppointmentHistory
    AppointmentHistory.objects.create(appointment=a1, old_status="requested", new_status="confirmed", changed_by="Admin RS", reason="Dikonfirmasi by phone")
    
    print("✓ AppointmentHistory berhasil")


    # 10. Payments
    Payment.objects.create(appointment=a2, amount=250000.00, payment_method="QRIS", status="paid", transaction_id="TRX-12345ABC", invoice_number="INV-2026-03C02", paid_at=timezone.now())
    
    print("✓ Payment berhasil")

    # 11. Notifications
    Notification.objects.create(patient=p1, appointment=a1, type="reminder", channel="whatsapp", message="Halo Bapak Dedi, jangan lupa jadwal konsultasi Anda dengan Dr. Haris Jantung (Poli Jantung) pada hari ini pukul 10:00. Mohon datang tepat waktu.")
    
    print("✓ Notification berhasil")

    # 12. Reviews
    Review.objects.create(appointment=a2, patient=p2, doctor=doc3, rating=5, comment="Dokter Fajar sangat sabar memeriksa anak saya yang rewel. Tempatnya bersih dan perawatnya sigap membantu.", is_published=True)
    
    print("✓ Review berhasil")

    # 13. ContactMessages
    ContactMessage.objects.create(full_name="Warga Tomohon", email="wargatomohon@mail.com", subject="Tanya Jam Operasional IGD", message="Apakah IGD buka 24 jam di hari libur nasional?")
    
    print("✓ ContactMessage berhasil")
    print("SEMUA DATA DUMMY BERHASIL DIBUAT! SILAKAN CEK DI WEBSITE & ADMIN!")

if __name__ == "__main__":
    create_dummy_data()
