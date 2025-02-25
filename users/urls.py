# myapp/urls.py
from django.conf import settings
from django.urls import path
from .views import UserRegistrationView, book_list
from .views import CustomAuthToken, EmailAuthToken, logout_view
from .views import protected_resource
from django.conf.urls.static import static


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', EmailAuthToken.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('protected/', protected_resource, name="protected_resource"),
    path('getAll/', book_list, name="protected_resource"),

]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)