from django.conf import settings
from .models import Category, BreakingTicker


def blog_context(request):
    return {
        'SITE_NAME': getattr(settings, 'SITE_NAME', 'PULSE'),
        'SITE_TAGLINE': getattr(settings, 'SITE_TAGLINE', "Africa's Trending Pulse"),
        'ADSENSE_CLIENT': getattr(settings, 'ADSENSE_CLIENT', ''),
        'all_categories': Category.objects.all(),
        'ticker_items': BreakingTicker.objects.filter(is_active=True)[:10],
    }
