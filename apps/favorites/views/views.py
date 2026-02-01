from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.favorites.models import Favorite
from apps.favorites.serializers.serializers import FavoriteSerializer


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def favorite_list(request):
    if request.method == 'GET':
        try:
            favorites = Favorite.objects.filter(user=request.user).select_related('product')
            serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
            return Response(serializer.data)
        except Exception as e:
            # Вместо падения сервера возвращаем описание ошибки (для отладки)
            return Response({"error": "Serializer error", "details": str(e)}, status=500)

    elif request.method == 'POST':
        # Передаем request в контекст, чтобы сериализатор знал, какой юзер создает запись
        serializer = FavoriteSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Проверяем на дубликаты перед сохранением
            if Favorite.objects.filter(user=request.user, product=serializer.validated_data['product']).exists():
                return Response({'error': 'Ushbu mahsulot allaqachon sevimlilarda'}, status=400)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def favorite_delete(request, pk):
    """
    Sevimlilar ro'yxatidan mahsulotni o'chirish
    """
    try:
        favorite = Favorite.objects.get(pk=pk, user=request.user)
    except Favorite.DoesNotExist:
        return Response({'error': 'Sevimli topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    favorite.delete()
    return Response({'message': 'Sevimlilardan o\'chirildi'}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_favorite(request):
    """
    Sevimlilar toggle (qo'shish/o'chirish)
    Agar mavjud bo'lsa - o'chiradi, yo'q bo'lsa - qo'shadi
    """
    product_id = request.data.get('product_id')

    if not product_id:
        return Response({'error': 'product_id kerak'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        from apps.products.models import Product
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    favorite = Favorite.objects.filter(user=request.user, product=product).first()

    if favorite:
        # Agar mavjud bo'lsa - o'chirish
        favorite.delete()
        return Response({
            'message': 'Sevimlilardan o\'chirildi',
            'is_favorite': False
        })
    else:
        # Agar yo'q bo'lsa - qo'shish
        favorite = Favorite.objects.create(user=request.user, product=product)
        serializer = FavoriteSerializer(favorite, context={'request': request})
        return Response({
            'message': 'Sevimlilarga qo\'shildi',
            'is_favorite': True,
            'favorite': serializer.data
        }, status=status.HTTP_201_CREATED)