from pathlib import Path
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Count, Q
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import (
    AppointmentForm, BackendAppointmentForm, BackendArticleForm,
    BackendDepartmentForm, BackendDoctorForm, BackendFacilityForm,
    BackendMcuPackageForm, BackendNewsForm, BackendPatientForm,
    BackendPartnerForm, BackendSlideForm, DoctorScheduleFormSet,
)
from .models import (
    Appointment, Article, ContactMessage, Department, Doctor, DoctorSchedule,
    Facility, McuPackage, News, Partner, Patient, Payment, ScheduleException,
    Slide,
)


def logo_png(request):
    logo_path = Path(__file__).resolve().parent.parent / "rsgumato_logo.png"
    if not logo_path.exists():
        raise Http404("Logo not found")
    return FileResponse(logo_path.open("rb"), content_type="image/png")


def title_logo_png(request):
    logo_path = Path(__file__).resolve().parent.parent / "title_logo.png"
    if not logo_path.exists():
        raise Http404("Title logo not found")
    return FileResponse(logo_path.open("rb"), content_type="image/png")


def main_banner(request):
    banner_path = Path(__file__).resolve().parent.parent / "#JanganTungguGejala.png"
    if not banner_path.exists():
        raise Http404("Banner not found")
    return FileResponse(banner_path.open("rb"), content_type="image/png")


_ALLOWED_SLIDESHOW = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10"}

def slideshow_image(request, filename):
    if filename not in _ALLOWED_SLIDESHOW:
        raise Http404("Slideshow image not found")
    img_path = Path(__file__).resolve().parent.parent / "slideshow" / f"{filename}.png"
    if not img_path.exists():
        raise Http404("Slideshow image not found")
    return FileResponse(img_path.open("rb"), content_type="image/png")


_DEPT_INFO = {
    'Anak': {
        'icon': 'bi-balloon-heart',
        'desc': 'Penanganan kesehatan bayi, anak, dan remaja oleh dokter spesialis anak berpengalaman.',
    },
    'Bedah': {
        'icon': 'bi-bandaid',
        'desc': 'Tindakan operasi untuk berbagai kondisi bedah umum secara aman dan terencana.',
    },
    'Bedah Saraf': {
        'icon': 'bi-lightning-charge',
        'desc': 'Operasi pada otak, tulang belakang, dan sistem saraf pusat maupun perifer.',
    },
    'Bedah Urologi': {
        'icon': 'bi-droplet',
        'desc': 'Penanganan gangguan saluran kemih, ginjal, dan organ reproduksi pria.',
    },
    'Forensik & Medikolegal': {
        'icon': 'bi-shield-check',
        'desc': 'Pemeriksaan medis untuk keperluan hukum, visum et repertum, dan medikolegal.',
    },
    'Gigi & Mulut': {
        'icon': 'bi-emoji-smile',
        'desc': 'Perawatan gigi, gusi, rahang, dan kesehatan rongga mulut secara menyeluruh.',
    },
    'Jantung & Pembuluh Darah': {
        'icon': 'bi-heart-pulse',
        'desc': 'Diagnosis dan terapi komprehensif untuk penyakit jantung serta gangguan pembuluh darah.',
    },
    'Kebidanan & Kandungan': {
        'icon': 'bi-person-heart',
        'desc': 'Perawatan kehamilan, persalinan, dan kesehatan sistem reproduksi wanita.',
    },
    'Kulit & Kelamin': {
        'icon': 'bi-brightness-high',
        'desc': 'Diagnosis dan pengobatan penyakit kulit, rambut, kuku, serta infeksi menular seksual.',
    },
    'Mata': {
        'icon': 'bi-eye',
        'desc': 'Pemeriksaan dan pengobatan gangguan penglihatan serta berbagai penyakit mata.',
    },
    'Penyakit Dalam': {
        'icon': 'bi-activity',
        'desc': 'Diagnosis dan penanganan penyakit organ dalam seperti diabetes, hipertensi, dan infeksi.',
    },
    'Rehabilitasi Medik': {
        'icon': 'bi-person-check',
        'desc': 'Program pemulihan fungsi gerak dan kemampuan tubuh pasca cedera atau operasi.',
    },
    'Saraf': {
        'icon': 'bi-lightning',
        'desc': 'Penanganan gangguan sistem saraf seperti stroke, epilepsi, migrain, dan neuropati.',
    },
    'THT': {
        'icon': 'bi-ear',
        'desc': 'Perawatan telinga, hidung, tenggorokan, serta kondisi kepala dan leher terkait.',
    },
    'Umum': {
        'icon': 'bi-hospital',
        'desc': 'Pelayanan medis dasar untuk berbagai keluhan umum dan pemeriksaan kesehatan rutin.',
    },
}

