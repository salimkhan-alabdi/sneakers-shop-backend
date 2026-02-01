from rest_framework import serializers
from apps.favorites.models import Favorite


class FavoriteProductSerializer(serializers.Serializer):
    """Favorite ichidagi product ma'lumotlari"""
    id = serializers.IntegerField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        # Birinchi asosiy rasmni olish
        main_image = obj.images.filter(is_main=True).first()
        if main_image and main_image.image_url:
            return main_image.image_url
        # Agar asosiy rasm bo'lmasa, birinchi rasmni olish
        first_image = obj.images.first()
        if first_image and first_image.image_url:
            return first_image.image_url
        return None


class FavoriteSerializer(serializers.ModelSerializer):
    product = FavoriteProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'product', 'product_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # user'ni request'dan olamiz (view'da context orqali beriladi)
        user = self.context['request'].user
        product_id = validated_data['product_id']

        # Mahsulot mavjudligini tekshirish
        from apps.products.models import Product
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError({"product_id": "Mahsulot topilmadi"})

        # Allaqachon sevimlilarda borligini tekshirish
        if Favorite.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError({"detail": "Bu mahsulot allaqachon sevimlilarda"})

        # Sevimlilar ro'yxatiga qo'shish
        favorite = Favorite.objects.create(user=user, product=product)
        return favorite