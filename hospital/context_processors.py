from django.conf import settings
from django.db import OperationalError, ProgrammingError

from .models import FooterSection, FooterSetting


def static_version(request):
    return {'STATIC_VERSION': getattr(settings, 'STATIC_VERSION', '1')}


def footer_content(request):
    try:
        setting = FooterSetting.get_solo()
        sections = (
            FooterSection.objects
            .filter(is_active=True)
            .prefetch_related("links")
            .order_by("order", "id")
        )
    except (OperationalError, ProgrammingError):
        setting = FooterSetting()
        sections = FooterSection.objects.none()
    return {
        "footer_setting": setting,
        "footer_sections": sections,
    }
