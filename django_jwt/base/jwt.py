from datetime import datetime, timedelta

import jwt
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed

from django_jwt.config import DJANGO_JWT_SETTINGS


JWT_ALGORITHM = DJANGO_JWT_SETTINGS.ALGORITHM


def generate_jwt(
        data: dict,
        lifetime_seconds: int,
        secret: str,
) -> str:
    payload = data.copy()
    if lifetime_seconds:
        expires_delta = datetime.utcnow() + timedelta(seconds=lifetime_seconds)
        payload['exp'] = expires_delta
    return jwt.encode(payload, secret, JWT_ALGORITHM)


def decode_jwt(
        encoded_jwt: str,
        secret: str,
        soft: bool = False,
) -> dict:
    try:
        decoded_token = jwt.decode(
            encoded_jwt,
            secret,
            algorithms=[JWT_ALGORITHM],
            options={'verify_signature': False},
        )
        if decoded_token.get('exp') < datetime.utcnow().timestamp():
            if soft:
                """ FOR LOGOUT """
                return {'user_id': decoded_token.get('user_id')}
            raise AuthenticationFailed(
                code=status.HTTP_401_UNAUTHORIZED,
                detail='Token expired',
            )
    except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
        raise AuthenticationFailed(
            code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
        )
    return decoded_token
