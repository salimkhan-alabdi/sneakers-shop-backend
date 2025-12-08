from django.urls import path
from apps.shared.views import set_language, get_language

app_name = "shared"

urlpatterns = [
    path('language/set/', set_language, name='set-language'),
    path('language/get/', get_language, name='get-language'),
]