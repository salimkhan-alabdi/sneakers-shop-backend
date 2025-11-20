from django.urls import path

from apps.brands.views.view import brand_list, brand_detail

app_name = "brands"

urlpatterns = [
    path('', brand_list, name='brand-list'),
    path('<int:pk>/', brand_detail, name='brand-detail'),
]