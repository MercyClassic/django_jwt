from rest_framework import serializers


class JWTLoginSerializer(serializers.Serializer):
    username_field = serializers.CharField()
    password = serializers.CharField()
