from django.urls import path
from apps.products.views.view import product_list, product_detail, product_by_slug

app_name = "products"

urlpatterns = [
    path('', product_list, name='product-list'),
    path('<int:pk>/', product_detail, name='product-detail'),
    path('<slug:slug>/', product_by_slug, name='product-by-slug'),
]