_UNSPLASH = 'https://images.unsplash.com/'
_FACILITIES = [
    {'icon': 'bi-alarm',          'name': 'IGD 24 Jam',       'img': _UNSPLASH + 'photo-1516574187841-cb9cc2ca948b?w=600&h=360&fit=crop&q=80', 'desc': 'Instalasi Gawat Darurat siap melayani kondisi darurat kapan saja, tanpa henti sepanjang hari.'},
    {'icon': 'bi-building',       'name': 'Rawat Inap',        'img': _UNSPLASH + 'photo-1538108149393-fbbd81895907?w=600&h=360&fit=crop&q=80', 'desc': 'Ruang perawatan kelas I, II, dan III yang nyaman dengan tenaga medis siaga penuh.'},
    {'icon': 'bi-calendar-check', 'name': 'Rawat Jalan',       'img': _UNSPLASH + 'photo-1576091160399-112ba8d25d1d?w=600&h=360&fit=crop&q=80', 'desc': 'Layanan poliklinik spesialis untuk konsultasi dan pemeriksaan tanpa perlu menginap.'},
    {'icon': 'bi-graph-up',       'name': 'ICU / ICCU',        'img': 'https://plus.unsplash.com/premium_photo-1661895714925-2c7a6be6be32?q=80&w=387&auto=format&fit=crop', 'desc': 'Unit perawatan intensif dengan monitoring vital sign dan alat bantu hidup 24 jam.'},
    {'icon': 'bi-scissors',       'name': 'Kamar Operasi',     'img': _UNSPLASH + 'photo-1551076805-e1869033e561?w=600&h=360&fit=crop&q=80', 'desc': 'Ruang operasi steril berperalatan modern dengan tim bedah dan anestesi berpengalaman.'},
    {'icon': 'bi-droplet',        'name': 'Laboratorium',      'img': 'https://images.unsplash.com/photo-1602052577122-f73b9710adba?q=80&w=870&auto=format&fit=crop', 'desc': 'Pemeriksaan laboratorium klinik lengkap untuk mendukung diagnosis yang akurat dan cepat.'},
    {'icon': 'bi-camera',         'name': 'Radiologi & USG',   'img': 'https://images.unsplash.com/photo-1666214280352-db292c05fd80?q=80&w=870&auto=format&fit=crop', 'desc': 'Layanan rontgen, ultrasonografi, dan pencitraan diagnostik untuk deteksi yang tepat.'},
    {'icon': 'bi-capsule',        'name': 'Apotek / Farmasi',  'img': 'https://images.unsplash.com/photo-1642055514517-7b52288890ec?q=80&w=774&auto=format&fit=crop', 'desc': 'Apotek rumah sakit dengan ketersediaan obat-obatan lengkap, terjangkau, dan terjamin.'},
    {'icon': 'bi-heart-pulse',    'name': 'Medical Check Up',  'img': 'https://images.unsplash.com/photo-1603807008857-ad66b70431aa?q=80&w=873&auto=format&fit=crop', 'desc': 'Paket pemeriksaan kesehatan menyeluruh untuk deteksi dini penyakit sebelum menjadi serius.'},
    {'icon': 'bi-person-check',   'name': 'Fisioterapi',       'img': _UNSPLASH + 'photo-1571019613454-1cb2f99b2d8b?w=600&h=360&fit=crop&q=80', 'desc': 'Program rehabilitasi gerak dan pemulihan fungsi fisik pasca cedera, operasi, atau stroke.'},
    {'icon': 'bi-truck',          'name': 'Ambulans 24 Jam',   'img': _UNSPLASH + 'photo-1587745416684-47953f16f02f?w=600&h=360&fit=crop&q=80', 'desc': 'Layanan transportasi medis darurat siap menjemput dan mengantar pasien kapan pun.'},
    {'icon': 'bi-shield-check',   'name': 'BPJS & Asuransi',  'img': _UNSPLASH + 'photo-1450101499163-c8848c66ca85?w=600&h=360&fit=crop&q=80', 'desc': 'Melayani pasien BPJS Kesehatan dan berbagai mitra asuransi kesehatan swasta rekanan.'},
]

def home(request):
    departments = Department.objects.all().order_by("name")
    dept_with_doctors = Department.objects.annotate(doc_count=Count('doctors')).filter(doc_count__gt=0).order_by('name')
    clinics = [
        {
            'id': d.id,
            'name': d.name,
            'doc_count': d.doc_count,
            'icon': d.icon or _DEPT_INFO.get(d.name, {}).get('icon', 'bi-hospital'),
            'desc': d.description or _DEPT_INFO.get(d.name, {}).get('desc', 'Layanan medis spesialis untuk penanganan optimal pasien.'),
        }
        for d in dept_with_doctors
    ]
    articles = Article.objects.filter(is_published=True).only('title', 'slug', 'thumbnail', 'thumbnail_url', 'created_at', 'content')[:4]
    news = News.objects.filter(is_published=True).only('title', 'slug', 'thumbnail', 'thumbnail_url', 'created_at', 'excerpt', 'content')[:3]
    slides = list(Slide.objects.filter(is_active=True))
    db_facilities = list(Facility.objects.filter(is_active=True))
    facilities = db_facilities if db_facilities else _FACILITIES
    return render(request, "hospital/home.html", {
        "departments": departments, "clinics": clinics, "facilities": facilities,
        "articles": articles, "news": news, "slides": slides,
    })


def news_list(request):
    all_news = list(News.objects.filter(is_published=True))
    featured  = all_news[0] if all_news else None
    sidebar   = all_news[1:6]
    grid      = all_news[6:]
    return render(request, "hospital/news_list.html", {
        "featured": featured, "sidebar_articles": sidebar, "grid_articles": grid,
    })

def news_detail(request, slug):
    try:
        item = News.objects.get(slug=slug, is_published=True)
    except News.DoesNotExist:
        from django.http import Http404
        raise Http404
    return render(request, "hospital/news_detail.html", {"news": item})

def mcu_package_list(request):
    packages = list(McuPackage.objects.filter(is_published=True))
    featured = next((item for item in packages if item.is_featured), packages[0] if packages else None)
    other_packages = [item for item in packages if item != featured]
    return render(request, "hospital/mcu_packages.html", {
        "featured": featured,
        "packages": packages,
        "other_packages": other_packages,
    })

def mcu_package_detail(request, slug):
    try:
        package = McuPackage.objects.get(slug=slug, is_published=True)
    except McuPackage.DoesNotExist:
        from django.http import Http404
        raise Http404
    related_packages = McuPackage.objects.filter(is_published=True).exclude(pk=package.pk)[:4]
    return render(request, "hospital/mcu_package_detail.html", {
        "package": package,
        "related_packages": related_packages,
    })

def articles_list(request):
    all_articles = list(Article.objects.filter(is_published=True))
    featured   = all_articles[0] if all_articles else None
    sidebar    = all_articles[1:6]
    grid       = all_articles[6:]
    return render(request, "hospital/articles.html", {
        "featured": featured,
        "sidebar_articles": sidebar,
        "grid_articles": grid,
    })

def article_detail(request, slug):
    try:
        article = Article.objects.get(slug=slug, is_published=True)
    except Article.DoesNotExist:
        from django.http import Http404
        raise Http404
    return render(request, "hospital/article_detail.html", {"article": article})

def about(request):
    return render(request, "hospital/about.html")


def mitra_list(request):
    category = request.GET.get("kategori", "").strip()
    partners = Partner.objects.filter(is_active=True)
    if category:
        partners = partners.filter(category=category)
    featured_partners = Partner.objects.filter(is_active=True, is_featured=True)[:8]
    categories = [
        (key, label, Partner.objects.filter(is_active=True, category=key).count())
        for key, label in Partner.CATEGORY_CHOICES
    ]
    return render(request, "hospital/mitra_list.html", {
        "partners": partners,
        "featured_partners": featured_partners,
        "categories": categories,
        "selected_category": category,
    })


def services(request):
    db_facilities = list(Facility.objects.filter(is_active=True))
    if db_facilities:
        facilities = [
            {
                "name": item.name,
                "description": item.description,
                "icon": item.icon,
                "image_src": item.get_image_src(),
            }
            for item in db_facilities
        ]
    else:
        facilities = [
            {
                "name": item["name"],
                "description": item["desc"],
                "icon": item["icon"],
                "image_src": item["img"],
            }
            for item in _FACILITIES
        ]
    return render(request, "hospital/services.html", {"facilities": facilities})


