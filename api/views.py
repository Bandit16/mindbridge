from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import LetterImage


class AlphabetImagesAPI(GenericAPIView):
    queryset = LetterImage.objects.all()  
    lookup_field = "letter"

    def get(self, request, letter):
        # Filter images by letter
        images = LetterImage.objects.filter(letter__letter=letter.lower())

        if not images.exists():
            return Response({"error": "No images found for the requested letter"}, status=404)

        response_data = [
            {
                "image_url": request.build_absolute_uri(image.image.url),
                "is_correct": image.is_correct,
            }
            for image in images
        ]

        return Response({"status": "success", "data": response_data})

