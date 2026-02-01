from rest_framework import serializers
from apps.favorites.models import Favorite
from apps.products.models import Product
from apps.shared.utils import get_imagekit

class FavoriteProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.SerializerMethodField()

def get_image(self, obj):
        # Ищем фото: сначала главное, если нет — любое
        img_obj = obj.images.filter(is_main=True).first() or obj.images.first()
        if not img_obj:
            return None

        # Пробуем ImageKit
        ik = get_imagekit()
        if ik and hasattr(img_obj, 'image_path') and img_obj.image_path:
            try:
                return ik.url({
                    "path": img_obj.image_path,
                    "transformation": [{"width": "400", "crop": "at_max"}]
                })
            except Exception:
                pass 

        # Если ImageKit не сработал или ключей нет, берем прямой URL
        return getattr(img_obj, 'image_url', None)

class FavoriteSerializer(serializers.ModelSerializer):
    product = FavoriteProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'product', 'product_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        product_id = validated_data['product_id']

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Mahsulot topilmadi"})

        # Метод get_or_create защитит от дублей и 500 ошибки при повторном клике
        favorite, created = Favorite.objects.get_or_create(user=user, product=product)
        
        if not created:
            raise serializers.ValidationError({"detail": "Bu mahsulot allaqachon sevimlilarda"})
            
        return favorite