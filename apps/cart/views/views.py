from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from apps.cart.models import Cart, CartItem
from apps.cart.serializers.serializers import CartSerializer, AddToCartSerializer, CartItemSerializer
from apps.products.models import Product, Size


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_cart(request):
    """
    Foydalanuvchi savatchasini olish
    """
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """
    Savatchaga mahsulot qo'shish
    """
    serializer = AddToCartSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    product_id = serializer.validated_data['product_id']
    size_id = serializer.validated_data.get('size_id')
    quantity = serializer.validated_data['quantity']

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({'error': 'Mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    # Size ixtiyoriy
    size = None
    if size_id:
        try:
            size = Size.objects.get(id=size_id, product=product)
        except Size.DoesNotExist:
            return Response({'error': 'O\'lcham topilmadi'}, status=status.HTTP_404_NOT_FOUND)

        if size.stock < quantity:
            return Response({
                'error': f'Omborda yetarli mahsulot yo\'q. Mavjud: {size.stock}'
            }, status=status.HTTP_400_BAD_REQUEST)

    cart, created = Cart.objects.get_or_create(user=request.user)

    if size:
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )
    else:

        cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        size=None, 
        defaults={'quantity': quantity}
)

    if not created:
        new_quantity = cart_item.quantity + quantity

        if size and size.stock < new_quantity:
            return Response({
                'error': f'Omborda yetarli mahsulot yo\'q. Mavjud: {size.stock}, Savatchada: {cart_item.quantity}'
            }, status=status.HTTP_400_BAD_REQUEST)

        cart_item.quantity = new_quantity
        cart_item.save()

    return Response({
        'message': 'Mahsulot savatchaga qo\'shildi',
        'cart': CartSerializer(cart).data
    }, status=status.HTTP_201_CREATED)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    """
    Savatcha mahsulotini yangilash (miqdorni o'zgartirish)
    """
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    quantity = request.data.get('quantity')
    if quantity is None:
        return Response({'error': 'quantity parametri kerak'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        quantity = int(quantity)
        if quantity < 1:
            return Response({'error': 'Miqdor 1 dan kichik bo\'lishi mumkin emas'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Noto\'g\'ri miqdor'}, status=status.HTTP_400_BAD_REQUEST)

    if cart_item.size and cart_item.size.stock < quantity:
        return Response({
            'error': f'Omborda yetarli mahsulot yo\'q. Mavjud: {cart_item.size.stock}'
        }, status=status.HTTP_400_BAD_REQUEST)

    cart_item.quantity = quantity
    cart_item.save()

    return Response({
        'message': 'Mahsulot yangilandi',
        'cart': CartSerializer(cart_item.cart).data
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    """
    Savatchadan mahsulotni o'chirish
    """
    try:
        cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
    except CartItem.DoesNotExist:
        return Response({'error': 'Mahsulot topilmadi'}, status=status.HTTP_404_NOT_FOUND)

    cart_item.delete()

    cart = Cart.objects.get(user=request.user)
    return Response({
        'message': 'Mahsulot savatchadan o\'chirildi',
        'cart': CartSerializer(cart).data
    })


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """
    Savatchani tozalash
    """
    cart = Cart.objects.get(user=request.user)
    cart.items.all().delete()

    return Response({
        'message': 'Savatcha tozalandi',
        'cart': CartSerializer(cart).data
    })