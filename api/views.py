from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .models import LetterImage, Letter , GameImage 
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from django.http import JsonResponse
from firebase_admin import auth
from firebase_admin import firestore
from .models import User , TestProgress
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class AlphabetImagesAPI(GenericAPIView):
    permission_classes = [AllowAny]

    queryset = LetterImage.objects.all()
    lookup_field = "letter"

    def get(self, request, letter):
        try:
            letter_obj = Letter.objects.get(letter=letter.lower())
        except Letter.DoesNotExist:
            return Response({"error": "Letter not found"}, status=404)

        images = LetterImage.objects.filter(letter=letter_obj)

        if not images.exists():
            return Response({"error": "No images found for the requested letter"}, status=404)

        response_data = {
            "character_image_url": request.build_absolute_uri(letter_obj.character_image.url) if letter_obj.character_image else None,
           
            "images": [
                {
                    "image_url": request.build_absolute_uri(image.image.url),
                    "is_correct": image.is_correct,
                }
                for image in images
            ]
        }

        return Response({"status": "success", "data": response_data})

class GameImagesAPI(GenericAPIView):
    permission_classes = [AllowAny]

    queryset = GameImage.objects.all()
    lookup_field = "letter"

    def get(self, request, letter):
        try:
            letter_obj = Letter.objects.get(letter=letter.lower())
        except Letter.DoesNotExist:
            return Response({"error": "Letter not found"}, status=404)

        images = GameImage.objects.filter(letter=letter_obj)
        if not images.exists():
            return Response({"error": "No images found for the requested letter"}, status=404)

        response_data = {
            "character_image_url": request.build_absolute_uri(letter_obj.character_image.url) if letter_obj.character_image else None,
            "images": [
                {
                    "image_url": request.build_absolute_uri(image.image.url),
                    "description": image.description,
                }
                for image in images
            ]
        }

        return Response({"status": "success", "data": response_data})
    



def test_firebase(request):
    try:
        # Retrieve a list of users (for testing purposes)
        users = auth.list_users().iterate_all()
        user_list = [{"uid": user.uid, "email": user.email} for user in users]
        return JsonResponse({"users": user_list})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    

    


class SyncFirebaseUsers(APIView):
    queryset = User.objects.all()  # Required for permissions like DjangoModelPermissions
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            users = auth.list_users().iterate_all()
            created_count = 0
            for user in users:
                obj, created = User.objects.get_or_create(
                    firebase_uid=user.uid,
                    defaults={
                        'email': user.email,
                        'name': user.display_name or "Anonymous"
                    }
                )
                if created:
                    created_count += 1
            return Response({
                "message": f"Firebase users synced successfully. {created_count} users created."
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
class SaveProgress(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            firebase_uid = request.data.get('firebase_uid')
            test_name = request.data.get('test_name')
            score = request.data.get('score')
            time_spent = request.data.get('time_spent')  # e.g., '00:10:30'

            user = User.objects.get(firebase_uid=firebase_uid)
            TestProgress.objects.create(
                user=user,
                test_name=test_name,
                score=score,
                time_spent=time_spent,
            )
            return Response({"message": "Progress saved successfully."})
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)