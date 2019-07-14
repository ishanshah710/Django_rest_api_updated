from rest_framework import serializers

from accounts.api.serializers import UserPublicSerializer
from status.models import Status

'''
serializers --> can convert data to JSON
serializers --> can also validate data
'''


class StatusSerializer(serializers.ModelSerializer):
    user = UserPublicSerializer(read_only=True)
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Status
        fields = [
            'uri',
            'pk',
            'user',
            'content',
            'image'
        ]
        read_only_fields = ['user']

    def get_uri(self,obj):
        return "/api/status/{pk}".format(pk=obj.pk)


    def validate(self , data):
        content = data.get("content",None)
        if content == "":
            content = None
        image = data.get("image",None)
        if content is None and image is None:
            raise serializers.ValidationError("Content or image is required!")
        return data
