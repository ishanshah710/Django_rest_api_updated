from django.contrib.auth import authenticate , get_user_model
from django.db.models import Q

from rest_framework import permissions, generics

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

# from rest_framework_jwt.utils import jwt_response_payload_handler
from accounts.api.permissions import AnonPermissionOnly
from accounts.api.serializers import UserRegisterSerializer, UserDetailSerializer

jwt_payload_handler            =  api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler             =  api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler   =  api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


User = get_user_model()

class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active = True)
    serializer_class = UserDetailSerializer
    lookup_field = 'username'


class AuthView(APIView):
    # authentication_classes = []
    # permission_classes = [permissions.AllowAny]
    permission_classes = [AnonPermissionOnly]


    def post(self , request , *args , **kwargs):
        # print(request.user)  --> AnonymousUser

        if request.user.is_authenticated:
            return Response({'detail' : 'you are there by already authenticated!'} , status=400)

        data = request.data
        username = data.get('username')
        password = data.get('password')

        # user = authenticate(username = username , password = password)  # bcoz the if cond qs.count() do thid for us !

        # print(user)  --> ishan

        # To use that custom user model (get_user_model with instance User)
        qs = User.objects.filter(
            Q(username__iexact = username) |  # Try to authenticate with username or email which is passed in username = data.get('username')
            Q(email__iexact = username)
        ).distinct() # this allows us to do one of these

        if qs.count() == 1: # i.e. it exists
            user_obj = qs.first()
            if user_obj.check_password(password):
                user = user_obj

                # To crate token manually
                payload = jwt_payload_handler(user)
                # payload = jwt_response_payload_handler(user)

                token = jwt_encode_handler(payload)

                response = jwt_response_payload_handler(token, user,
                                                        request=request)  # bcoz request is passed in post method
                # so need to use request = self.request

                return Response(response)

                # return Response({'token' : token})

        return Response({'detail' : 'Invalid Creditentials'} , status=401) # just a response


        # # To crate token manually
        # payload = jwt_payload_handler(user)
        # # payload = jwt_response_payload_handler(user)
        #
        # token = jwt_encode_handler(payload)
        #
        # response = jwt_response_payload_handler(token , user , request=request) # bcoz request is passed in post method
        # # so need to use request = self.request
        #
        # return Response(response)
        #
        # # return Response({'token' : token})



class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AnonPermissionOnly]

    def get_serializer_context(self, *args ,**kwargs): #just an extra context passing
    # in UserRegister Serializer and it returns dict called 'request'
        return { 'request' : self.request }

    # Thats how we passed requested data to serializer



# RegisterAPIView without using serializers

# class RegisterAPIView(APIView):
#     permission_classes = [permissions.AllowAny]
#     def post(self , request , *args , **kwargs):
#         if request.user.is_authenticated:
#             return Response({'detail' : 'you are already registered and are authenticated!'} , status=400)
#         data = request.data
#         username    = data.get('username')
#         email       = data.get('username')
#         password    = data.get('password')
#         password2   = data.get('password2')
#
#
#         qs = User.objects.filter(
#             Q(username__iexact = username) |  # Try to authenticate with username or email which is passed in username = data.get('username')
#             Q(email__iexact = username)
#         )
#
#         if password != password2:
#             return Response({"password":"Both Passwords don't match!"})
#
#         if qs.exists():
#             return Response({"detail" : "This user already exists!"} , status=401)
#         else:
#             user = User.objects.create(username=username , email=email)
#             user.set_password(password)
#             user.save()
#
#             # payload = jwt_payload_handler(user)
#             # token = jwt_encode_handler(payload)
#             # response = jwt_response_payload_handler(token, user,
#             #                                         request=request)
#
#             # return Response(response , status=201)
#
#             return Response({'detail' : 'Thank you for registering. Please verify your email.'} , status = 201)
#
#         return Response({'detail' : 'Invalid Request!'} , status=401) # just a response
