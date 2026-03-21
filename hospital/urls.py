from django.urls import path

from . import views


urlpatterns = [
    path("assets/logo.png", views.logo_png, name="logo_png"),
    path("assets/title-logo.png", views.title_logo_png, name="title_logo_png"),
    path("assets/banner-main", views.main_banner, name="main_banner"),
    path("assets/slideshow/<str:filename>.png", views.slideshow_image, name="slideshow_image"),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("services/", views.services, name="services"),
    path("doctors/", views.doctors, name="doctors"),
    path("doctors/<uuid:doctor_id>/", views.doctor_detail, name="doctor_detail"),
    path("appointments/", views.appointment_create, name="appointment_create"),
    path("contact/", views.contact, name="contact"),
    
    # Custom Backend Dashboard
    path("dashboard/login/", views.backend_login, name="backend_login"),
    path("dashboard/logout/", views.backend_logout, name="backend_logout"),
    path("dashboard/", views.backend_dashboard, name="backend_dashboard"),
    path("dashboard/appt/<uuid:appt_id>/status/", views.backend_update_status, name="backend_update_status"),
    
    # Custom Backend CRUD
    path("dashboard/appointments/add/", views.backend_appointment_add, name="backend_appointment_add"),
    path("dashboard/appointments/<uuid:appt_id>/edit/", views.backend_appointment_edit, name="backend_appointment_edit"),
    path("dashboard/appointments/<uuid:appt_id>/delete/", views.backend_appointment_delete, name="backend_appointment_delete"),
    
    # Custom Backend Lists
    path("dashboard/patients/", views.backend_patient_list, name="backend_patient_list"),
    path("dashboard/doctors/", views.backend_doctor_list, name="backend_doctor_list"),
    path("dashboard/payments/", views.backend_payment_list, name="backend_payment_list"),
    path("dashboard/departments/", views.backend_department_list, name="backend_department_list"),
    
    # API endpoints
    path("api/ocr-ktp/", views.ocr_ktp, name="ocr_ktp"),
    path("api/get-doctors-by-dept/", views.get_doctors_by_department, name="get_doctors_by_dept"),
    
    # QA Diagnostic
    path("dashboard/qa/ocr/", views.backend_qa_ocr, name="backend_qa_ocr"),
]

