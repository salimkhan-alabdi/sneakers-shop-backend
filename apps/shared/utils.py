from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from imagekitio import ImageKit
from django.conf import settings


def superuser_required(view_func):
    """
    Decorator faqat superuser uchun view'ni ochadi
    """

    def check_superuser(user):
        if not user.is_superuser:
            raise PermissionDenied
        return True

    decorated_view = user_passes_test(check_superuser)(view_func)
    return decorated_view



def get_imagekit():
    return ImageKit(
        public_key=settings.IMAGEKIT_PUBLIC_KEY,
        private_key=settings.IMAGEKIT_PRIVATE_KEY,
        url_endpoint=settings.IMAGEKIT_URL_ENDPOINT,
    )