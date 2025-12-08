from django.contrib import admin
from apps.cart.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['subtotal']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_items', 'total_price', 'created_at']
    search_fields = ['user__username', 'user__email']
    inlines = [CartItemInline]


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'product', 'size', 'quantity', 'subtotal', 'created_at']
    search_fields = ['product__name', 'cart__user__username']
    list_filter = ['created_at']