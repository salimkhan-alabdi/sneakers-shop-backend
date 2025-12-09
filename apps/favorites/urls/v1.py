from django.urls import path
from apps.favorites.views.views import favorite_list, favorite_delete, toggle_favorite

app_name = "favorites"

urlpatterns = [
    path('', favorite_list, name='favorite-list'),
    path('<int:pk>/', favorite_delete, name='favorite-delete'),
    path('toggle/', toggle_favorite, name='favorite-toggle'),
]