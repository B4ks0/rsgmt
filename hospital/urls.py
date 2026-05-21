from django.urls import path

from . import views


urlpatterns = [
    path("assets/logo.png", views.logo_png, name="logo_png"),
    path("assets/title-logo.png", views.title_logo_png, name="title_logo_png"),
    path("assets/banner-main", views.main_banner, name="main_banner"),
    path("assets/slideshow/<str:filename>.png", views.slideshow_image, name="slideshow_image"),
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("berita/", views.news_list, name="news_list"),
    path("berita/<slug:slug>/", views.news_detail, name="news_detail"),
    path("artikel/", views.articles_list, name="articles_list"),
    path("artikel/<slug:slug>/", views.article_detail, name="article_detail"),
    path("mitra/", views.mitra_list, name="mitra_list"),
    path("services/", views.services, name="services"),
    path("doctors/", views.doctors, name="doctors"),
    path("doctors/<uuid:doctor_id>/", views.doctor_detail, name="doctor_detail"),
    path("appointments/", views.appointment_create, name="appointment_create"),
    
    # API endpoints
    path("search/", views.search_page, name="search"),
    path("api/search/", views.api_search, name="api_search"),
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
    path("cek-antrian/", views.queue_check, name="queue_check"),
    path("dashboard/antrian/", views.backend_queue_list, name="backend_queue_list"),
    path("dashboard/antrian/<uuid:appt_id>/assign/", views.backend_queue_assign, name="backend_queue_assign"),
    path("dashboard/news/", views.backend_news_list, name="backend_news_list"),
    path("dashboard/news/add/", views.backend_news_create, name="backend_news_create"),
    path("dashboard/news/<int:news_id>/edit/", views.backend_news_edit, name="backend_news_edit"),
    path("dashboard/news/<int:news_id>/delete/", views.backend_news_delete, name="backend_news_delete"),
    path("dashboard/articles/", views.backend_article_list, name="backend_article_list"),
    path("dashboard/articles/add/", views.backend_article_create, name="backend_article_create"),
    path("dashboard/articles/<int:article_id>/edit/", views.backend_article_edit, name="backend_article_edit"),
    path("dashboard/articles/<int:article_id>/delete/", views.backend_article_delete, name="backend_article_delete"),
    path("dashboard/contacts/", views.backend_contact_list, name="backend_contact_list"),
    path("dashboard/contacts/<int:contact_id>/detail/", views.backend_contact_detail, name="backend_contact_detail"),
    path("dashboard/departments/", views.backend_department_list, name="backend_department_list"),
    path("dashboard/departments/add/", views.backend_department_create, name="backend_department_create"),
    path("dashboard/departments/<int:dept_id>/edit/", views.backend_department_edit, name="backend_department_edit"),
    path("dashboard/departments/<int:dept_id>/delete/", views.backend_department_delete, name="backend_department_delete"),

    # Fasilitas
    path("dashboard/facilities/", views.backend_facility_list, name="backend_facility_list"),
    path("dashboard/facilities/add/", views.backend_facility_create, name="backend_facility_create"),
    path("dashboard/facilities/<int:facility_id>/edit/", views.backend_facility_edit, name="backend_facility_edit"),
    path("dashboard/facilities/<int:facility_id>/delete/", views.backend_facility_delete, name="backend_facility_delete"),

    # Slideshow
    path("dashboard/slides/", views.backend_slide_list, name="backend_slide_list"),
    path("dashboard/slides/add/", views.backend_slide_create, name="backend_slide_create"),
    path("dashboard/slides/<int:slide_id>/edit/", views.backend_slide_edit, name="backend_slide_edit"),
    path("dashboard/slides/<int:slide_id>/delete/", views.backend_slide_delete, name="backend_slide_delete"),
    path("dashboard/slides/<int:slide_id>/download/", views.backend_slide_download, name="backend_slide_download"),
]

