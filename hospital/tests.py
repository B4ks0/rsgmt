from datetime import date, timedelta, time

from django.test import TestCase
from django.urls import reverse

from .forms import AppointmentForm
from .models import Department, Doctor, DoctorSchedule, ScheduleException


class AppointmentFormTests(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name="Umum")
        self.other_department = Department.objects.create(name="Gigi")
        self.doctor = Doctor.objects.create(full_name="dr. Aktif", department=self.department)
        self.other_doctor = Doctor.objects.create(full_name="dr. Lain", department=self.other_department)
        tomorrow = date.today() + timedelta(days=1)
        self.valid_date = tomorrow
        DoctorSchedule.objects.create(
            doctor=self.doctor,
            day_of_week=tomorrow.weekday(),
            start_time=time(8, 0),
            end_time=time(12, 0),
            is_active=True,
        )

    def form_data(self, **overrides):
        data = {
            "full_name": "Pasien QA",
            "national_id": "1234567890123456",
            "phone": "081234567890",
            "email": "qa@example.com",
            "is_new_patient": "True",
            "department": str(self.department.id),
            "doctor": str(self.doctor.id),
            "preferred_date": self.valid_date.isoformat(),
            "message": "Keluhan QA",
        }
        data.update(overrides)
        return data

    def test_valid_appointment_form_accepts_matching_schedule(self):
        form = AppointmentForm(data=self.form_data())

        self.assertTrue(form.is_valid(), form.errors)

    def test_rejects_doctor_from_different_department(self):
        form = AppointmentForm(data=self.form_data(doctor=str(self.other_doctor.id)))

        self.assertFalse(form.is_valid())
        self.assertIn("doctor", form.errors)

    def test_rejects_date_outside_doctor_schedule(self):
        unscheduled_date = self.valid_date + timedelta(days=1)
        form = AppointmentForm(data=self.form_data(preferred_date=unscheduled_date.isoformat()))

        self.assertFalse(form.is_valid())
        self.assertIn("preferred_date", form.errors)

    def test_rejects_unavailable_schedule_exception(self):
        ScheduleException.objects.create(
            doctor=self.doctor,
            exception_date=self.valid_date,
            is_available=False,
        )

        form = AppointmentForm(data=self.form_data())

        self.assertFalse(form.is_valid())
        self.assertIn("preferred_date", form.errors)


class DoctorAvailabilityApiTests(TestCase):
    def test_malformed_doctor_id_returns_json_error(self):
        response = self.client.get(
            reverse("get_doctor_available_dates"),
            {"doctor_id": "not-a-uuid"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["success"], False)
