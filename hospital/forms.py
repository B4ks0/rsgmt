from django import forms

from .models import Appointment, ContactMessage


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
        self.fields["doctor"].required = True
        self.fields["preferred_date"].required = True

    def clean_preferred_date(self):
        from django.utils import timezone
        date = self.cleaned_data.get("preferred_date")
        if date and date < timezone.now().date():
            raise forms.ValidationError("Tanggal tidak boleh di masa lalu.")
        return date

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
        fields = ["name", "location", "floor_number", "phone", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

from .models import Article, News, Slide

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
