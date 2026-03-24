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
    
    # API endpoints
    path("api/submit-contact/", views.contact, name="api_submit_contact"),
    path("api/get-doctors-by-dept/", views.get_doctors_by_department, name="get_doctors_by_dept"),
    path("api/get-doctor-available-dates/", views.get_doctor_available_dates, name="get_doctor_available_dates"),
    
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
    path("dashboard/patients/add/", views.backend_patient_create, name="backend_patient_create"),
    path("dashboard/patients/<uuid:patient_id>/edit/", views.backend_patient_edit, name="backend_patient_edit"),
    path("dashboard/doctors/", views.backend_doctor_list, name="backend_doctor_list"),
    path("dashboard/doctors/add/", views.backend_doctor_create, name="backend_doctor_create"),
    path("dashboard/doctors/<uuid:doctor_id>/edit/", views.backend_doctor_edit, name="backend_doctor_edit"),
    path("dashboard/doctors/<uuid:doctor_id>/delete/", views.backend_doctor_delete, name="backend_doctor_delete"),
    path("dashboard/payments/", views.backend_payment_list, name="backend_payment_list"),
    path("dashboard/contacts/", views.backend_contact_list, name="backend_contact_list"),
    path("dashboard/contacts/<int:contact_id>/detail/", views.backend_contact_detail, name="backend_contact_detail"),
    path("dashboard/departments/", views.backend_department_list, name="backend_department_list"),
    path("dashboard/departments/add/", views.backend_department_create, name="backend_department_create"),
    path("dashboard/departments/<int:dept_id>/edit/", views.backend_department_edit, name="backend_department_edit"),
]

