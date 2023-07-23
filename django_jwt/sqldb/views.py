from django_jwt.base.views import (
    BaseJWTLoginAPIVIew,
    BaseJWTRefreshAPIVIew,
    BaseJWTLogoutAPIVIew,
)
from .service import JWTSqlDB


class JWTLoginAPIVIew(BaseJWTLoginAPIVIew):
    service = JWTSqlDB()


class JWTRefreshAPIVIew(BaseJWTRefreshAPIVIew):
    service = JWTSqlDB()


class JWTLogoutAPIVIew(BaseJWTLogoutAPIVIew):
    service = JWTSqlDB()
