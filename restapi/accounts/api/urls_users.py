from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token , refresh_jwt_token

from accounts.api.views import *

urlpatterns = [
    path('<str:username>/',UserDetailAPIView.as_view(),name="detail")

]