def doctors(request):
    q = request.GET.get('q', '')
    dept_id = request.GET.get('dept', '')
    day_id = request.GET.get('day', '')

    items = Doctor.objects.filter(is_active=True).select_related("department", "specialization").prefetch_related("schedules")
    
    if q:
        items = items.filter(full_name__icontains=q)
    if dept_id:
        items = items.filter(department_id=dept_id)
    if day_id and day_id.isdigit():
        items = items.filter(schedules__day_of_week=int(day_id), schedules__is_active=True)

    items = items.distinct()

    departments = Department.objects.all().order_by("name")
    
    days_choices = [
        (0, 'Senin'), (1, 'Selasa'), (2, 'Rabu'), (3, 'Kamis'),
        (4, 'Jumat'), (5, 'Sabtu'), (6, 'Minggu')
    ]

    total_count = items.count()

    paginator = Paginator(items, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "hospital/doctors.html", {
        "doctors": page_obj,
        "departments": departments,
        "days_choices": days_choices,
        "q": q,
        "selected_dept": dept_id,
        "selected_day": day_id,
        "total_count": total_count,
    })

def doctor_detail(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id, is_active=True)
        # Fetch schedules sorted by day of week
        schedules = doctor.schedules.filter(is_active=True).order_by('day_of_week')
        
        # Day mapping for Indoneisan 
        day_mapping = {
            0: 'Senin', 1: 'Selasa', 2: 'Rabu', 3: 'Kamis', 
            4: 'Jumat', 5: 'Sabtu', 6: 'Minggu'
        }
        
        # Add labels to schedules
        for s in schedules:
            s.day_label = day_mapping.get(s.day_of_week, 'Unknown')
            
        context = {
            'doctor': doctor,
            'schedules': schedules,
        }
        return render(request, "hospital/doctor_detail.html", context)
    except Doctor.DoesNotExist:
        return redirect('doctors')


def appointment_create(request):
    success_flag = False
    if request.method == "POST":
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            request.session['appointment_success'] = True
            return redirect("appointment_create")
    else:
        initial_data = {}
        doctor_id = request.GET.get('doctor')
        success_flag = request.session.pop('appointment_success', False)

        if doctor_id:
            try:
                doctor = Doctor.objects.get(id=doctor_id)
                initial_data['doctor'] = doctor
                initial_data['department'] = doctor.department
            except (Doctor.DoesNotExist, ValueError):
                pass
        form = AppointmentForm(initial=initial_data)
    return render(request, "hospital/appointment_form.html", {"form": form, "is_success": success_flag})


def contact(request):
    """API endpoint for submitting contact form via AJAX"""
    if request.method == "POST":
        try:
            full_name = request.POST.get('full_name', '').strip()
            email = request.POST.get('email', '').strip()
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()
            
            # Validate fields
            if not (full_name and email and subject and message):
                return JsonResponse({'success': False, 'error': 'All fields are required'}, status=400)
            
            # Create and save contact message
            ContactMessage.objects.create(
                full_name=full_name,
                email=email,
                subject=subject,
                message=message
            )
            
            return JsonResponse({'success': True, 'message': 'Contact message saved successfully'})
        except Exception:
            return JsonResponse({'success': False, 'error': 'Terjadi kesalahan server. Silakan coba lagi.'}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)




def is_staff_check(user): return user.is_active and user.is_staff
staff_member_required = user_passes_test(is_staff_check, login_url='backend_login')

def backend_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("backend_dashboard")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                auth_login(request, user)
                next_url = request.GET.get("next", "")
                if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                    return redirect(next_url)
                return redirect("backend_dashboard")
            else:
                messages.error(request, "Akses ditolak. Hubungi Administrator.")
        else:
            messages.error(request, "Username atau password salah.")
    else:
        form = AuthenticationForm()
    return render(request, "hospital/backend/login.html", {"form": form})

def backend_logout(request):
    auth_logout(request)
    messages.info(request, "Anda telah berhasil logout.")
    return redirect("backend_login")

@staff_member_required
def backend_dashboard(request):
    """ Custom Backend Dashboard tailored for Hospital tracking """

    # Get counts without pagination to avoid multiple queries
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='requested').count()
    
    # Get search query & filters
    q = request.GET.get('q', '').strip()
    f_doctor = request.GET.get('doctor', '')
    f_dept = request.GET.get('dept', '')
    f_status = request.GET.get('status', '')
    f_type = request.GET.get('ptype', '')
    
    # Get paginated appointments
    all_appointments = Appointment.objects.select_related("patient", "doctor", "department").order_by("-booked_at")
    
    if q:
        filter_q = (
            Q(patient__full_name__icontains=q) | 
            Q(full_name__icontains=q) | 
            Q(patient__national_id__icontains=q) | 
            Q(national_id__icontains=q) | 
            Q(patient__phone__icontains=q) | 
            Q(phone__icontains=q) | 
            Q(queue_number__icontains=q)
        )
        all_appointments = all_appointments.filter(filter_q)
        
    if f_doctor:
        all_appointments = all_appointments.filter(doctor_id=f_doctor)
    if f_dept:
        all_appointments = all_appointments.filter(department_id=f_dept)
    if f_status:
        all_appointments = all_appointments.filter(status=f_status)
    if f_type == 'new':
        all_appointments = all_appointments.filter(is_new_patient=True)
    elif f_type == 'existing':
        all_appointments = all_appointments.filter(is_new_patient=False)
        
    all_appointments = all_appointments.distinct()
    
    paginator = Paginator(all_appointments, 25)  # Show 25 appointments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Supply lists for dropdowns
    doctors_list = Doctor.objects.filter(is_active=True).order_by('full_name')
    depts_list = Department.objects.all().order_by('name')
    status_choices = Appointment.Status.choices
    
    context = {
        "appointments": page_obj,
        "page_obj": page_obj,
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_appointments": total_appointments,
        "pending_appointments": pending_appointments,
        "q": q,
        "f_doctor": f_doctor,
        "f_dept": f_dept,
        "f_status": f_status,
        "f_type": f_type,
        "doctors_list": doctors_list,
        "depts_list": depts_list,
        "status_choices": status_choices,
    }
    return render(request, "hospital/backend/dashboard.html", context)

@staff_member_required
def backend_update_status(request, appt_id):
    """ Quick AJAX/POST view to update appointment statuses interactively """
    if request.method == "POST":
        new_status = request.POST.get("status")
        try:
            appt = Appointment.objects.get(id=appt_id)
            if new_status in dict(Appointment.Status.choices):
                appt.status = new_status
                appt.save()
                messages.success(request, f"Status janji temu {appt} berhasil diubah menjadi {new_status}.")
        except Appointment.DoesNotExist:
            messages.error(request, "Janji temu tidak ditemukan.")
    return redirect("backend_dashboard")

