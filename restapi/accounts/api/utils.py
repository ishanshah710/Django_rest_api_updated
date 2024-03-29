import datetime

from django.conf import settings
from django.utils import timezone

expire_delta = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']

from rest_framework_jwt.settings import api_settings



def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        # 'user': UserSerializer(user, context={'request': request}).data
        'user':user.username,
        'expires' : timezone.now() + expire_delta - datetime.timedelta(seconds=200)
    }

