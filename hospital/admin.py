from django.contrib import admin
from .models import (
    Specialization, Department, Doctor, Patient, DoctorSchedule,
    ScheduleException, Appointment, AppointmentHistory,
    Payment, Notification, Review, ContactMessage
)

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ["name", "floor_number", "phone"]
    search_fields = ["name"]

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ["full_name", "department", "specialization", "is_active"]
    list_filter = ["department", "specialization", "is_active"]
    search_fields = ["full_name", "title", "department__name"]

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ["full_name", "phone", "email", "date_of_birth"]
    search_fields = ["full_name", "phone", "national_id"]

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ["doctor", "day_of_week", "start_time", "end_time", "is_active"]
    list_filter = ["day_of_week", "is_active"]

@admin.register(ScheduleException)
class ScheduleExceptionAdmin(admin.ModelAdmin):
    list_display = ["doctor", "exception_date", "is_available"]

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ["patient_display", "doctor", "appointment_date", "status", "booked_at"]
    list_filter = ["status", "type"]
    search_fields = ["patient__full_name", "full_name", "phone"]

    def patient_display(self, obj):
        return obj.patient.full_name if obj.patient else obj.full_name
    patient_display.short_description = "Patient"

@admin.register(AppointmentHistory)
class AppointmentHistoryAdmin(admin.ModelAdmin):
    list_display = ["appointment", "old_status", "new_status", "changed_by", "changed_at"]



@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["appointment", "amount", "payment_method", "status", "paid_at"]
    list_filter = ["status", "payment_method"]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["patient", "type", "channel", "is_read", "sent_at"]
    list_filter = ["is_read", "type", "channel"]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["patient", "doctor", "rating", "is_published", "created_at"]
    list_filter = ["rating", "is_published"]

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["full_name", "subject", "email", "is_resolved", "created_at"]
    list_filter = ["is_resolved"]
    search_fields = ["full_name", "email", "subject"]
