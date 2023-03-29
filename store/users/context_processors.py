from products.models import Wishlist
from django.conf import settings

def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }


def main(request):
    try:
        wishlist = Wishlist.objects.get(user=request.user)
        product = wishlist.products.all().count()
    except Wishlist.DoesNotExist:
        product = []

    return {
        'wishlist_count': product
    }
