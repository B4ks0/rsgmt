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
    path("api/ocr-ktp/", views.ocr_ktp, name="ocr_ktp"),
    path("api/get-doctors-by-dept/", views.get_doctors_by_department, name="get_doctors_by_dept"),
    
    # QA Diagnostic
    path("dashboard/qa/ocr/", views.backend_qa_ocr, name="backend_qa_ocr"),
]

