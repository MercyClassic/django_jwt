from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


from .jwt import decode_jwt
from django_jwt.config import DJANGO_JWT_SETTINGS


class JWTAuthenticateBackend(BaseAuthentication):
    def authenticate(self, request, *args, **kwargs) -> tuple | None:
        encoded_token = request.headers.get('Authorization')
        if not encoded_token:
            return None

        token_data = decode_jwt(
            encoded_token,
            DJANGO_JWT_SETTINGS.JWT_ACCESS_SECRET_KEY,
        )
        return token_data, None

    @staticmethod
    def get_user(user_id: int):
        user_model = get_user_model()
        query = user_model.objects
        load_only = DJANGO_JWT_SETTINGS.LOAD_ONLY
        if load_only:
            query = query.only(load_only)

        try:
            user = query.get(id=user_id)
        except user_model.DoesNotExist:
            return
        return user

    def authenticate_header(self, request):
        return 'Bearer'