@staff_member_required
def backend_appointment_add(request):
    if request.method == "POST":
        form = BackendAppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Janji temu baru berhasil ditambahkan.")
            return redirect("backend_dashboard")
    else:
        form = BackendAppointmentForm()
    return render(request, "hospital/backend/appointment_form.html", {"form": form, "title": "Tambah Janji Temu"})

@staff_member_required
def backend_appointment_edit(request, appt_id):
    try:
        appt = Appointment.objects.get(id=appt_id)
    except Appointment.DoesNotExist:
        messages.error(request, "Janji temu tidak ditemukan.")
        return redirect("backend_dashboard")

    if request.method == "POST":
        form = BackendAppointmentForm(request.POST, instance=appt)
        if form.is_valid():
            form.save()
            messages.success(request, "Data janji temu berhasil diperbarui.")
            return redirect("backend_dashboard")
    else:
        form = BackendAppointmentForm(instance=appt)
    return render(request, "hospital/backend/appointment_form.html", {"form": form, "title": "Edit Janji Temu"})

@staff_member_required
def backend_appointment_delete(request, appt_id):
    if request.method == "POST":
        try:
            appt = Appointment.objects.get(id=appt_id)
            appt.delete()
            messages.success(request, "Data janji temu berhasil dihapus.")
        except Appointment.DoesNotExist:
            messages.error(request, "Janji temu tidak ditemukan.")
    return redirect("backend_dashboard")

@staff_member_required
def backend_patient_list(request):
    q = request.GET.get('q', '')
    gender = request.GET.get('gender', '')
    
    items = Patient.objects.all()
    if q:
        items = items.filter(Q(full_name__icontains=q) | Q(national_id__icontains=q) | Q(phone__icontains=q))
    if gender:
        items = items.filter(gender=gender)
        
    items = items.order_by("-created_at")
    
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "hospital/backend/generic_list.html", {
        "items": page_obj,
        "title": "Kelola Pasien", 
        "model_name": "Pasien",
        "q": q,
        "filter_gender": gender
    })

@staff_member_required
def backend_patient_create(request):
    if request.method == "POST":
        form = BackendPatientForm(request.POST)
        if form.is_valid():
            patient = form.save()
            messages.success(request, f"Data pasien baru {patient.full_name} berhasil ditambahkan.")
            return redirect("backend_patient_list")
    else:
        form = BackendPatientForm()
        
    return render(request, "hospital/backend/patient_form.html", {
        "form": form,
        "patient": None,
        "title": "Tambah Pasien Baru"
    })

@staff_member_required
def backend_patient_edit(request, patient_id):
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        messages.error(request, "Pasien tidak ditemukan.")
        return redirect("backend_patient_list")

    if request.method == "POST":
        form = BackendPatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, f"Data pasien {patient.full_name} berhasil diperbarui.")
            return redirect("backend_patient_list")
    else:
        form = BackendPatientForm(instance=patient)
        
    return render(request, "hospital/backend/patient_form.html", {
        "form": form,
        "patient": patient,
        "title": f"Edit Pasien: {patient.full_name}"
    })

@staff_member_required
def backend_doctor_list(request):
    q = request.GET.get('q', '')
    dept_id = request.GET.get('dept', '')
    
    items = Doctor.objects.select_related("department").all()
    if q:
        items = items.filter(Q(full_name__icontains=q) | Q(phone__icontains=q) | Q(specialization__name__icontains=q))
    if dept_id:
        items = items.filter(department_id=dept_id)
        
    items = items.order_by("full_name")
    departments = Department.objects.all().order_by("name")
    
    paginator = Paginator(items, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "hospital/backend/generic_list.html", {
        "items": page_obj,
        "title": "Kelola Dokter", 
        "model_name": "Dokter",
        "q": q,
        "filter_dept": dept_id,
        "departments": departments,
    })
@staff_member_required
def backend_doctor_create(request):
    if request.method == "POST":
        form = BackendDoctorForm(request.POST, request.FILES)
        formset = DoctorScheduleFormSet(request.POST) 
        if form.is_valid():
            try:
                with transaction.atomic():
                    doctor = form.save()
                    formset = DoctorScheduleFormSet(request.POST, instance=doctor)
                    if formset.is_valid():
                        formset.save()
                        messages.success(request, f"Data dokter baru {doctor.full_name} dan jadwalnya berhasil disimpan.")
                        return redirect("backend_doctor_list")
                    else:
                        messages.error(request, "Jadwal tidak valid. Periksa kembali isian jadwal praktik.")
                        raise ValueError("rollback")
            except ValueError:
                pass
    else:
        form = BackendDoctorForm()
        formset = DoctorScheduleFormSet()

    return render(request, "hospital/backend/doctor_form.html", {
        "form": form,
        "formset": formset,
        "doctor": None,
        "title": "Tambah Dokter Baru"
    })

@staff_member_required
def backend_doctor_edit(request, doctor_id):
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        messages.error(request, "Dokter tidak ditemukan.")
        return redirect("backend_doctor_list")

    if request.method == "POST":
        form = BackendDoctorForm(request.POST, request.FILES, instance=doctor)
        formset = DoctorScheduleFormSet(request.POST, instance=doctor)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, f"Data dokter {doctor.full_name} dan jadwalnya berhasil diperbarui.")
            return redirect("backend_doctor_list")
    else:
        form = BackendDoctorForm(instance=doctor)
        formset = DoctorScheduleFormSet(instance=doctor)

    return render(request, "hospital/backend/doctor_form.html", {
        "form": form,
        "formset": formset,
        "doctor": doctor,
        "title": f"Edit Dokter: {doctor.full_name}"
    })

@staff_member_required
def backend_doctor_delete(request, doctor_id):
    if request.method == "POST":
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            name = doctor.full_name
            doctor.delete()
            messages.success(request, f"Data dokter {name} berhasil dihapus permanen.")
        except Doctor.DoesNotExist:
            messages.error(request, "Dokter tidak ditemukan atau sudah dihapus.")
    return redirect("backend_doctor_list")

@staff_member_required
def backend_payment_list(request):
    items = Payment.objects.select_related("appointment").all().order_by("-created_at")
    return render(request, "hospital/backend/generic_list.html", {"items": items, "title": "Pembayaran", "model_name": "Pembayaran"})

