from django.forms import ValidationError
from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from users.models import Book

from .serializers import BookSerializer, UserRegistrationSerializer
from rest_framework.authtoken.models import Token   
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from .serializers import EmailAuthTokenSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_resource(request):
    # Возвращаем некоторую защищенную информацию
    data = {
        "message": "This is a protected resource.",
        # "user": request.user.username,
    }
    return Response(data)
class EmailAuthToken(ObtainAuthToken):
    serializer_class = EmailAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                data = {
                    "user": {
                        "id": user.id,
                        "name": user.first_name,    
                        "email": user.email,
                    },
                    "code": status.HTTP_201_CREATED,
                    "message": "Пользователь создан",
                    
                }
                return Response(data, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({'errors': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Получаем токен текущего пользователя
        token = request.auth
        # Удаляем токен из базы данных
        token.delete()
        return Response({"message": "Successfully logged out."}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=400)
    
    
    

@api_view(['GET'])
def book_list(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        data = {
            "data": {
                *books
            },
            "code": status.HTTP_200_OK,
            "message": "Список книг для указанной страницы получен",
            "total_books": len(books), 
        }
        return Response(serializer.data)


# @api_view(['GET', 'PUT', 'DELETE'])
# def book_detail(request, pk):
#     try:
#         book = Book.objects.get(pk=pk)
#     except Book.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = BookSerializer(book)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         serializer = BookSerializer(book, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     elif request.method == 'DELETE':
#         book.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)