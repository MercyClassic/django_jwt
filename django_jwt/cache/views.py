from django_jwt.base.views import (
    BaseJWTLoginAPIVIew,
    BaseJWTRefreshAPIVIew,
    BaseJWTLogoutAPIVIew,
)
from .service import JWTCached


class JWTLoginAPIVIew(BaseJWTLoginAPIVIew):
    service = JWTCached()


class JWTRefreshAPIVIew(BaseJWTRefreshAPIVIew):
    service = JWTCached()


class JWTLogoutAPIVIew(BaseJWTLogoutAPIVIew):
    service = JWTCached()