@staff_member_required
def backend_department_list(request):
    items = Department.objects.annotate(total_doctors=Count('doctors')).order_by("name")
    
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "hospital/backend/generic_list.html", {"items": page_obj, "title": "Departemen / Poli", "model_name": "Departemen"})

_ICON_CHOICES = [
    'bi-hospital', 'bi-heart-pulse', 'bi-activity', 'bi-bandaid', 'bi-person-heart',
    'bi-eye', 'bi-ear', 'bi-emoji-smile', 'bi-balloon-heart', 'bi-person-check',
    'bi-shield-check', 'bi-lightning', 'bi-lightning-charge', 'bi-brightness-high',
    'bi-droplet', 'bi-scissors', 'bi-person-badge', 'bi-stethoscope', 'bi-capsule',
    'bi-thermometer-half', 'bi-lungs', 'bi-clipboard2-pulse', 'bi-gender-female',
    'bi-gender-male', 'bi-brain', 'bi-bone', 'bi-virus', 'bi-syringe', 'bi-building',
]

@staff_member_required
def backend_department_create(request):
    if request.method == "POST":
        form = BackendDepartmentForm(request.POST)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f"Data poli baru {dept.name} berhasil ditambahkan.")
            return redirect("backend_department_list")
    else:
        form = BackendDepartmentForm()

    return render(request, "hospital/backend/department_form.html", {
        "form": form, "department": None, "doctors": [],
        "title": "Tambah Poli Baru", "icon_choices": _ICON_CHOICES,
    })

@staff_member_required
def backend_department_edit(request, dept_id):
    try:
        dept = Department.objects.get(id=dept_id)
    except Department.DoesNotExist:
        messages.error(request, "Departemen tidak ditemukan.")
        return redirect("backend_department_list")

    if request.method == "POST":
        form = BackendDepartmentForm(request.POST, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, f"Poli {dept.name} berhasil diperbarui.")
            return redirect("backend_department_list")
    else:
        form = BackendDepartmentForm(instance=dept)

    doctors = dept.doctors.all().order_by("full_name")
    return render(request, "hospital/backend/department_form.html", {
        "form": form, "department": dept, "doctors": doctors,
        "title": f"Edit Poli: {dept.name}", "icon_choices": _ICON_CHOICES,
    })


@staff_member_required
def backend_department_delete(request, dept_id):
    try:
        dept = Department.objects.get(id=dept_id)
    except Department.DoesNotExist:
        messages.error(request, "Departemen tidak ditemukan.")
        return redirect("backend_department_list")
    if dept.doctors.exists():
        messages.error(request, f"Poli \"{dept.name}\" tidak bisa dihapus karena masih memiliki {dept.doctors.count()} dokter. Pindahkan atau hapus dokter terlebih dahulu.")
        return redirect("backend_department_list")
    if request.method == "POST":
        dept.delete()
        messages.success(request, f"Poli \"{dept.name}\" berhasil dihapus.")
    return redirect("backend_department_list")


def search_page(request):
    q = request.GET.get('q', '').strip()
    ctx = {'q': q, 'doctors': [], 'departments': [], 'articles': [], 'news': []}
    if len(q) >= 2:
        ctx['doctors'] = Doctor.objects.filter(
            Q(full_name__icontains=q) | Q(department__name__icontains=q), is_active=True
        ).select_related('department')[:8]
        ctx['departments'] = Department.objects.filter(name__icontains=q).annotate(dc=Count('doctors')).filter(dc__gt=0)[:6]
        ctx['articles'] = Article.objects.filter(
            Q(title__icontains=q) | Q(content__icontains=q), is_published=True
        )[:6]
        ctx['news'] = News.objects.filter(
            Q(title__icontains=q) | Q(excerpt__icontains=q), is_published=True
        )[:6]
    return render(request, 'hospital/search.html', ctx)


def api_search(request):
    q = request.GET.get('q', '').strip()
    if len(q) < 2:
        return JsonResponse({'results': [], 'q': q})

    results = []

    # Dokter
    for d in Doctor.objects.filter(
        Q(full_name__icontains=q) | Q(department__name__icontains=q), is_active=True
    ).select_related('department')[:5]:
        results.append({
            'type': 'doctor', 'group': 'Dokter',
            'icon': 'bi-person-badge',
            'title': d.full_name,
            'subtitle': d.department.name if d.department else '',
            'url': f'/doctors/{d.id}/',
        })

    # Klinik / Departemen
    for dept in Department.objects.filter(name__icontains=q).annotate(dc=Count('doctors')).filter(dc__gt=0)[:4]:
        results.append({
            'type': 'clinic', 'group': 'Klinik & Poliklinik',
            'icon': dept.icon or 'bi-hospital',
            'title': dept.name,
            'subtitle': f'{dept.dc} dokter tersedia',
            'url': f'/doctors/?dept={dept.id}',
        })

    # Artikel
    for a in Article.objects.filter(
        Q(title__icontains=q) | Q(content__icontains=q), is_published=True
    )[:4]:
        results.append({
            'type': 'article', 'group': 'Artikel Kesehatan',
            'icon': 'bi-journal-medical',
            'title': a.title,
            'subtitle': a.created_at.strftime('%d %b %Y'),
            'url': f'/artikel/{a.slug}/',
        })

    # Berita
    for n in News.objects.filter(
        Q(title__icontains=q) | Q(excerpt__icontains=q), is_published=True
    )[:4]:
        results.append({
            'type': 'news', 'group': 'Berita',
            'icon': 'bi-megaphone',
            'title': n.title,
            'subtitle': n.created_at.strftime('%d %b %Y'),
            'url': f'/berita/{n.slug}/',
        })

    return JsonResponse({'results': results, 'q': q})


def get_doctors_by_department(request):
    department_id = request.GET.get('department_id', '').strip()
    if not department_id or not department_id.isdigit():
        return JsonResponse({'success': True, 'doctors': []})
    doctors = Doctor.objects.filter(department_id=int(department_id), is_active=True).only('id', 'full_name')
    results = [{'id': str(d.id), 'full_name': d.full_name} for d in doctors]
    return JsonResponse({'success': True, 'doctors': results})

