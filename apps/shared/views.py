from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.translation import activate


@api_view(['POST'])
def set_language(request):
    """
    Tilni o'zgartirish
    Request: {"language": "uz"} yoki "ru" yoki "en"
    """
    language = request.data.get('language', 'uz')

    if language in ['uz', 'ru', 'en']:
        activate(language)
        request.session['django_language'] = language
        return Response({
            'message': 'Til muvaffaqiyatli o\'zgartirildi',
            'language': language
        })

    return Response({
        'error': 'Noto\'g\'ri til kodi. Faqat uz, ru, en'
    }, status=400)


@api_view(['GET'])
def get_language(request):
    """
    Joriy tilni olish
    """
    language = request.session.get('django_language', 'uz')
    return Response({
        'language': language,
        'available_languages': ['uz', 'ru', 'en']
    })