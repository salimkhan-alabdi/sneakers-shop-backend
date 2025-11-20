from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from apps.products.models import Product
from apps.products.serializers.serializers import ProductListSerializer, ProductCreateUpdateSerializer


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        products = Product.objects.select_related('category', 'brand').prefetch_related('images', 'sizes').all()

        # Filterlar
        category_id = request.GET.get('category_id')
        brand_id = request.GET.get('brand_id')
        gender = request.GET.get('gender')
        color = request.GET.get('color')
        material = request.GET.get('material')
        price_min = request.GET.get('price_min')
        price_max = request.GET.get('price_max')
        rating = request.GET.get('rating')
        is_popular = request.GET.get('is_popular')
        is_new = request.GET.get('is_new')
        sizes = request.GET.get('sizes')

        if category_id:
            products = products.filter(category_id=category_id)
        if brand_id:
            products = products.filter(brand_id=brand_id)
        if gender:
            products = products.filter(gender=gender)
        if color:
            products = products.filter(color__icontains=color)
        if material:
            products = products.filter(material__icontains=material)
        if price_min:
            products = products.filter(price__gte=price_min)
        if price_max:
            products = products.filter(price__lte=price_max)
        if rating:
            products = products.filter(rating__gte=rating)
        if is_popular:
            products = products.filter(is_popular=is_popular.lower() == 'true')
        if is_new:
            products = products.filter(is_new=is_new.lower() == 'true')
        if sizes:
            products = products.filter(sizes__size=sizes).distinct()

        serializer = ProductListSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):
    try:
        product = Product.objects.select_related('category', 'brand').prefetch_related('images', 'sizes').get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductListSerializer(product)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProductCreateUpdateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)