def get_doctor_available_dates(request):
    """Get available dates for a doctor in the next 60 days"""
    
    doctor_id = request.GET.get('doctor_id')
    
    if not doctor_id:
        return JsonResponse({'success': False, 'error': 'doctor_id required'})
    
    try:
        doctor = Doctor.objects.get(id=doctor_id, is_active=True)
    except (Doctor.DoesNotExist, ValidationError, ValueError):
        return JsonResponse({'success': False, 'error': 'Doctor not found'})
    
    # Get doctor's schedules (Monday=0, Sunday=6)
    schedules = doctor.schedules.filter(is_active=True)
    available_days = set(s.day_of_week for s in schedules)
    
    # Generate available dates for next 60 days
    today = timezone.now().date()
    available_dates = []
    
    for i in range(60):
        check_date = today + timedelta(days=i)
        day_of_week = check_date.weekday()  # Monday=0, Sunday=6
        
        # Check if it's a practice day for this doctor
        if day_of_week in available_days:
            # Check for exceptions (override dates)
            exception = ScheduleException.objects.filter(doctor=doctor, exception_date=check_date).first()
            if exception:
                if exception.is_available:
                    available_dates.append(check_date.isoformat())
            else:
                available_dates.append(check_date.isoformat())
                
    photo_path = '/static/hospital/img/default-doctor.png'
    if getattr(doctor, 'photo_url', None):
        photo_path = doctor.photo_url
    elif getattr(doctor, 'photo', None) and hasattr(doctor.photo, 'url'):
        photo_path = doctor.photo.url
        
    doctor_info = {
        'full_name': doctor.full_name,
        'department': doctor.department.name if doctor.department else '',
        'photo_url': photo_path,
    }
    
    return JsonResponse({'success': True, 'available_dates': available_dates, 'doctor_info': doctor_info})


# ── Facility CRUD ─────────────────────────────────────────────────────────

@user_passes_test(lambda u: u.is_staff, login_url='/dashboard/login/')
def backend_facility_list(request):
    facilities = Facility.objects.all()
    return render(request, "hospital/backend/facility_list.html", {"facilities": facilities})


@user_passes_test(lambda u: u.is_staff, login_url='/dashboard/login/')
def backend_facility_create(request):
    if request.method == "POST":
        form = BackendFacilityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Fasilitas berhasil ditambahkan.")
            return redirect("backend_facility_list")
    else:
        form = BackendFacilityForm()
    return render(request, "hospital/backend/facility_form.html", {
        "form": form, "title": "Tambah Fasilitas", "icon_choices": _ICON_CHOICES,
    })


@user_passes_test(lambda u: u.is_staff, login_url='/dashboard/login/')
def backend_facility_edit(request, facility_id):
    try:
        facility = Facility.objects.get(pk=facility_id)
    except Facility.DoesNotExist:
        messages.error(request, "Fasilitas tidak ditemukan.")
        return redirect("backend_facility_list")
    if request.method == "POST":
        form = BackendFacilityForm(request.POST, request.FILES, instance=facility)
        if form.is_valid():
            form.save()
            messages.success(request, "Fasilitas berhasil diperbarui.")
            return redirect("backend_facility_list")
    else:
        form = BackendFacilityForm(instance=facility)
    return render(request, "hospital/backend/facility_form.html", {
        "form": form, "facility": facility, "title": "Edit Fasilitas", "icon_choices": _ICON_CHOICES,
    })


@user_passes_test(lambda u: u.is_staff, login_url='/dashboard/login/')
def backend_facility_delete(request, facility_id):
    try:
        facility = Facility.objects.get(pk=facility_id)
    except Facility.DoesNotExist:
        messages.error(request, "Fasilitas tidak ditemukan.")
        return redirect("backend_facility_list")
    if request.method == "POST":
        facility.delete()
        messages.success(request, "Fasilitas berhasil dihapus.")
    return redirect("backend_facility_list")


# ── Slide (Slideshow) CRUD ─────────────────────────────────────────────────

@user_passes_test(lambda u: u.is_staff, login_url='/dashboard/login/')
def backend_slide_list(request):
    slides = Slide.objects.all()
    return render(request, "hospital/backend/slide_list.html", {"slides": slides})


@user_passes_test(lambda u: u.is_staff, login_url='/dashboard/login/')
def backend_slide_create(request):
    if request.method == "POST":
        form = BackendSlideForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Slide berhasil ditambahkan.")
            return redirect("backend_slide_list")
    else:
        form = BackendSlideForm()
    return render(request, "hospital/backend/slide_form.html", {"form": form, "title": "Tambah Slide"})


@user_passes_test(lambda u: u.is_staff, login_url='/dashboard/login/')
def backend_slide_edit(request, slide_id):
    try:
        slide = Slide.objects.get(pk=slide_id)
    except Slide.DoesNotExist:
        messages.error(request, "Slide tidak ditemukan.")
        return redirect("backend_slide_list")
    if request.method == "POST":
        form = BackendSlideForm(request.POST, request.FILES, instance=slide)
        if form.is_valid():
            form.save()
            messages.success(request, "Slide berhasil diperbarui.")
            return redirect("backend_slide_list")
    else:
        form = BackendSlideForm(instance=slide)
    return render(request, "hospital/backend/slide_form.html", {"form": form, "slide": slide, "title": "Edit Slide"})


@user_passes_test(lambda u: u.is_staff, login_url='/dashboard/login/')
def backend_slide_delete(request, slide_id):
    try:
        slide = Slide.objects.get(pk=slide_id)
    except Slide.DoesNotExist:
        messages.error(request, "Slide tidak ditemukan.")
        return redirect("backend_slide_list")
    if request.method == "POST":
        slide.delete()
        messages.success(request, "Slide berhasil dihapus.")
    return redirect("backend_slide_list")


