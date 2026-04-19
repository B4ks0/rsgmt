import uuid
from django.db import models
from django.utils import timezone

class Specialization(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    icon_url = models.URLField(blank=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=120, unique=True)
    location = models.CharField(max_length=120, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    floor_number = models.IntegerField(default=1)
    description = models.TextField(blank=True) # Kept for backwards compatibility

    def __str__(self):
        return self.name

class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=160)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40, blank=True)
    license_number = models.CharField(max_length=100, blank=True)
    specialization = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True, related_name='doctors')
    department = models.ForeignKey(Department, on_delete=models.PROTECT, related_name='doctors')
    photo_url = models.CharField(max_length=255, blank=True)
    experience_years = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Keeping old fields backwards-compatible
    title = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="doctors/", blank=True, null=True)

    class Meta:
        ordering = ["full_name"]

    def __str__(self):
        return self.full_name

class Patient(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=160)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=40)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    blood_type = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    national_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

class DoctorSchedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.IntegerField() # 0 = Monday, 6 = Sunday
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration_min = models.IntegerField(default=15)
    max_patients = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)

class ScheduleException(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedule_exceptions')
    exception_date = models.DateField()
    reason = models.CharField(max_length=255, blank=True)
    is_available = models.BooleanField(default=False)

class Appointment(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        CONFIRMED = "confirmed", "Confirmed"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='appointments', null=True, blank=True)
    schedule = models.ForeignKey(DoctorSchedule, on_delete=models.SET_NULL, null=True, blank=True, related_name='appointments')
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.TimeField(null=True, blank=True)
    queue_number = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=40, choices=Status.choices, default=Status.REQUESTED)
    type = models.CharField(max_length=40, default='online')
    chief_complaint = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    booked_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Legacy fields for views compatibility
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    preferred_date = models.DateField(null=True, blank=True)
    full_name = models.CharField(max_length=160, blank=True)
    national_id = models.CharField(max_length=20, blank=True)
    ktp_photo = models.ImageField(upload_to='ktp_photos/', null=True, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    message = models.TextField(blank=True)
    email = models.EmailField(blank=True)
    is_new_patient = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['status']),  # For filtering by status
            models.Index(fields=['-booked_at']),  # For ordering and listing
            models.Index(fields=['doctor', 'appointment_date']),  # For doctor schedules
            models.Index(fields=['patient']),  # For patient appointments
            models.Index(fields=['status', '-booked_at']),  # For dashboard filtering + ordering
        ]

    def __str__(self):
        name = self.patient.full_name if self.patient else self.full_name
        return f"{name} ({self.appointment_date or self.preferred_date})"

    @property
    def get_whatsapp_url(self):
        import urllib.parse
        phone_num = self.patient.phone if self.patient else self.phone
        if not phone_num:
            return "#"
        
        phone_num = ''.join(filter(str.isdigit, phone_num))
        if phone_num.startswith("08"):
            phone_num = "628" + phone_num[2:]
        elif phone_num.startswith("8"):
            phone_num = "628" + phone_num[1:]
        elif phone_num.startswith("0"):
            phone_num = "62" + phone_num[1:]
            
        name = self.patient.full_name if self.patient else self.full_name
        doctor_name = self.doctor.full_name if self.doctor else "Dokter"
        
        raw_poli = self.department.name if self.department else (self.doctor.department.name if self.doctor else "")
        # Remove redundant Poli/Poliklinik prefixes
        if raw_poli.lower().startswith("poli "):
            raw_poli = raw_poli[5:]
        elif raw_poli.lower().startswith("poliklinik "):
            raw_poli = raw_poli[11:]
        
        poli_text = f"Poli {raw_poli.strip()}" if raw_poli else "Poliklinik"
        
        appointment_dt = self.appointment_date or self.preferred_date
        
        # Localize date string (basic indonesian fallback)
        if appointment_dt:
            months = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
            date_str = f"{appointment_dt.day} {months[appointment_dt.month]} {appointment_dt.year}"
        else:
            date_str = "jadwal yang akan ditentukan"
            
        text = f"Halo Bapak/Ibu {name},\n\nTerima kasih telah membuat jadwal janji temu di RS Gunung Maria Tomohon. Kami ingin mengonfirmasi jadwal kunjungan Anda dengan {doctor_name} di {poli_text} pada tanggal {date_str}.\n\nMohon balas pesan ini untuk menyatakan konfirmasi kehadiran Anda. Terima kasih!"
        
        encoded_text = urllib.parse.quote(text)
        return f"https://wa.me/{phone_num}?text={encoded_text}"

class AppointmentHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='history')
    old_status = models.CharField(max_length=40, blank=True)
    new_status = models.CharField(max_length=40)
    changed_by = models.CharField(max_length=100)
    reason = models.TextField(blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True)
    status = models.CharField(max_length=40, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    invoice_number = models.CharField(max_length=100, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='notifications')
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    type = models.CharField(max_length=50)
    channel = models.CharField(max_length=50)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.OneToOneField(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='review')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='reviews')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField()
    comment = models.TextField(blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class ContactMessage(models.Model):
    full_name = models.CharField(max_length=160, db_index=True)
    email = models.EmailField(db_index=True)
    subject = models.CharField(max_length=180, db_index=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_resolved = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=['-created_at', 'is_resolved']),
        ]

    def __str__(self) -> str:
        return f"{self.full_name}: {self.subject}"
