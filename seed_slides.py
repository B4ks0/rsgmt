"""
Seed script: migrates static slideshow images into the Slide model.
Run once on a fresh install: python seed_slides.py
"""
import os, shutil, django
from pathlib import Path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from hospital.models import Slide

slides_media = Path(settings.MEDIA_ROOT) / 'slides'
slides_media.mkdir(parents=True, exist_ok=True)

src_dir = Path(settings.BASE_DIR) / 'slideshow'

for i in range(1, 6):
    src = src_dir / f'{i}.png'
    if not src.exists():
        print(f'skip: {src} tidak ada')
        continue

    dst_name = f'static_slide_{i}.png'
    dst = slides_media / dst_name
    shutil.copy2(src, dst)

    slide, created = Slide.objects.get_or_create(
        image='slides/' + dst_name,
        defaults={'order': i, 'is_active': True},
    )
    status = 'dibuat' if created else 'sudah ada'
    print(f'Slide #{i}: {status} -> media/slides/{dst_name}')
