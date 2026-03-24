from pathlib import Path

from django.contrib import messages
from django.http import FileResponse, Http404
from django.shortcuts import redirect, render

from .forms import AppointmentForm
from .models import Doctor, Department


def logo_png(request):
    logo_path = Path(__file__).resolve().parent.parent / "rsgumato_logo.png"
    if not logo_path.exists():
        raise Http404("Logo not found")
    return FileResponse(open(logo_path, "rb"), content_type="image/png")


def title_logo_png(request):
    logo_path = Path(__file__).resolve().parent.parent / "title_logo.png"
    if not logo_path.exists():
        raise Http404("Title logo not found")
    return FileResponse(open(logo_path, "rb"), content_type="image/png")


def main_banner(request):
    banner_path = Path(__file__).resolve().parent.parent / "#JanganTungguGejala.png"
    if not banner_path.exists():
        raise Http404("Banner not found")
    return FileResponse(open(banner_path, "rb"), content_type="image/png")


def slideshow_image(request, filename):
    img_path = Path(__file__).resolve().parent.parent / "slideshow" / f"{filename}.png"
    if not img_path.exists():
        raise Http404("Slideshow image not found")
    return FileResponse(open(img_path, "rb"), content_type="image/png")


def home(request):
    departments = Department.objects.all().order_by("name")
    return render(request, "hospital/home.html", {"departments": departments})


def about(request):
    return render(request, "hospital/about.html")


def services(request):
    return render(request, "hospital/services.html")


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

    from .models import Department
    departments = Department.objects.all().order_by("name")
    
    days_choices = [
        (0, 'Senin'), (1, 'Selasa'), (2, 'Rabu'), (3, 'Kamis'),
        (4, 'Jumat'), (5, 'Sabtu'), (6, 'Minggu')
    ]

    total_count = items.count()

    from django.core.paginator import Paginator
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
    if request.method == "POST":
        form = AppointmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Permintaan janji temu berhasil dikirim. Tim kami akan menghubungi Anda untuk konfirmasi.",
            )
            return redirect("appointment_create")
    else:
        initial_data = {}
        doctor_id = request.GET.get('doctor')
        if doctor_id:
            try:
                from .models import Doctor
                doctor = Doctor.objects.get(id=doctor_id)
                initial_data['doctor'] = doctor
                initial_data['department'] = doctor.department
            except:
                pass
        form = AppointmentForm(initial=initial_data)
    return render(request, "hospital/appointment_form.html", {"form": form})


