from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotFound,
    PermissionDenied,
)

from django_jwt.config import DJANGO_JWT_SETTINGS
from .jwt import decode_jwt, generate_jwt


class BaseTokenActions:
    user_model = get_user_model()

    def generate_auth_tokens(self, user_data: dict) -> dict:
        access_token = generate_jwt(
            data=user_data,
            lifetime_seconds=DJANGO_JWT_SETTINGS.ACCESS_TOKEN_LIFETIME_SECONDS,
            secret=DJANGO_JWT_SETTINGS.JWT_ACCESS_SECRET_KEY,
        )
        refresh_token = generate_jwt(
            data=user_data,
            lifetime_seconds=DJANGO_JWT_SETTINGS.REFRESH_TOKEN_LIFETIME_SECONDS,
            secret=DJANGO_JWT_SETTINGS.JWT_REFRESH_SECRET_KEY,
        )
        self.save_refresh_token(user_id=user_data.get('user_id'), token=refresh_token)
        return {'access_token': access_token, 'refresh_token': refresh_token}

    def save_refresh_token(self, **kwargs):
        raise NotImplementedError

    def jwt_login(self, serialized_data: dict) -> dict:
        filtering = {self.user_model.USERNAME_FIELD: serialized_data.get('username_field')}
        try:
            user = (
                self.user_model.objects
                .only('id', 'password', 'is_active')
                .get(**filtering)
            )
        except self.user_model.DoesNotExist:
            raise NotFound
        if not user.check_password(serialized_data.get('password')):
            raise AuthenticationFailed
        if not user.is_active:
            raise PermissionDenied(code=status.HTTP_403_FORBIDDEN, detail='User is not active')
        user_data = {'user_id': user.pk}

        extra_attrs = DJANGO_JWT_SETTINGS.EXTRA_ATTRS_FUNC
        if extra_attrs:
            user_data.update(extra_attrs(user_id=user.pk))

        return self.generate_auth_tokens(user_data)

    def delete_refresh_token(self, user_id: int, token: str) -> None:
        raise NotImplementedError

    def refresh_access_token(self, request) -> dict:
        token = request.COOKIES.get('refresh_token')
        token_data = decode_jwt(token, secret=DJANGO_JWT_SETTINGS.JWT_REFRESH_SECRET_KEY)
        self.delete_refresh_token(request.user.pk, token)
        user = (
            self.user_model.objects
            .only('id', 'is_active')
            .get(id=token_data.get('user_id'))
        )
        if not user.is_active:
            raise PermissionDenied(code=status.HTTP_403_FORBIDDEN, detail='User is not active')

        user_data = {'user_id': user.pk}
        extra_attrs = DJANGO_JWT_SETTINGS.EXTRA_ATTRS_FUNC
        if extra_attrs:
            user_data.update(extra_attrs(user_id=user.pk))

        return self.generate_auth_tokens(user_data)

    def jwt_logout(self, request) -> None:
        token = request.COOKIES.get('refresh_token')
        token_data = decode_jwt(
            token,
            secret=DJANGO_JWT_SETTINGS.JWT_REFRESH_SECRET_KEY,
            soft=True,
        )

        self.delete_refresh_token(token_data.get('user_id'), token)
