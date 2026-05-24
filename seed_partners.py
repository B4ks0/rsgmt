import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from hospital.models import Partner


partners = [
    ("AIA", "insurance", "35_logo_aia.png", True),
    ("AdMedika", "insurance", "admedika-logo.png", True),
    ("Allianz", "insurance", "Allianz.svg.png", True),
    ("BPJS Kesehatan", "insurance", "bpjs-kes-removebg-preview.png", True),
    ("TASPEN", "institution", "detail-logo-taspen-png-hd_237-design.png", True),
    ("FMIPA UKIT", "education", "fmipa ukit.png", False),
    ("Jasa Raharja", "institution", "Logo Jasa Raharja.png", True),
    ("Lippo Insurance", "insurance", "logo lippo insurance.png", False),
    ("Fullerton Health", "insurance", "logo-fullerton-health-removebg-preview.png", True),
    ("Universitas Negeri Manado", "education", "Logo-Unima-2023.png", False),
    ("Palang Merah Indonesia", "institution", "palang merah - indonesia.png", False),
    ("PLN", "corporate", "pln-2016-1280x-q95.png", False),
    ("Mandiri Inhealth", "insurance", "PRIMARY LOGO Mandiri Inhealth-01 PNG.png", True),
    ("STIKES Gunung Maria", "education", "Stikes gunung maria.png", False),
    ("Telkom Indonesia", "corporate", "Telkom_Indonesia_logo.png", False),
    ("Unika De La Salle Manado", "education", "unika de la salle manado.png", False),
]


created = 0
updated = 0
for index, (name, category, filename, is_featured) in enumerate(partners, start=1):
    defaults = {
        "category": category,
        "description": "",
        "logo_url": f"/static/hospital/img/kerjasama/{filename}",
        "order": index,
        "is_featured": is_featured,
        "is_active": True,
    }
    obj, is_new = Partner.objects.update_or_create(name=name, defaults=defaults)
    if is_new:
        created += 1
        print(f"  [+] {obj.name}")
    else:
        updated += 1
        print(f"  [=] diperbarui: {obj.name}")

print(f"\nSelesai: {created} mitra baru, {updated} mitra diperbarui, total seed {len(partners)}.")
