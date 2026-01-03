from rest_framework import serializers

from apps.products.models import Product, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "image",
            "is_main",
            "created_at",
        ]

    def get_image(self, obj):
        if obj.image_url:
            return obj.image_url
        return None

class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "price",
            "gender",
            "color_hex",
            "material",
            "is_popular",
            "is_new",
            "rating",
            "images",
            "created_at",
            "updated_at",
        ]
