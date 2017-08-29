from hd_mesos.models import Users
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    nickname = serializers.CharField(required=False, max_length=16)
    role = serializers.BooleanField()
    password = serializers.CharField(max_length=128)
    class Meta:
        model = Users
        fields = ('url', 'username', 'nickname', 'role','password')
    
    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Users.objects.create(**validated_data)