import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

jwt_payload_handler            =  api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler             =  api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler   =  api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

expire_delta = settings.JWT_AUTH['JWT_REFRESH_EXPIRATION_DELTA']


User = get_user_model()


class UserDetailSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['pk','username','uri']



class UserPublicSerializer(serializers.ModelSerializer):
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['pk' , 'username','uri']

    def get_uri(self , obj):
        return "/api/users/{pk}/".format(pk=obj.pk)




class UserRegisterSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(style={'input_type':'password'} , write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    token = serializers.SerializerMethodField(read_only=True)

    expires = serializers.SerializerMethodField(read_only=True)

    # token_response = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password2',
            'token',

            'expires',
            # 'token_response' # defined by get_token_response

            'message' # get_message
        ]
        extra_kwargs = {'password' : {'write_only' : True}}

# If we comment out password = ... and extra_kwargs = ... both and then assign a new user to #
# data dictionary in rest_api.py for creating new user then run rest_api.py #
# Then in output it will show password also in hashed format #


    def validate_email(self,value):
        qs = User.objects.filter(email__iexact = value)
        if qs.exists():
            raise serializers.ValidationError("User with this email already exists!")
        return value


    def validate_username(self,value):
        qs = User.objects.filter(username__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("User with this username already exists!")
        return value


    def get_token(self , obj): # instance of the model working with the serializer
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token


    def get_expires(self,obj): # actually no need of obj
        return timezone.now() + expire_delta - datetime.timedelta(seconds=200)


    # def get_token_response(self , obj):
    #     user = obj
    #
    #     ## Before creating extra context get_serializer_context in views
    #
    #     # payload = jwt_payload_handler(user)
    #     # token = jwt_encode_handler(payload)
    #     # response = jwt_response_payload_handler(token , user , request = None) # request = request
    #
    #     ## After creating extra context get_serializer_context in views
    #
    #     payload = jwt_payload_handler(user)
    #     token = jwt_encode_handler(payload)
    #     context = self.context
    #
    #     ## just for printing and checking ##
    #     request = context['request']
    #     print(request.user.is_authenticated)
    #
    #     response = jwt_response_payload_handler(token , user , request = context['request'])
    #
    #     return response


    def get_message(self,obj):
        return "Thank you for registering. Please verify your email before continuing."

    def validate(self, data):
        pwd = data.get('password')

        # pwd2 = data.get('password2')

        # To take out password2 which is giving us jsondecode error if we use .get
        pwd2 = data.pop('password2')


        if pwd != pwd2:
            raise serializers.ValidationError("Passwords must match!")

        return data

    def create(self, validated_data):
        print(validated_data)
        # user_obj = User.objects.create(username = validated_data.get('username'),
        #                            email = validated_data.get('email'))


        user_obj = User(username = validated_data.get('username'),
                        email = validated_data.get('email'))

        user_obj.set_password(validated_data.get('password'))
        user_obj.is_active = False # to check active status of use in django-admin interface
        user_obj.save()
        return user_obj