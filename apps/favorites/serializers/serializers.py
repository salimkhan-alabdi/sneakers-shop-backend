from rest_framework import serializers
from apps.favorites.models import Favorite
from apps.products.models import Product
from apps.shared.utils import get_imagekit

class FavoriteProductSerializer(serializers.Serializer):
    """Данные продукта внутри избранного с поддержкой ImageKit"""
    id = serializers.IntegerField()
    # ПРОВЕРЬ: если в модели Product поле называется 'title', оставь так. 
    # Если 'name', замени title на name ниже.
    title = serializers.CharField(source='title', default='') 
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        # 1. Пытаемся найти главное фото или любое первое
        img_obj = obj.images.filter(is_main=True).first() or obj.images.first()
        
        if not img_obj or not img_obj.image:
            return None

        try:
            # 2. Интеграция ImageKit
            ik = get_imagekit()
            path = str(img_obj.image)
            
            # Генерируем оптимизированный URL
            image_url = ik.url({
                "path": path,
                "transformation": [{"width": "400", "crop": "at_max"}]
            })
            return image_url
        except Exception:
            # 3. Резервный вариант: если ImageKit упал/не настроен, отдаем обычный URL
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(img_obj.image.url)
            return img_obj.image.url

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