@user_passes_test(lambda u: u.is_staff, login_url='/dashboard/login/')
def backend_slide_download(request, slide_id):
    import urllib.request as urlreq
    from django.http import HttpResponse
    try:
        slide = Slide.objects.get(pk=slide_id)
    except Slide.DoesNotExist:
        raise Http404
    if slide.image:
        file_path = slide.image.path
        ext = Path(file_path).suffix.lower() or '.png'
        filename = f"slide-{slide.pk}{ext}"
        response = FileResponse(open(file_path, 'rb'), content_type='image/png', as_attachment=True)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    elif slide.image_url:
        try:
            with urlreq.urlopen(slide.image_url, timeout=10) as r:
                data = r.read()
                content_type = r.headers.get('Content-Type', 'image/jpeg')
        except Exception:
            raise Http404("Gambar tidak bisa diunduh.")
        ext = '.jpg'
        if 'png' in content_type:
            ext = '.png'
        elif 'webp' in content_type:
            ext = '.webp'
        filename = f"slide-{slide.pk}{ext}"
        response = HttpResponse(data, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    raise Http404("Slide tidak memiliki gambar.")

@staff_member_required
def backend_queue_list(request):
    from django.utils import timezone as tz
    from datetime import date as date_type

    date_str = request.GET.get('date', tz.localdate().isoformat())
    doctor_id = request.GET.get('doctor', '')
    try:
        filter_date = date_type.fromisoformat(date_str)
    except ValueError:
        filter_date = tz.localdate()

    base_qs = (
        Appointment.objects
        .filter(status__in=['requested', 'confirmed'])
        .filter(Q(appointment_date=filter_date) | Q(preferred_date=filter_date))
        .select_related('patient', 'doctor', 'doctor__department')
    )
    if doctor_id:
        base_qs = base_qs.filter(doctor_id=doctor_id)

    all_appts = list(base_qs.order_by('queue_number', 'booked_at'))

    # Pisahkan: belum bernomor vs sudah bernomor
    unassigned = [a for a in all_appts if not a.queue_number]
    assigned   = [a for a in all_appts if a.queue_number]

    stats = {
        'total':      len(all_appts),
        'unassigned': len(unassigned),
        'active':     len([a for a in assigned if a.queue_status not in ('done', 'absent')]),
        'done':       len([a for a in assigned if a.queue_status in ('done', 'absent')]),
    }

    doctors_list = Doctor.objects.filter(is_active=True).order_by('full_name')
    return render(request, "hospital/backend/queue_management.html", {
        "appointments": all_appts,
        "unassigned": unassigned,
        "assigned": assigned,
        "stats": stats,
        "filter_date": filter_date,
        "filter_doctor": doctor_id,
        "doctors_list": doctors_list,
    })

@staff_member_required
def backend_queue_assign(request, appt_id):
    """Assign queue number + update status via AJAX POST."""
    if request.method == "POST":
        try:
            appt = Appointment.objects.get(id=appt_id)
            queue_number = request.POST.get('queue_number', '').strip()
            queue_status = request.POST.get('queue_status', 'waiting')
            if queue_number:
                appt.queue_number = queue_number
            if queue_status in dict(Appointment.QUEUE_STATUS_CHOICES):
                appt.queue_status = queue_status
            if appt.status == 'requested' and queue_number:
                appt.status = 'confirmed'
            appt.save(update_fields=['queue_number', 'queue_status', 'status'])
            return JsonResponse({
                'success': True,
                'queue_number': appt.queue_number,
                'queue_status': appt.queue_status,
                'queue_status_label': dict(Appointment.QUEUE_STATUS_CHOICES).get(appt.queue_status, ''),
                'wa_url': appt.get_queue_whatsapp_url,
            })
        except Appointment.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Tidak ditemukan'}, status=404)
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)

def queue_check(request):
    result = None
    phone_query = ''
    if request.GET.get('phone'):
        phone_query = request.GET.get('phone', '').strip()
        clean = ''.join(filter(str.isdigit, phone_query))
        appts = Appointment.objects.filter(
            status__in=['requested', 'confirmed', 'completed']
        ).filter(
            Q(patient__phone__icontains=clean) |
            Q(phone__icontains=clean) |
            Q(patient__phone__icontains=phone_query) |
            Q(phone__icontains=phone_query)
        ).select_related('patient', 'doctor', 'doctor__department').order_by('-booked_at')[:5]
        result = list(appts)
    return render(request, "hospital/queue_check.html", {
        "result": result,
        "phone_query": phone_query,
    })

