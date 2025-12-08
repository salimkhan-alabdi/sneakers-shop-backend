from django.urls import path
from apps.cart.views.views import (
    get_cart, add_to_cart, update_cart_item,
    remove_from_cart, clear_cart
)

app_name = "cart"

urlpatterns = [
    path('', get_cart, name='get-cart'),
    path('add/', add_to_cart, name='add-to-cart'),
    path('item/<int:item_id>/update/', update_cart_item, name='update-cart-item'),
    path('item/<int:item_id>/remove/', remove_from_cart, name='remove-from-cart'),
    path('clear/', clear_cart, name='clear-cart'),
]