def contact(request):
    """API endpoint for submitting contact form via AJAX"""
    if request.method == "POST":
        from django.http import JsonResponse
        try:
            full_name = request.POST.get('full_name', '').strip()
            email = request.POST.get('email', '').strip()
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()
            
            # Validate fields
            if not (full_name and email and subject and message):
                return JsonResponse({'success': False, 'error': 'All fields are required'}, status=400)
            
            # Create and save contact message
            from .models import ContactMessage
            ContactMessage.objects.create(
                full_name=full_name,
                email=email,
                subject=subject,
                message=message
            )
            
            return JsonResponse({'success': True, 'message': 'Contact message saved successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)



from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login as auth_login, logout as auth_logout
from .models import Appointment, Patient, Doctor

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
                return redirect(request.GET.get("next", "backend_dashboard"))
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
    from django.core.paginator import Paginator
    
    # Get counts without pagination to avoid multiple queries
    total_patients = Patient.objects.count()
    total_doctors = Doctor.objects.count()
    total_appointments = Appointment.objects.count()
    pending_appointments = Appointment.objects.filter(status='requested').count()
    
    # Get paginated appointments
    all_appointments = Appointment.objects.select_related("patient", "doctor", "department").order_by("-booked_at")
    
    paginator = Paginator(all_appointments, 25)  # Show 25 appointments per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        "appointments": page_obj,
        "page_obj": page_obj,
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "total_appointments": total_appointments,
        "pending_appointments": pending_appointments,
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

from .forms import BackendAppointmentForm

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

from .models import Payment, Department

@staff_member_required
def backend_patient_list(request):
    from django.db.models import Q
    q = request.GET.get('q', '')
    gender = request.GET.get('gender', '')
    
    items = Patient.objects.all()
    if q:
        items = items.filter(Q(full_name__icontains=q) | Q(national_id__icontains=q) | Q(phone__icontains=q))
    if gender:
        items = items.filter(gender=gender)
        
    items = items.order_by("-created_at")
    
    from django.core.paginator import Paginator
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

from .forms import BackendPatientForm

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

from .forms import BackendDoctorForm, DoctorScheduleFormSet

@staff_member_required
def backend_doctor_list(request):
    from django.db.models import Q
    q = request.GET.get('q', '')
    dept_id = request.GET.get('dept', '')
    
    items = Doctor.objects.select_related("department").all()
    if q:
        items = items.filter(Q(full_name__icontains=q) | Q(phone__icontains=q) | Q(specialization__name__icontains=q))
    if dept_id:
        items = items.filter(department_id=dept_id)
        
    items = items.order_by("full_name")
    departments = Department.objects.all().order_by("name")
    
    from django.core.paginator import Paginator
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
from django.db import transaction

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
                        raise ValueError("Formset invalid") # triggers rollback to not save partial
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

from django.db.models import Count

@staff_member_required
def backend_department_list(request):
    items = Department.objects.annotate(total_doctors=Count('doctors')).order_by("name")
    
    from django.core.paginator import Paginator
    paginator = Paginator(items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "hospital/backend/generic_list.html", {"items": page_obj, "title": "Departemen / Poli", "model_name": "Departemen"})

from .forms import BackendDepartmentForm

@staff_member_required
def backend_department_create(request):
    if request.method == "POST":
        form = BackendDepartmentForm(request.POST, request.FILES)
        if form.is_valid():
            dept = form.save()
            messages.success(request, f"Data poli baru {dept.name} berhasil ditambahkan.")
            return redirect("backend_department_list")
    else:
        form = BackendDepartmentForm()

    return render(request, "hospital/backend/department_form.html", {
        "form": form,
        "department": None,
        "doctors": [],
        "title": "Tambah Poli Baru"
    })

@staff_member_required
def backend_department_edit(request, dept_id):
    try:
        dept = Department.objects.get(id=dept_id)
    except Department.DoesNotExist:
        messages.error(request, "Departemen tidak ditemukan.")
        return redirect("backend_department_list")
        
    if request.method == "POST":
        form = BackendDepartmentForm(request.POST, request.FILES, instance=dept)
        if form.is_valid():
            form.save()
            messages.success(request, f"Poli {dept.name} berhasil diperbarui.")
            return redirect("backend_department_list")
    else:
        form = BackendDepartmentForm(instance=dept)
        
    doctors = dept.doctors.all().order_by("full_name")
    
    return render(request, "hospital/backend/department_form.html", {
        "form": form,
        "department": dept,
        "doctors": doctors,
        "title": f"Edit Poli: {dept.name}"
    })


def get_doctors_by_department(request):
    department_id = request.GET.get('department_id')
    doctors = Doctor.objects.filter(department_id=department_id, is_active=True)
    results = [{'id': str(d.id), 'full_name': d.full_name} for d in doctors]
    return JsonResponse({'success': True, 'doctors': results})

def get_doctor_available_dates(request):
    """Get available dates for a doctor in the next 60 days"""
    from datetime import datetime, timedelta
    from .models import ScheduleException
    
    doctor_id = request.GET.get('doctor_id')
    
    if not doctor_id:
        return JsonResponse({'success': False, 'error': 'doctor_id required'})
    
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Doctor not found'})
    
    # Get doctor's schedules
    schedules = doctor.schedules.filter(is_active=True)
    available_days = set(s.day_of_week for s in schedules)
    
    # Generate available dates for next 60 days
    today = datetime.now().date()
    available_dates = []
    
    for i in range(60):
        check_date = today + timedelta(days=i)
        day_of_week = check_date.weekday()
        
        # Check if it's a practice day for this doctor
        if day_of_week in available_days:
            # Check for exceptions
            exception = ScheduleException.objects.filter(doctor=doctor, exception_date=check_date).first()
            if exception:
                if exception.is_available:
                    available_dates.append(check_date.isoformat())
            else:
                available_dates.append(check_date.isoformat())
    
    return JsonResponse({'success': True, 'available_dates': available_dates})

@staff_member_required
def backend_contact_list(request):
    from django.db.models import Q
    from .models import ContactMessage
    
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
    from .models import ContactMessage
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
