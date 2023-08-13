from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from . import serializers


class BaseJWTLoginAPIVIew(GenericAPIView):
    service = None
    serializer_class = serializers.JWTLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            tokens = self.service.jwt_login(serializer.validated_data)
            response = Response(
                status=status.HTTP_200_OK,
                data={'access_token': tokens['access_token']},
            )
            response.set_cookie(key='refresh_token', value=tokens['refresh_token'], httponly=True)
            return response
        return Response(status=status.HTTP_401_UNAUTHORIZED, data='Could not validate credentials')


class BaseJWTRefreshAPIVIew(APIView):
    service = None
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        tokens = self.service.refresh_access_token(request)
        response = Response(
            status=status.HTTP_200_OK,
            data={'access_token': tokens['access_token']},
        )
        response.set_cookie(key='refresh_token', value=tokens['refresh_token'], httponly=True)
        return response


class BaseJWTLogoutAPIVIew(APIView):
    service = None

    def post(self, request, *args, **kwargs):
        token = request.COOKIES.get('refresh_token')
        if not token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        self.service.jwt_logout(request)
        response = Response(status=status.HTTP_200_OK)
        response.delete_cookie(key='refresh_token')
        return response
