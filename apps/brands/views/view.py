from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.brands.models import Brand
from apps.brands.serializers.serializers import BrandSerializer


@api_view(['GET', 'POST'])
def brand_list(request):
    if request.method == 'GET':
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def brand_detail(request, pk):
    try:
        brand = Brand.objects.get(pk=pk)
    except Brand.DoesNotExist:
        return Response({'error': 'Brand not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BrandSerializer(brand)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BrandSerializer(brand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def brand_by_slug(request, slug):
    try:
        brand = Brand.objects.get(slug=slug)
    except Brand.DoesNotExist:
        return Response({'error': 'Brand not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = BrandSerializer(brand)
    return Response(serializer.data)