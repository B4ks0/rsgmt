from django import forms
from django.db.models import Count

from .models import Appointment, ContactMessage, Department, Doctor, ScheduleException


class AppointmentForm(forms.ModelForm):
    is_new_patient = forms.TypedChoiceField(
        coerce=lambda x: x == 'True',
        choices=((False, 'Sudah Pernah'), (True, 'Baru Pertama Kali')),
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
        label="Apakah Anda sudah pernah berobat di RS Gunung Maria Tomohon?"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            base = "form-select" if name in {"department", "doctor"} else "form-control"
            field.widget.attrs.setdefault("class", base)
        self.fields["full_name"].required = True
        self.fields["national_id"].required = True
        self.fields["phone"].required = True
        self.fields["department"].required = True
        self.fields["doctor"].required = True
        self.fields["preferred_date"].required = True
        self.fields["department"].queryset = (
            Department.objects.annotate(active_doctors=Count("doctors"))
            .filter(active_doctors__gt=0, doctors__is_active=True)
            .distinct()
            .order_by("name")
        )
        self.fields["doctor"].queryset = Doctor.objects.filter(is_active=True).select_related("department")

    def clean_preferred_date(self):
        from django.utils import timezone
        date = self.cleaned_data.get("preferred_date")
        if date and date < timezone.now().date():
            raise forms.ValidationError("Tanggal tidak boleh di masa lalu.")
        return date

    def clean_national_id(self):
        national_id = (self.cleaned_data.get("national_id") or "").strip()
        digits = "".join(filter(str.isdigit, national_id))
        if len(digits) != 16:
            raise forms.ValidationError("NIK harus terdiri dari 16 angka.")
        return digits

    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get("department")
        doctor = cleaned_data.get("doctor")
        preferred_date = cleaned_data.get("preferred_date")

        if doctor and department and doctor.department_id != department.id:
            self.add_error("doctor", "Dokter yang dipilih tidak sesuai dengan poli/departemen.")

        if doctor and preferred_date:
            exception = ScheduleException.objects.filter(
                doctor=doctor,
                exception_date=preferred_date,
            ).first()
            if exception and not exception.is_available:
                self.add_error("preferred_date", "Dokter tidak tersedia pada tanggal tersebut.")
            elif not exception:
                has_schedule = doctor.schedules.filter(
                    day_of_week=preferred_date.weekday(),
                    is_active=True,
                ).exists()
                if not has_schedule:
                    self.add_error("preferred_date", "Tanggal yang dipilih tidak sesuai jadwal praktik dokter.")

        return cleaned_data

    class Meta:
        model = Appointment
        fields = [
            "full_name",
            "national_id",
            "phone",
            "email",
            "is_new_patient",
            "ktp_photo",
            "department",
            "doctor",
            "preferred_date",
            "message",
        ]
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "message": forms.Textarea(attrs={"rows": 4}),
        }


class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 5})}


class BackendAppointmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")
    
    class Meta:
        model = Appointment
        fields = "__all__"
        widgets = {
            "appointment_date": forms.DateInput(attrs={"type": "date"}),
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "appointment_time": forms.TimeInput(attrs={"type": "time"}),
            "chief_complaint": forms.Textarea(attrs={"rows": 3}),
            "message": forms.Textarea(attrs={"rows": 3}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

from .models import Doctor, DoctorSchedule
from django.forms import inlineformset_factory

class BackendDoctorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = Doctor
        fields = ["full_name", "department", "specialization", "title", "phone", "email", "license_number", "experience_years", "bio", "photo", "is_active"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
        }

class DoctorScheduleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control form-control-sm")

    def has_changed(self):
        has_changed = super().has_changed()
        day = self.data.get(self.add_prefix('day_of_week'))
        start_time = self.data.get(self.add_prefix('start_time'))
        # Jika hari dan jam mulai kosong (misal pada extra form kosong), anggap tidak ada perubahan
        if not day and not start_time and not self.instance.pk:
            return False
        return has_changed

    class Meta:
        model = DoctorSchedule
        fields = ["day_of_week", "start_time", "end_time", "max_patients", "is_active"]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
        }

DoctorScheduleFormSet = inlineformset_factory(
    Doctor, DoctorSchedule,
    form=DoctorScheduleForm,
    extra=1,
    can_delete=True
)

from .models import Department

class BackendDepartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = Department
        fields = ["name", "icon", "description", "location", "floor_number", "phone"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "icon": forms.TextInput(attrs={"placeholder": "bi-hospital"}),
        }
        labels = {
            "name": "Nama Poli / Departemen",
            "icon": "Icon (Bootstrap Icons class)",
            "description": "Deskripsi Layanan",
            "location": "Lokasi / Gedung",
            "floor_number": "Lantai",
            "phone": "Nomor Telepon",
        }

from .models import Article, Facility, FooterLink, FooterSection, FooterSetting, HomeArticleFeature, McuPackage, News, Partner, Slide

class BackendNewsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = News
        fields = ["title", "slug", "excerpt", "content", "thumbnail", "thumbnail_url", "content_image", "content_image_url", "is_published"]
        widgets = {
            "excerpt": forms.Textarea(attrs={"rows": 3}),
            "content": forms.Textarea(attrs={"rows": 14}),
            "slug": forms.TextInput(attrs={"placeholder": "otomatis-dari-judul"}),
            "thumbnail_url": forms.URLInput(attrs={"placeholder": "https://images.unsplash.com/..."}),
            "content_image_url": forms.URLInput(attrs={"placeholder": "https://..."}),
        }
        labels = {
            "title": "Judul Berita", "slug": "Slug URL",
            "excerpt": "Ringkasan (opsional)", "content": "Isi Konten",
            "thumbnail": "Thumbnail (Upload File)", "thumbnail_url": "Thumbnail URL",
            "content_image": "Gambar dalam Konten (Upload)", "content_image_url": "Gambar dalam Konten (URL)",
            "is_published": "Publikasikan",
        }


class BackendMcuPackageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = McuPackage
        fields = [
            "title", "slug", "excerpt", "content", "price_label", "duration",
            "checklist", "preparation", "thumbnail", "thumbnail_url",
            "content_image", "content_image_url", "order", "is_featured",
            "is_published",
        ]
        widgets = {
            "excerpt": forms.Textarea(attrs={"rows": 3}),
            "content": forms.Textarea(attrs={"rows": 12}),
            "checklist": forms.Textarea(attrs={"rows": 8, "placeholder": "Tulis satu item pemeriksaan per baris"}),
            "preparation": forms.Textarea(attrs={"rows": 6, "placeholder": "Tulis satu instruksi persiapan per baris"}),
            "slug": forms.TextInput(attrs={"placeholder": "otomatis-dari-judul"}),
            "thumbnail_url": forms.URLInput(attrs={"placeholder": "https://images.unsplash.com/..."}),
            "content_image_url": forms.URLInput(attrs={"placeholder": "https://..."}),
        }
        labels = {
            "title": "Nama Paket", "slug": "Slug URL",
            "excerpt": "Ringkasan", "content": "Isi Konten",
            "price_label": "Label Harga", "duration": "Estimasi Durasi",
            "checklist": "Daftar Pemeriksaan", "preparation": "Persiapan Pasien",
            "thumbnail": "Thumbnail (Upload File)", "thumbnail_url": "Thumbnail URL",
            "content_image": "Gambar dalam Konten (Upload)", "content_image_url": "Gambar dalam Konten (URL)",
            "order": "Urutan Tampil", "is_featured": "Jadikan Paket Utama",
            "is_published": "Publikasikan",
        }


class BackendArticleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = Article
        fields = ["title", "slug", "content", "thumbnail", "thumbnail_url", "is_published"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 12}),
            "slug": forms.TextInput(attrs={"placeholder": "otomatis-dari-judul"}),
            "thumbnail_url": forms.URLInput(attrs={"placeholder": "https://images.unsplash.com/..."}),
        }
        labels = {
            "title": "Judul Artikel",
            "slug": "Slug URL",
            "content": "Isi Konten",
            "thumbnail": "Thumbnail (Upload File)",
            "thumbnail_url": "Thumbnail URL (Eksternal)",
            "is_published": "Publikasikan",
        }


class BackendHomeArticleFeatureForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["article"].queryset = Article.objects.filter(is_published=True).order_by("-created_at")
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = HomeArticleFeature
        fields = [
            "is_active", "article", "kicker", "title_override", "excerpt_override",
            "image", "image_url", "primary_label", "primary_url",
            "secondary_label", "secondary_url",
        ]
        widgets = {
            "excerpt_override": forms.Textarea(attrs={"rows": 4, "placeholder": "Kosongkan untuk memakai ringkasan dari artikel terpilih."}),
            "image_url": forms.URLInput(attrs={"placeholder": "https://images.unsplash.com/..."}),
            "primary_url": forms.TextInput(attrs={"placeholder": "Kosongkan untuk otomatis ke detail artikel."}),
            "secondary_url": forms.TextInput(attrs={"placeholder": "/artikel/"}),
        }
        labels = {
            "is_active": "Tampilkan section artikel pilihan",
            "article": "Artikel yang ditampilkan",
            "kicker": "Label kecil di atas judul",
            "title_override": "Judul custom",
            "excerpt_override": "Deskripsi custom",
            "image": "Gambar background (upload)",
            "image_url": "Gambar background URL",
            "primary_label": "Label tombol utama",
            "primary_url": "Custom link tombol utama",
            "secondary_label": "Label tombol kedua",
            "secondary_url": "Link tombol kedua",
        }


class BackendFacilityForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = Facility
        fields = ["name", "icon", "description", "image", "image_url", "order", "is_active"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "image_url": forms.URLInput(attrs={"placeholder": "https://images.unsplash.com/..."}),
            "icon": forms.TextInput(attrs={"placeholder": "bi-building"}),
            "order": forms.NumberInput(attrs={"min": "0"}),
        }
        labels = {
            "name": "Nama Fasilitas",
            "icon": "Icon (Bootstrap Icons class)",
            "description": "Deskripsi",
            "image": "Gambar (Upload File)",
            "image_url": "Gambar URL (Eksternal)",
            "order": "Urutan",
            "is_active": "Aktifkan",
        }


class BackendPartnerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = Partner
        fields = [
            "name", "category", "description", "logo", "logo_url",
            "website_url", "order", "is_featured", "is_active",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "logo_url": forms.URLInput(attrs={"placeholder": "https://... atau /static/hospital/img/kerjasama/logo.png"}),
            "website_url": forms.URLInput(attrs={"placeholder": "https://contoh-mitra.com"}),
            "order": forms.NumberInput(attrs={"min": "0"}),
        }
        labels = {
            "name": "Nama Mitra",
            "category": "Kategori",
            "description": "Deskripsi",
            "logo": "Logo (Upload File)",
            "logo_url": "Logo URL",
            "website_url": "Website Mitra",
            "order": "Urutan",
            "is_featured": "Tampilkan di Sorotan",
            "is_active": "Aktifkan",
        }


class BackendSlideForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = Slide
        fields = ["image", "image_url", "caption", "link_url", "order", "is_active"]
        widgets = {
            "image_url": forms.URLInput(attrs={"placeholder": "https://..."}),
            "link_url": forms.URLInput(attrs={"placeholder": "https://... (opsional)"}),
            "order": forms.NumberInput(attrs={"min": "0"}),
        }
        labels = {
            "image": "Gambar (Upload File)",
            "image_url": "Gambar URL (Eksternal)",
            "caption": "Keterangan / Teks Slide",
            "link_url": "Link URL (klik pada slide)",
            "order": "Urutan",
            "is_active": "Aktifkan Slide",
        }


class BackendFooterSettingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = FooterSetting
        fields = ["site_name", "hospital_code", "tagline", "dashboard_label", "dashboard_url", "show_dashboard_link"]
        widgets = {
            "tagline": forms.Textarea(attrs={"rows": 3}),
            "dashboard_url": forms.TextInput(attrs={"placeholder": "/dashboard/"}),
        }
        labels = {
            "site_name": "Nama Website / Rumah Sakit",
            "hospital_code": "Kode RS",
            "tagline": "Tagline Footer",
            "dashboard_label": "Label Link Dashboard",
            "dashboard_url": "URL Dashboard",
            "show_dashboard_link": "Tampilkan link dashboard di footer",
        }


class BackendFooterSectionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = FooterSection
        fields = ["title", "section_type", "order", "is_active"]
        widgets = {
            "order": forms.NumberInput(attrs={"min": "0"}),
        }
        labels = {
            "title": "Judul Kolom",
            "section_type": "Tipe Section",
            "order": "Urutan Tampil",
            "is_active": "Aktifkan Section",
        }


class BackendFooterLinkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = FooterLink
        fields = ["section", "label", "url", "icon", "order", "is_active", "open_new_tab"]
        widgets = {
            "url": forms.TextInput(attrs={"placeholder": "/about/ atau https://... atau mailto:..."}),
            "icon": forms.TextInput(attrs={"placeholder": "bi-whatsapp"}),
            "order": forms.NumberInput(attrs={"min": "0"}),
        }
        labels = {
            "section": "Section Footer",
            "label": "Label / Teks",
            "url": "Custom Link",
            "icon": "Icon Bootstrap",
            "order": "Urutan Tampil",
            "is_active": "Aktifkan Link",
            "open_new_tab": "Buka di tab baru",
        }


from .models import Patient

class BackendPatientForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")
                
    class Meta:
        model = Patient
        fields = ["full_name", "national_id", "email", "phone", "date_of_birth", "gender", "blood_type", "address"]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "address": forms.Textarea(attrs={"rows": 3}),
        }
