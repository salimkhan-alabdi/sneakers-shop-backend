from rest_framework import serializers

from apps.products.models import (
    Product,
    ProductImage,
    Size,
)


# =========================
# SIZE
# =========================
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = [
            "id",
            "value",
        ]


# =========================
# PRODUCT IMAGE
# =========================
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
        return obj.image_url if obj.image_url else None


# =========================
# PRODUCT LIST
# =========================
class ProductListSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)

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
            "sizes",
            "images",
            "created_at",
            "updated_at",
        ]


# =========================
# PRODUCT CREATE / UPDATE
# =========================
class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "price",
            "gender",
            "color_hex",
            "material",
            "is_popular",
            "is_new",
            "rating",
        ]