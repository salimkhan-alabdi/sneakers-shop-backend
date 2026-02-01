from rest_framework import serializers

from apps.products.models import Product, ProductImage, Size
from apps.brands.models import Brand
from apps.categories.models import Category


# --------------------
# BRAND
# --------------------
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            "id",
            "name",
            "slug",
        ]


# --------------------
# CATEGORY
# --------------------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "slug",
        ]


# --------------------
# PRODUCT IMAGE
# --------------------
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
        # 1. Пытаемся использовать ImageKit, если есть path
        if obj.image_path:
            ik = get_imagekit()
            if ik:
                try:
                    # Генерируем оптимизированное изображение
                    return ik.url({
                        "path": obj.image_path,
                        "transformation": [{"width": "600", "crop": "at_max"}]
                    })
                except Exception:
                    pass # Если ошибка в библиотеке, идем дальше

        # 2. Если ImageKit не сработал, отдаем прямой URL
        return obj.image_url 

# --------------------
# SIZE
# --------------------
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = [
            "id",
            "size",
            "stock",
        ]


# --------------------
# PRODUCT LIST
# --------------------
class ProductListSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    sizes = SizeSerializer(many=True, read_only=True)
    
    # Добавляем удобное поле для главного фото (фронтенд будет рад)
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "brand", "category", 
            "price", "gender", "color_hex", "material", 
            "is_popular", "is_new", "rating", 
            "images", "main_image", "sizes", 
            "created_at", "updated_at",
        ]

    def get_main_image(self, obj):
        # Ищем главное фото или просто первое в списке
        main_img = obj.images.filter(is_main=True).first() or obj.images.first()
        if main_img:
            # Используем уже готовую логику из ProductImageSerializer
            return ProductImageSerializer(main_img).get_image(main_img)
        return None

# --------------------
# PRODUCT CREATE / UPDATE
# --------------------
class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    sizes = SizeSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "brand",
            "price",
            "gender",
            "color_hex",
            "material",
            "is_popular",
            "is_new",
            "rating",
            "sizes",
        ]

    def create(self, validated_data):
        sizes_data = validated_data.pop("sizes", [])
        product = Product.objects.create(**validated_data)

        for size_data in sizes_data:
            Size.objects.create(product=product, **size_data)

        return product

    def update(self, instance, validated_data):
        sizes_data = validated_data.pop("sizes", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if sizes_data is not None:
            instance.sizes.all().delete()
            for size_data in sizes_data:
                Size.objects.create(product=instance, **size_data)

        return instance
