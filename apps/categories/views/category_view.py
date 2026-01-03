from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from apps.categories.models import Category
from apps.categories.serializers.serializers import CategorySerializer
from apps.brands.models import Brand
from apps.brands.serializers.serializers import BrandSerializer

@api_view(["GET", "POST"])
def category_list(request):
    if request.method == "GET":
        categories = Category.objects.all()
        serializer = CategorySerializer(
            categories,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)

    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "DELETE"])
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "GET":
        serializer = CategorySerializer(
            category,
            context={"request": request},
        )
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = CategorySerializer(
            category,
            data=request.data,
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    category.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["GET"])
def category_by_slug(request, slug):
    category = get_object_or_404(Category, slug=slug)

    serializer = CategorySerializer(
        category,
        context={"request": request},
    )
    return Response(serializer.data)

@api_view(["GET"])
def category_filters(request, slug):
    category = get_object_or_404(Category, slug=slug)

    brands = Brand.objects.filter(
        products__category=category
    ).distinct()

    return Response({
        "brands": BrandSerializer(brands, many=True).data
    })