@staff_member_required
def backend_news_list(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    items = News.objects.all()
    if q:
        items = items.filter(title__icontains=q)
    if status == 'published':
        items = items.filter(is_published=True)
    elif status == 'draft':
        items = items.filter(is_published=False)
    paginator = Paginator(items.order_by('-created_at'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, "hospital/backend/news_list.html", {
        "news_list": page_obj, "q": q, "status": status,
    })

@staff_member_required
def backend_news_create(request):
    if request.method == "POST":
        form = BackendNewsForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save()
            messages.success(request, f"Berita \"{item.title}\" berhasil ditambahkan.")
            return redirect("backend_news_list")
    else:
        form = BackendNewsForm()
    return render(request, "hospital/backend/news_form.html", {"form": form, "news": None, "title": "Tambah Berita Baru"})

@staff_member_required
def backend_news_edit(request, news_id):
    try:
        item = News.objects.get(id=news_id)
    except News.DoesNotExist:
        messages.error(request, "Berita tidak ditemukan.")
        return redirect("backend_news_list")
    if request.method == "POST":
        form = BackendNewsForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, f"Berita \"{item.title}\" berhasil diperbarui.")
            return redirect("backend_news_list")
    else:
        form = BackendNewsForm(instance=item)
    return render(request, "hospital/backend/news_form.html", {"form": form, "news": item, "title": f"Edit: {item.title}"})

@staff_member_required
def backend_news_delete(request, news_id):
    if request.method == "POST":
        try:
            item = News.objects.get(id=news_id)
            title = item.title
            item.delete()
            messages.success(request, f"Berita \"{title}\" berhasil dihapus.")
        except News.DoesNotExist:
            messages.error(request, "Berita tidak ditemukan.")
    return redirect("backend_news_list")

@staff_member_required
def backend_mcu_package_list(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    items = McuPackage.objects.all()
    if q:
        items = items.filter(Q(title__icontains=q) | Q(checklist__icontains=q))
    if status == 'published':
        items = items.filter(is_published=True)
    elif status == 'draft':
        items = items.filter(is_published=False)
    paginator = Paginator(items.order_by('order', '-created_at'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, "hospital/backend/mcu_package_list.html", {
        "packages": page_obj, "q": q, "status": status,
    })

@staff_member_required
def backend_mcu_package_create(request):
    if request.method == "POST":
        form = BackendMcuPackageForm(request.POST, request.FILES)
        if form.is_valid():
            package = form.save()
            messages.success(request, f"Paket MCU \"{package.title}\" berhasil ditambahkan.")
            return redirect("backend_mcu_package_list")
    else:
        form = BackendMcuPackageForm()
    return render(request, "hospital/backend/mcu_package_form.html", {
        "form": form, "package": None, "title": "Tambah Paket MCU",
    })

@staff_member_required
def backend_mcu_package_edit(request, package_id):
    try:
        package = McuPackage.objects.get(id=package_id)
    except McuPackage.DoesNotExist:
        messages.error(request, "Paket MCU tidak ditemukan.")
        return redirect("backend_mcu_package_list")
    if request.method == "POST":
        form = BackendMcuPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            messages.success(request, f"Paket MCU \"{package.title}\" berhasil diperbarui.")
            return redirect("backend_mcu_package_list")
    else:
        form = BackendMcuPackageForm(instance=package)
    return render(request, "hospital/backend/mcu_package_form.html", {
        "form": form, "package": package, "title": f"Edit: {package.title}",
    })

@staff_member_required
def backend_mcu_package_delete(request, package_id):
    if request.method == "POST":
        try:
            package = McuPackage.objects.get(id=package_id)
            title = package.title
            package.delete()
            messages.success(request, f"Paket MCU \"{title}\" berhasil dihapus.")
        except McuPackage.DoesNotExist:
            messages.error(request, "Paket MCU tidak ditemukan.")
    return redirect("backend_mcu_package_list")

@staff_member_required
def backend_partner_list(request):
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()
    status = request.GET.get('status', '')
    items = Partner.objects.all()
    if q:
        items = items.filter(Q(name__icontains=q) | Q(description__icontains=q))
    if category:
        items = items.filter(category=category)
    if status == 'active':
        items = items.filter(is_active=True)
    elif status == 'inactive':
        items = items.filter(is_active=False)
    paginator = Paginator(items.order_by('order', 'name'), 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, "hospital/backend/partner_list.html", {
        "partners": page_obj,
        "q": q,
        "category": category,
        "status": status,
        "category_choices": Partner.CATEGORY_CHOICES,
    })

@staff_member_required
def backend_partner_create(request):
    if request.method == "POST":
        form = BackendPartnerForm(request.POST, request.FILES)
        if form.is_valid():
            partner = form.save()
            messages.success(request, f"Mitra \"{partner.name}\" berhasil ditambahkan.")
            return redirect("backend_partner_list")
    else:
        form = BackendPartnerForm()
    return render(request, "hospital/backend/partner_form.html", {
        "form": form, "partner": None, "title": "Tambah Mitra",
    })

@staff_member_required
def backend_partner_edit(request, partner_id):
    try:
        partner = Partner.objects.get(id=partner_id)
    except Partner.DoesNotExist:
        messages.error(request, "Mitra tidak ditemukan.")
        return redirect("backend_partner_list")
    if request.method == "POST":
        form = BackendPartnerForm(request.POST, request.FILES, instance=partner)
        if form.is_valid():
            form.save()
            messages.success(request, f"Mitra \"{partner.name}\" berhasil diperbarui.")
            return redirect("backend_partner_list")
    else:
        form = BackendPartnerForm(instance=partner)
    return render(request, "hospital/backend/partner_form.html", {
        "form": form, "partner": partner, "title": f"Edit: {partner.name}",
    })

@staff_member_required
def backend_partner_delete(request, partner_id):
    if request.method == "POST":
        try:
            partner = Partner.objects.get(id=partner_id)
            name = partner.name
            partner.delete()
            messages.success(request, f"Mitra \"{name}\" berhasil dihapus.")
        except Partner.DoesNotExist:
            messages.error(request, "Mitra tidak ditemukan.")
    return redirect("backend_partner_list")

@staff_member_required
def backend_article_list(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    items = Article.objects.all()
    if q:
        items = items.filter(title__icontains=q)
    if status == 'published':
        items = items.filter(is_published=True)
    elif status == 'draft':
        items = items.filter(is_published=False)
    paginator = Paginator(items.order_by('-created_at'), 10)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, "hospital/backend/article_list.html", {
        "articles": page_obj, "q": q, "status": status,
    })

@staff_member_required
def backend_article_create(request):
    if request.method == "POST":
        form = BackendArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save()
            messages.success(request, f"Artikel \"{article.title}\" berhasil ditambahkan.")
            return redirect("backend_article_list")
    else:
        form = BackendArticleForm()
    return render(request, "hospital/backend/article_form.html", {"form": form, "article": None, "title": "Tambah Artikel Baru"})

@staff_member_required
def backend_article_edit(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
    except Article.DoesNotExist:
        messages.error(request, "Artikel tidak ditemukan.")
        return redirect("backend_article_list")
    if request.method == "POST":
        form = BackendArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, f"Artikel \"{article.title}\" berhasil diperbarui.")
            return redirect("backend_article_list")
    else:
        form = BackendArticleForm(instance=article)
    return render(request, "hospital/backend/article_form.html", {"form": form, "article": article, "title": f"Edit: {article.title}"})

@staff_member_required
def backend_article_delete(request, article_id):
    if request.method == "POST":
        try:
            article = Article.objects.get(id=article_id)
            title = article.title
            article.delete()
            messages.success(request, f"Artikel \"{title}\" berhasil dihapus.")
        except Article.DoesNotExist:
            messages.error(request, "Artikel tidak ditemukan.")
    return redirect("backend_article_list")

@staff_member_required
def backend_contact_list(request):

    q = request.GET.get('q', '').strip()[:100]  # Limit to 100 chars to prevent DoS
    status = request.GET.get('status', '').strip()
    
    # Load only the fields needed for the list view
    items = ContactMessage.objects.all().only('id', 'full_name', 'email', 'subject', 'created_at', 'is_resolved')
    
    if q:
        items = items.filter(Q(full_name__icontains=q) | Q(email__icontains=q) | Q(subject__icontains=q))
    
    if status == 'resolved':
        items = items.filter(is_resolved=True)
    elif status == 'unresolved':
        items = items.filter(is_resolved=False)
    
    items = items.order_by("-created_at")

    # Pagination without converting to list (avoids memory issue)
    try:
        page = int(request.GET.get('page', '1'))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1

    page_size = 10
    offset = (page - 1) * page_size

    # Fetch one extra to detect if there's a next page without .count()
    page_items = items[offset:offset + page_size + 1]
    page_list = list(page_items)  # ONLY the current page items, not entire dataset
    
    has_next = len(page_list) > page_size
    contacts = page_list[:page_size]
    has_previous = page > 1

    return render(request, "hospital/backend/contact_list.html", {
        "contacts": contacts,
        "title": "Pesan Kontak Masuk",
        "q": q,
        "status": status,
        "page": page,
        "has_next": has_next,
        "has_previous": has_previous,
        "next_page": page + 1,
        "previous_page": page - 1,
        "page_size": page_size,
    })


@staff_member_required
def backend_contact_detail(request, contact_id):
    """Return contact message details as JSON for modal loading to avoid fetching large text in list queries."""
    try:
        cm = ContactMessage.objects.get(id=contact_id)
        return JsonResponse({
            'success': True,
            'id': cm.id,
            'full_name': cm.full_name,
            'email': cm.email,
            'subject': cm.subject,
            'message': cm.message,
            'created_at': cm.created_at.strftime('%d %b %Y, %H:%M'),
            'is_resolved': cm.is_resolved,
        })
    except ContactMessage.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Not found'}, status=404)
