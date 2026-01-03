from django.urls import path
from .views import ImageKitAuthView, set_language, get_language

app_name = "shared"

urlpatterns = [
    path("imagekit/auth/", ImageKitAuthView.as_view()),
    path("language/set/", set_language),
    path("language/get/", get_language),
]