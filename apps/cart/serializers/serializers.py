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

    def get_product_image(self, obj):
        """Получение оптимизированной ссылки через ImageKit"""
        product = obj.product
        # Ищем главное фото или любое доступное
        img_obj = product.images.filter(is_main=True).first() or product.images.first()
        
        if not img_obj or not img_obj.image:
            return None

        try:
            ik = get_imagekit()
            # Генерируем URL (например, квадрат 200x200 для превью в корзине)
            return ik.url({
                "path": str(img_obj.image),
                "transformation": [{
                    "height": "200",
                    "width": "200",
                    "crop": "at_max"
                }]
            })
        except Exception:
            # Если ImageKit не настроен, возвращаем обычную ссылку
            request = self.context.get('request')
            if request and hasattr(img_obj.image, 'url'):
                return request.build_absolute_uri(img_obj.image.url)
            return img_obj.image.url if hasattr(img_obj.image, 'url') else None

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