from rest_framework import serializers
from apps.cart.models import Cart, CartItem
from apps.products.serializers.serializers import ProductListSerializer, SizeSerializer
from apps.shared.utils import get_imagekit

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    size = SizeSerializer(read_only=True, allow_null=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    
    product_image = serializers.SerializerMethodField()

    product_id = serializers.IntegerField(write_only=True)
    size_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_id', 'product_image', 
            'size', 'size_id', 'quantity', 'subtotal', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'subtotal', 'created_at', 'updated_at']

def get_image(self, obj):
    img_obj = obj.images.filter(is_main=True).first() or obj.images.first()
    if not img_obj:
        return None

    ik = get_imagekit()
    if ik and img_obj.image_path:
        try:
            return ik.url({
                "path": img_obj.image_path,
                "transformation": [{"width": "300"}]
            })
        except:
            pass # Если не вышло, идем к запасному варианту ниже
    
    # Запасной вариант (Fallback)
    return img_obj.image_url or None

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_items = serializers.IntegerField(read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'total_items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    size_id = serializers.IntegerField(required=False, allow_null=True)
    quantity = serializers.IntegerField(required=True, min_value=1)