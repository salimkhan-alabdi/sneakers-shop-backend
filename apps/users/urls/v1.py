from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views.views import register, login, profile, update_profile

app_name = "users"

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update-profile'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]