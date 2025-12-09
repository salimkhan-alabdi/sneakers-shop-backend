from django.urls import path
from apps.categories.views.category_view import category_list, category_detail, category_by_slug

app_name = "categories"

urlpatterns = [
    path('', category_list, name='category-list'),
    path('<int:pk>/', category_detail, name='category-detail'),
    path('<slug:slug>/', category_by_slug, name='category-by-slug'),
]