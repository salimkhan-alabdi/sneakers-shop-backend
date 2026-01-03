from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.translation import activate

from .utils import get_imagekit

class ImageKitAuthView(APIView):
 
    def get(self, request):
        imagekit = get_imagekit()
        return Response(imagekit.get_authentication_parameters())

@api_view(["POST"])
def set_language(request):
    language = request.data.get("language")

    if language not in ("uz", "ru", "en"):
        return Response(
            {"error": "Invalid language code. Allowed: uz, ru, en"},
            status=400,
        )

    activate(language)
    request.session["django_language"] = language

    return Response(
        {
            "message": "Language successfully changed",
            "language": language,
        }
    )

@api_view(["GET"])
def get_language(request):
    return Response(
        {
            "language": request.session.get("django_language", "uz"),
            "available_languages": ["uz", "ru", "en"],
        }
    )

