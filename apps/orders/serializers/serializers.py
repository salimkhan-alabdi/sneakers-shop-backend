from decimal import Decimal

from rest_framework import serializers

from apps.orders.models import Order, OrderItem
from apps.products.serializers.serializers import (
    ProductListSerializer,
    SizeSerializer,
)


# --------------------
# ORDER ITEM INPUT
# --------------------
class OrderItemInputSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    size = serializers.CharField(
        required=False,
        allow_blank=True,
        allow_null=True,
    )
    quantity = serializers.IntegerField(
        required=True,
        min_value=1,
    )


# --------------------
# ORDER ITEM OUTPUT
# --------------------
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    size = SizeSerializer(read_only=True, allow_null=True)

    subtotal = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True,
    )

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "size",
            "quantity",
            "price",
            "subtotal",
            "created_at",
        ]


# --------------------
# ORDER OUTPUT
# --------------------
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    payment_method_display = serializers.CharField(
        source="get_payment_method_display",
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "status_display",
            "full_name",
            "phone",
            "address",
            "city",
            "region",
            "postal_code",
            "payment_method",
            "payment_method_display",
            "is_paid",
            "paid_at",
            "subtotal",
            "delivery_price",
            "total_price",
            "note",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "is_paid",
            "paid_at",
        ]


# --------------------
# CREATE ORDER
# --------------------
class CreateOrderSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField()
    city = serializers.CharField(max_length=100)

    region = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100,
    )
    postal_code = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=20,
    )

    payment_method = serializers.ChoiceField(
        choices=["cash", "card", "payme", "click"],
        default="cash",
    )

    delivery_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0"),
        min_value=Decimal("0"),
    )

    note = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    items = OrderItemInputSerializer(many=True)
