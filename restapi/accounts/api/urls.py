from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token , refresh_jwt_token

from accounts.api.views import *

urlpatterns = [
    path('',AuthView.as_view()),
    path('register/',RegisterAPIView.as_view()),

    path('jwt/',obtain_jwt_token),
    path('jwt/refresh/',refresh_jwt_token),

]